# -*- coding:utf-8 -*-
import json
import time
from elasticsearch import Elasticsearch
from flask import Blueprint, redirect
from process import es_create

mod = Blueprint('manage', __name__, url_prefix='/manage')

es = Elasticsearch('219.224.135.93', timeout = 60)
index_type = 'user'
index_name = "user_portrait"

es_create() # init data

@mod.route('/list/')
def user_list():
    query_body = {
        'query':{
            'match_all': {}
        },
        'size': 10000
    }
    results = es.search(index=index_name, doc_type=index_type, body=query_body)['hits']['hits']
    item_set = []
    for item in results:
        item_set.append(item['_source'])
    return json.dumps(item_set)

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

