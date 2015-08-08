# -*- coding:utf-8 -*-
import json
import csv
from flask import views, Blueprint, render_template, request
from user_portrait.global_utils import es_user_profile as es
from user_portrait.search_user_profile import es_get_source, es_mget_source
from os.path import dirname, abspath, join
from .form import SearchForm


mod = Blueprint('profile', __name__, url_prefix='/profile')



class HomeView(views.MethodView):
    """
    搜索首页和结果展示页
    """
    index_template = 'index.html'

    def get(self):
        #q = request.args.get('q')
        item_content = []
        item_head = []
        fuzz_item = ['uid', 'nick_name']
        data = {}
        query = []
        num = 0
        data['uid'] = request.args.get('uidnickname')
        data['nick_name'] = request.args.get('uidnickname')
        for key in data:
            if data[key]:
                if key in fuzz_item:
                    query.append({'wildcard':{key : "*" + data[key] + '*'}})
                    num += 1
        if num > 0:
            try:
                source = es.search(
                    index = 'weibo_user',
                    doc_type = 'user',
                    body = {
                        'query':{
                            'bool':{
                                'should':query
                            }
                        },
                        "sort":[{'statusnum':{'order':'desc'}}],
                        "size" : 100
                        }
                )
            except Exception as e:
                # TODO handle exception
                raise e 
        else:
            source = es.search(
                index = 'weibo_user',
                doc_type = 'user',
                body = {
                    'query':{'match_all':{}
                },
                    "sort":[{'statusnum':{'order':'desc'}}],
                    "size" : 100
                    }
            )
        file_location = dirname(dirname(abspath(__file__)))+'/static/download/test.csv'
        isflag = 1
        csvfile = file(file_location, 'wb')
        writer = csv.writer(csvfile)
        for key in source['hits']['hits']:
            item_content = []
            source_content = key['_source']
            if isflag:
                item_head = [key for key in source_content]
                writer.writerow(item_head)
                isflag = 0
    
            for key in source_content:

                item_content.append(self.decode_item(source_content[key]))
            writer.writerow(item_content)

        return render_template(self.index_template, source=source, data=data)

    def decode_item(self, data):
        try:
            result = data.encode('utf-8')
        except:
            result = data
        return result


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
        return render_template(self.template, source=source, data=data)

class IndividualView(views.MethodView):
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

class Testviews(views.MethodView):

    def get(self):
        return  render_template('test.html')
