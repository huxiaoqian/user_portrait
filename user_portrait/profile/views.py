# -*- coding:utf-8 -*-
import json
from flask import views, Blueprint, render_template, request
from user_portrait.search_user_profile import es_get_source, es_mget_source
from user_portrait.global_utils import es_user_profile
from .form import SearchForm


mod = Blueprint('profile', __name__, url_prefix='/profile')
es = es_user_profile

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

class SearchView(views.MethodView):
    """多维度复杂检索页"""

    template = ''

    def get(self):
        form = SearchForm()
        return render_template(self.template, form=form)

    def post(self):
        form = SearchForm()
        if not form.validate_on_submit():
            return render_template(self.template, form=form)
        # TODO es search
        try:
            source = es.search(size=100)
        except Exception as e:
            raise e
        return render_template(self.template, source=source)

class UserView(views.MethodView):
    """
    单个用户的个人信息页面
    """
    template = 'individual.html'

    def get(self, id):
        user = es_get_source(id)
        followers = []
        friends = []
        if user:
            user_followers_ids = user.get('followers')
            user_friends_ids = user.get('friends')
            if user_followers_ids:
                followers = es_mget_source(user_followers_ids)
            if user_friends_ids:
                friends = es_mget_source(user_friends_ids)

        return render_template(self.template, user=user,
                               followers=followers, friends=friends,
                               id=id)


class UserFollowersView(views.MethodView):
    """
    单个用户与粉丝的关联延伸
    """

    template = 'individual_followers.html'

    def get(self, id):
        return render_template(self.template, id=id)


class UserFriendsView(views.MethodView):
    """
    单个用户与好友的关联延伸
    """

    template = 'individual_friends.html'

    def get(self, id):
        return render_template(self.template, id=id)

mod.add_url_rule('/', view_func=HomeView.as_view('homepage'))
mod.add_url_rule('/keywords/', view_func=KeywordView.as_view('keyword'))
mod.add_url_rule('/search/', view_func=SearchView.as_view('index'))
mod.add_url_rule('/<id>/', view_func=UserView.as_view('detail'))
mod.add_url_rule('/<id>/followers/', view_func=UserFollowersView.as_view('followers'))
mod.add_url_rule('/<id>/friends/', view_func=UserFriendsView.as_view('friends'))
