# -*- coding: utf-8 -*-

import sys
import json
from elasticsearch import Elasticsearch

reload(sys)
sys.path.append('./../')
from global_utils import ES_CLUSTER_FLOW1 as es

def query_es(es, index_name, doctype):
    query_body = {
        'query':{
            'bool':{
                'must':[
                    {
                        'match':{
                            'uname':{
                                'query':'中国',
                                'boost':2
                            }
                        }
                    },
                    {
                        'match':{
                            'topic':'education'
                        }
                    }
                ]
            }
        }
    }

    result = es.search(index=index_name, doc_type=doctype, body=query_body)['hits']['hits']

    uid_list = []
    for item in result:
        info = {}
        info['uid'] = item['_id']
        info['score'] = item['_score']
        uid_list.append(info)

    return uid_list

def constant_score(es, index_name, doctype):
    query_body = {
        'query':{
            'bool':{
                'must':[
                    {'constant_score':{
                        'query':{'match':{'topic':'education'}}
                    }},
                    {'constant_score':{
#                        'boost': 2,
                        'query': {'match':{'uname':u'中国'}}
                    }}
                ]
            }
        }
    }

    result = es.search(index=index_name, doc_type=doctype, body=query_body)['hits']['hits']
    uid_list = []
    for item in result:
        info = {}
        info['uid'] = item['_id']
        info['score'] = item['_score']
        uid_list.append(info)
    return uid_list

if __name__ == '__main__':

    w = query_es(es, 'user_portrait', 'user')
    print w 
    print len(w)
#    print constant_score(es, 'user_portrait', 'user')