class UserView(views.MethodView):
    """user detail information"""
    def get(self):
        item_head = []
        fuzz_item = ['uid', 'nick_name', 'real_name', 'user_location', 'user_email', 'user_birth']
        range_item = ['statusnum', 'fansnum', 'friendsnum']
        select_item = ['sex', 'tn', 'sp_type']
        data = {}
        query = []
        num = 0
        order = []
        data['uid'] = request.args.get('q0')
        data['nick_name'] = request.args.get('q2')
        data['real_name'] = request.args.get('q3')
        data['sp_type'] = request.args.get('q4')
        data['tn'] = request.args.get('tn')
        data['sex'] = request.args.get('sex')
        data['user_email'] = request.args.get('q7') 
        data['user_location'] = request.args.get('q12')
        data['user_birth'] = request.args.get('q13')
        rank_order = request.args.get('order')
        for key in range_item:
            data[key] = {}
        data['statusnum']['from'] = '0'
        data['statusnum']['to'] = '100000000'
        data['fansnum']['from'] = '0'
        data['fansnum']['to'] = '100000000'
        data['friendsnum']['from'] = '0'
        data['friendsnum']['to'] = '100000000'
        data['statusnum']['from'] = request.args.get('q5')
        data['statusnum']['to'] = request.args.get('q6')
        data['fansnum']['from'] = request.args.get('q8')
        data['fansnum']['to'] = request.args.get('q9')
        data['friendsnum']['from'] = request.args.get('q10')
        data['friendsnum']['to'] = request.args.get('q11')
        size = request.args.get('size')
        if size == '':
            size = 100
        for key in range_item:
            if data[key]['from'] == '' and data[key]['to'] != '':
                data[key]['from'] = '0'
            if data[key]['from'] != '' and data[key]['to'] == '':
                data[key]['to'] = '100000000'
        if rank_order == "0":
            order = [{'statusnum':{'order':'desc'}}]
        if rank_order == "1":
            order = [{'fansnum':{'order':'desc'}}]
        if rank_order == "2":
            order = [{'friendsnum':{'order':'desc'}}]

        if data['tn'] == '2':
            data['tn'] = ''
        if data['sex'] == '3':
            data['sex'] = ''
        if data['sp_type'] == '0':
            data['sp_type'] = ''
        for key in data:
            if data[key] and key not in range_item:
                if key in fuzz_item:
                    query.append({'wildcard':{key : "*" + data[key] + '*'}})
                    num += 1
                if key in select_item :
                    if data[key]:
                        query.append({'match':{key : data[key]}})
                        num += 1
            elif data[key]:
                if data[key]['from'] and data[key]['to']:
                    query.append({'range':{key:{"from":data[key]['from'],"to":data[key]['to']}}})
                    num += 1

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
                        },
                        "sort":order,
                        "size" : size
                        }
                )
            except Exception as e:
                # TODO handle exception
                raise e 
        else:
            source = es.search(
                index = 'weibo_user',
                doc_type = 'user',
                body = {
                    'query':{'match_all':{}
                },
                    "sort":[{'statusnum':{'order':'desc'}}],
                    "size" : 100
                    }
            )
        file_location = dirname(dirname(abspath(__file__)))+'/static/download/test.csv'
        isflag = 1
        csvfile = file(file_location, 'wb')
        writer = csv.writer(csvfile)
        for key in source['hits']['hits']:
            item_content = []
            source_content = key['_source']
            if isflag:
                item_head = [key for key in source_content]
                writer.writerow(item_head)
                isflag = 0
            for key in source_content:
                item_content.append(self.decode_item(source_content[key]))
            writer.writerow(item_content)
        csvfile.close()

        return json.dumps(source)

    def decode_item(self, data):
        try:
            result = data.encode('utf-8')
        except:
            result = data
        return result

class DownloadView(views.MethodView):

    def get(self):
        user_id = request.args.get('id')
        select_id = user_id.split(',')
        file_location = dirname(dirname(abspath(__file__)))+'/static/download/test.csv'
        isflag = 1
        csvfile = file(file_location, 'wb')
        writer = csv.writer(csvfile)

        for uid in select_id:
            item_content = []
            if uid:
                source = es.search(
                    index = 'weibo_user',
                    doc_type = 'user',
                    body ={
                        'query':{
                            'match':{'id':uid}
                        },
                        'size':1
                    }                        
                )
                source_content = source['hits']['hits'][0]['_source']
                if isflag:
                    item_head = [key for key in source_content]
                    writer.writerow(item_head)
                    isflag = 0

                for key in source_content:
                    if isinstance(source_content[key],unicode):
                        print 'it is unicode'
                    item_content.append(self.decode_item(source_content[key]))

                writer.writerow(item_content)

        csvfile.close()
        return  json.dumps(source)

    def decode_item(self, data):
        try:
            result = data.encode('utf-8')
        except:
            result = data
        return result

mod.add_url_rule('/', view_func=HomeView.as_view('homepage'))
mod.add_url_rule('/keywords/', view_func=KeywordView.as_view('keyword'))
mod.add_url_rule('/search/', view_func=SearchView.as_view('index'))
mod.add_url_rule('/<id>/', view_func=IndividualView.as_view('detail'))
mod.add_url_rule('/<id>/followers/', view_func=UserFollowersView.as_view('followers'))
mod.add_url_rule('/<id>/friends/', view_func=UserFriendsView.as_view('friends'))
mod.add_url_rule('/test/', view_func=Testviews.as_view('test'))
mod.add_url_rule('/user/', view_func=UserView.as_view('user'))
mod.add_url_rule('/download/', view_func=DownloadView.as_view('download'))
