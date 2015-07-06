# -*- coding: UTF-8 -*-
import json
import time
from elasticsearch import Elasticsearch

es = Elasticsearch('219.224.135.93', timeout = 60)
index_type = 'user'
index_name = "user_portrait"

def expand_index_action(data):
    _id = data['uid']
    action = {"index": {"_id": _id}}
    return action

def es_create():
    es.indices.delete(index=index_name)
    # print es.nodes.info("node_id=all")
    # print es.cluster.health()
    flag = es.indices.exists(index=index_name)
    if not flag:
        es.indices.create(index=index_name, ignore=400)

    bulk_action = []
    for i in range(10):
        item = {
            "uid": 5*str(i),
            "uname": "testname",
            "topic": "education",
            "area": "education",
            "psycho_feature": "featurefeaturefeature",
            "psycho_status": "statusstatusstatus"
        }
        action = expand_index_action(item)
        bulk_action.extend([action, item])
    for i in range(10):
        item = {
            "uid": 10*str(i),
            "uname": "testname",
            "topic": "politics",
            "area": "politics",
            "psycho_feature": "featurefeaturefeature",
            "psycho_status": "statusstatusstatus"
        }
        action = expand_index_action(item)
        bulk_action.extend([action, item])

    es.bulk(bulk_action, index=index_name, doc_type=index_type)

def test():
    # es_create()
    return

if __name__=='__main__':
    # test 
    test()
