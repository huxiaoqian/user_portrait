# -*- coding:utf-8 -*-

import sys
sys.path.append('../../../')
from user_portrait.global_utils import es_user_profile, es_user_portrait

def profile_match(term, value):
    query_body = {
        "query": {
            "match": {
                term: value
            }
        },
        "size": 100000
    }

    # mapping = es_user_profile.indices.analyze(index='weibo_user', body=value)
    # print mapping
    results = es_user_profile.search(index='weibo_user', doc_type='user', body=query_body)['hits']
    count = results['total']
    source = results['hits']
    print term, value, count
    return source

def portrait_match(term, value):
    query_body = {
        "query": {
            "match": {
                term: value
            }
        },
        "size": 100000
    }

    mapping = es_user_portrait.indices.analyze(index='user_portrait', body=value)
    print mapping
    results = es_user_portrait.search(index='user_portrait', doc_type='user', body=query_body)['hits']
    count = results['total']
    source = results['hits']
    print term, value, count
    return source

def portrait_exist(term):
    query_body = {
        "query": {
            "filtered":{
                "filter":{
                    "exists": {
                        "field": term
                    }
                }
            }
        },
        "size": 100000
    }

    results = es_user_portrait.search(index='user_portrait', doc_type='user', body=query_body)['hits']
    count = results['total']
    source = results['hits']
    print term, count

