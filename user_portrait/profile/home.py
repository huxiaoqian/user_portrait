# -*- coding: utf-8 -*-

import json

from flask import views, Blueprint, render_template, request

from toogle.extensions import es, redis

bp = Blueprint('home', __name__)


class HomeView(views.MethodView):
    """
    搜索首页和结果展示页
    """

    home_template = 'home.html'
    index_template = 'index.html'

    def get(self):
        #q = request.args.get('q')
        fuzz_item = ['uid', 'nick_name', 'real_name']
        data = {}
        query = []
        num = 0
        data['uid'] = request.args.get('q1')
        data['nick_name'] = request.args.get('q2')
        data['real_name'] = request.args.get('q3')
        data['isreal'] = request.args.get('tn')
        data['sex'] = request.args.get('sex')
        data['weibo_from'] = request.args.get('q5')
        data['weibo_to'] = request.args.get('q6')
        size = request.args.get('size')
        if data['isreal'] == '2':
            data['isreal'] = ''
        if data['sex'] == '0':
            data['sex'] = ''
        for key in data:
            if data[key]:
                if key in fuzz_item:
                    query.append({'wildcard':{key : "*" + data[key] + '*'}})
                    num += 1
                elif key == 'weibo_from' or 'weibo_to':
                    query.append({'range':{"statusnum":{"from":data['weibo_from'],"to":data['weibo_to']}}})
                    num += 1
                else :
                    query.append({'match':{key : data[key]}})
                    num += 1

        # nick_name = request.args.get('q2')
        # if q is not None:
        #     q = q.strip()
        # if not q:
        #     return render_template(self.home_template)
        
        # add to redis
        #redis.sadd('keywords', q)
        # es search
        if num > 0:
            try:
                source = es.search(
                    index = 'weibo_user',
                    doc_type = 'user',
                    body = {
                        'query':{
                            'bool':{
                                'must':query
                            }
                        }
                    },
                    size = size
                )
            except Exception as e:
                # TODO handle exception
                raise e 
        else:
            source = es.search(
                index = 'weibo_user',
                doc_type = 'user',
                body = {
                    'query':{'match_all':{}}
                },
                size = 100
            )

        return render_template(self.index_template, source=source)


class KeywordView(views.MethodView):
    """关键词搜索热度展示页"""

    template = 'keyword.html'

    def get(self):
        keywords = list(redis.smembers('keywords'))
        return render_template(self.template, keywords=json.dumps(keywords))


bp.add_url_rule('/', view_func=HomeView.as_view('homepage'))
bp.add_url_rule('/keywords/', view_func=KeywordView.as_view('keyword'))
