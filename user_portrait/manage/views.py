# -*- coding:utf-8 -*-
import json
import time
from elasticsearch import Elasticsearch
from flask import Blueprint, redirect, views, render_template, request
from process import es_create
from user_portrait.global_utils import es_user_portrait

mod = Blueprint('manage', __name__, url_prefix='/manage')

es = es_user_portrait
index_type = 'user'
index_name = "user_portrait"

es_create() # init data

search_template = 'search_list.html'

@mod.route('/list/')
def user_list():
    query_body = {
        'query':{
            'match_all': {}
        },
        'size': 100
    }
    results = es.search(index=index_name, doc_type=index_type, body=query_body)['hits']['hits']
    item_set = []
    for item in results:
        item_set.append(item['_source'])
    # return json.dumps(item_set)
    print item_set
    return render_template(search_template,item_set=item_set)

@mod.route('/delete/')
def es_delete():
    ids = ['1111111111', '11111']
    bulk_action = []
    for uid in ids:
        action = {"delete": {"_id": uid}}
        bulk_action.append(action)
    es.bulk(bulk_action, index=index_name, doc_type=index_type)
    time.sleep(1)
    return redirect('/manage/list/')

@mod.route('/search_by_id/')
def es_search_by_id():
    uid = '0000000000'
    query_body = {
        'query':{
            'term': {'uid': uid}
        },
        'size': 10000
    }
    results = es.search(index=index_name, doc_type=index_type, body=query_body)['hits']['hits']
    item_set = []
    for item in results:
        item_set.append(item['_source'])
    return json.dumps(item_set)

@mod.route('/search_by_topic/')
def es_search_by_topic():
    topic = 'education'
    query_body = {
        'query':{
            'term': {'topic': topic}
        },
        'size': 10000
    }
    results = es.search(index=index_name, doc_type=index_type, body=query_body)['hits']['hits']
    item_set = []
    for item in results:
        item_set.append(item['_source'])
    return json.dumps(item_set)

@mod.route('/search_by_area/')
def es_search_by_area():
    area = 'politics'
    query_body = {
        'query':{
            'term': {'area': area}
        },
        'size': 10000
    }
    results = es.search(index=index_name, doc_type=index_type, body=query_body)['hits']['hits']
    item_set = []
    for item in results:
        item_set.append(item['_source'])
    return json.dumps(item_set)

@mod.route('/search_multi/')
def es_search_multi():
    area = 'politics'
    topic = 'politics'
    query_body = {
        'query': {
            'bool': {
                'must': [
                    {'term': {'area': area}},
                    {'term': {'topic': topic}}
                ]
            }
        },
        'size': 10000
    }
    results = es.search(index=index_name, doc_type=index_type, body=query_body)['hits']['hits']
    item_set = []
    for item in results:
        item_set.append(item['_source'])
    return json.dumps(item_set)

# @mod.route('/search/')
# def es_search():
#     search_template = 'search_list.html'
#     item_content = []
#     item_head = []
#     fuzz_item = ['uid', 'nick_name', 'real_name', 'user_location']
#     range_item = ['statusnum', 'fansnum', 'friendsnum']
#     select_item = ['sex', 'tn', 'sp_type']
#     data = {}
#     query = []
#     num = 0
#     order = []
#     data['uid'] = request.args.get('q1')
#     data['nick_name'] = request.args.get('q2')
#     data['rel_name'] = request.args.get('q3')
#     data['sp_type'] = request.args.get('q4')
#     data['isreal'] = request.args.get('tn')
#     data['sex'] = request.args.get('sex')
#     data['email'] = request.args.get('q7') 
#     data['user_location'] = request.args.get('q12')
#     rank_order = request.args.get('order')
#     size = 100
#     for key in range_item:
#         data[key] = {}
#     data['statusnum']['from'] = '0'
#     data['statusnum']['to'] = '100000000'
#     data['fansnum']['from'] = '0'
#     data['fansnum']['to'] = '100000000'
#     data['friendsnum']['from'] = '0'
#     data['friendsnum']['to'] = '100000000'
#     data['statusnum']['from'] = request.args.get('q5')
#     data['statusnum']['to'] = request.args.get('q6')
#     data['fansnum']['from'] = request.args.get('q8')
#     data['fansnum']['to'] = request.args.get('q9')
#     data['friendsnum']['from'] = request.args.get('q10')
#     data['friendsnum']['to'] = request.args.get('q11')
#     size = request.args.get('size')
#     for key in range_item:
#         if data[key]['from'] == '' and data[key]['to'] != '':
#             data[key]['from'] = '0'
#         if data[key]['from'] != '' and data[key]['to'] == '':
#             data[key]['to'] = '100000000'
#     if rank_order == "0":
#         order = [{'statusnum':{'order':'desc'}}]
#         num += 1
#     if rank_order == "1":
#         order = [{'fansnum':{'order':'desc'}}]
#         num += 1
#     if rank_order == "2":
#         order = [{'friendsnum':{'order':'desc'}}]
#         num += 1

#     if data['isreal'] == '2':
#         data['isreal'] = ''
#     if data['sex'] == '0':
#         data['sex'] = ''
#     if data['sp_type'] == '0':
#         data['sp_type'] = ''
#     for key in data:
#         if data[key] and key not in range_item:
#             if key in fuzz_item:
#                 query.append({'wildcard':{key : "*" + data[key] + '*'}})
#                 num += 1
#             if key in select_item :
#                 if data[key]:
#                     query.append({'match':{key : data[key]}})
#                     num += 1
#         elif data[key]:
#             if data[key]['from'] and data[key]['to']:
#                 query.append({'range':{key:{"from":data[key]['from'],"to":data[key]['to']}}})
#                 num += 1
#                 print data[key]['to']

#     if num > 0:
#         try:
#             source = es.search(
#                 index = 'weibo_user',
#                 doc_type = 'user',
#                 body = {
#                     'query':{
#                         'bool':{
#                             'must':query
#                         }
#                     },
#                     "sort":order,
#                     "size" : size
#                     }
#             )
#         except Exception as e:
#             # TODO handle exception
#             raise e 
#     else:
#         source = es.search(
#             index = 'weibo_user',
#             doc_type = 'user',
#             body = {
#                 'query':{'match_all':{}
#             },
#                 "sort":[{'statusnum':{'order':'desc'}}],
#                 "size" : 100
#                 }
#         )
#     return render_template(search_template, source=source)

