# -*- coding: UTF-8 -*-
import json
import time
import sys
sys.path.append('../../')
from datetime import date, timedelta
from elasticsearch import Elasticsearch
from user_portrait.global_utils import R_RECOMMENTATION, es_user_portrait
from user_portrait.time_utils import datetime2ts

es = es_user_portrait
index_type = 'user'
index_name = "user_portrait"

r_cluster = R_RECOMMENTATION
hash_name = 'compute'


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
            "topic": json.dumps({"教育": 1,"科技":1}),
            "domain": "教育 科技",
            "psycho_feature": "featurefeaturefeature",
            "psycho_status": "statusstatusstatus",
            "text_len": 10,
            "emoticon": json.dumps({"key":"hahaha"}),
            "hashtag": json.dumps({"key":"hahaha"}),
            "emotion_words": json.dumps({"key": "hahaha"}),
            "link": 10,
            "online_pattern": json.dumps({"key": "hahaha"}),
            "activity_location": "beijing",
            "keywords":json.dumps({"key":"hahaha"})
        }
        action = expand_index_action(item)
        bulk_action.extend([action, item])
    for i in range(10):
        item = {
            "uid": 10*str(i),
            "uname": "testname",
            "topic": json.dumps({"政治": 1,"科技": 1}),
            "domain": "政治 科技",
            "psycho_feature": "featurefeaturefeature",
            "psycho_status": "statusstatusstatus",
            "text_len": 10,
            "emoticon": json.dumps({"key":"hahaha"}),
            "hashtag": json.dumps({"key":"hahaha"}),
            "emotion_words": json.dumps({"key": "hahaha"}),
            "link": 10,
            "online_pattern": json.dumps({"key": "hahaha"}),
            "activity_location": "beijing",
            "keywords":json.dumps({"key":"hahaha"})
        }
        action = expand_index_action(item)
        bulk_action.extend([action, item])

    es.bulk(bulk_action, index=index_name, doc_type=index_type)

def start_cal(uid_list):

    if uid_list == True: # calculation all uids
        uid_list = r_cluster.hkeys(hash_name)

    # update redis, change status from 0 to 1
    status = 1
    for uid in uid_list:
        value_string = json.loads(r_cluster.hget(hash_name, uid))
        value_string[1] = status #change status from 0 to 1
        r_cluster.hset(hash_name, uid, json.dumps(value_string))
        print value_string[0], value_string[1]
    """
    # calculation starts, return 'success'
    signal = calculation(uid_list)
    if signal == 'success':
        # delete 
        for uid in uid_list:
            r_cluster.hdel(hash_name, uid)
        print 'success'
    """

# just for test
def reset_redis(uid_list):
    test_date = '2013-09-01'
    status = 0
    for uid in uid_list:
        value_string = [test_date, status]
        r_cluster.hset(hash_name, uid, json.dumps(value_string))

def auto_cal():
    # monitor time
    uid_list = []
    today = date.today()
    delta = timedelta(days = 7) # without updates over a week
    print 'today', today

    results_dict = r_cluster.hgetall(hash_name)
    for uid in results_dict:
        result = json.loads(results_dict[uid])
        in_date = date.fromtimestamp(datetime2ts(result[0]))
        if (today - in_date) > delta:
            uid_list.append(uid)
    start_cal(uid_list)

    # monitor length
    limit = 10000
    count = r_cluster.hlen(hash_name)
    print 'count',count
    if count > limit:
        start_cal(True)


# link to yuanshi
def calculation(uids):
    return 'success'

def test(uid_list):
    es_create()
    # reset_redis(uid_list)
    # auto_cal()
    # start_cal(uid_list)

if __name__=='__main__':
    # test 
    test_uid_list = ['2101413011','1995786393','2132734472','2776631980','2128524603',\
                     '1792702427','2703153040','2787852095','1599102507','1726544024']
    test(test_uid_list)

