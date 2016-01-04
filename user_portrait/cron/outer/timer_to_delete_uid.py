# -*- coding: utf-8 -*-

"""
preset time to delete the users (uid) recommended and stored in redis

"""

import sys
import redis
import time
import json
import datetime
from elasticsearch import Elasticsearch

reload(sys)
sys.path.append('./../../')
from global_utils import R_RECOMMENTATION_OUT, ES_CLUSTER_FLOW1
from global_utils import portrait_index_name, portrait_index_type
from global_utils import copy_portrait_index_name, copy_portrait_index_type
from time_utisl import ts2datetime, datetime2ts

es = ES_CLUSTER_FLOW1
recommend_redis = R_RECOMMENTATION_OUT


def transfer_str_to_list(value):
    uid_list = []
    temp = value.split(",")
    for item in temp:
        user = item.split("'")[1]
        uid_list.append(user)
    return uid_list

def expand_delete_action(data, index_name, doctype):
    action = {"delete": {"_index": index_name, "_type": doctype, "_id": data}}
    return action

def main():
    ts = time.time()

    date = recommend_redis.hgetall("decide_delete_list") # decide to delete uids 
    keys = recommend_redis.hkeys("decide_delete_list") # keys: 2013-09-07
    print date
    print keys

    if keys == []:
        return None

    bulk_action = []
    copy_bulk_action = []
    count = 0

    for item in keys:
        print item
        item_timestamp = datetime2ts(item)
        print item_timestamp

        if ts - item_timestamp >= 7 * 86400:
        #if ts - item_timestamp > 0:

            temp_list = json.loads(recommend_redis.hget("decide_delete_list", item))
            hdel("decide_delete_list", item)
            hdel("history_delete_list", item)

            if temp_list == []:
                continue

            for uid in temp_list:
                del_data = expand_delete_action(uid, portrait_index_name, portrait_index_type)
                copy_del_data = expand_delete_action(uid, copy_portrait_index_name, copy_portrait_index_type)
                bulk_action.append(del_data)
                copy_bulk_action.append(copy_del_data)
                count += 1

                if count % 100 == 0:
                    es.bulk(bulk_action, index=portrait_index_name, doc_type=portrait_index_type, timeout=30)
                    es.bulk(copy_bulk_action, index=copy_portrait_index_name, doc_type=copy_portrait_index_type, timeout=30)
                    bulk_action = []
                    copy_bulk_action = []

    if bulk_action:
        es.bulk(bulk_action, index=portrait_index_name, doc_type=portrait_index_type, timeout=30)
        es.bulk(copy_bulk_action, index=copy_portrait_index_name, doc_type=copy_portrait_index_type, timeout=30)

if __name__ == "__main__":
    main()
