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

es = ES_CLUSTER_FLOW1
recommend_redis = R_RECOMMENTATION_OUT

index_destination = "user_index_profile"
index_destination_doctype = "manage"
# index_destination = "user_portrait"
# index_destination_doctype = "user"

def transfer_str_to_list(value):
    uid_list = []
    temp = value.split(",")
    for item in temp:
        user = item.split("'")[1]
        uid_list.append(user)
    return uid_list

def expand_delete_action(data, index_name=index_destination, doctype=index_destination_doctype):
    action = {"delete": {"_index": index_name, "_type": doctype, "_id": data}}
    return action

def main():
    ts = time.time()

    date = recommend_redis.hgetall("decide_delete_list") # decide to delete uids 
    keys = recommend_redis.hkeys("decide_delete_list")
    print date
    print keys

    if keys == []:
        return None

    bulk_action = []
    count = 0

    for item in keys:
        print item
        time_struct = datetime.date(int(item[0:4]), int(item[4:6]), int(item[6:]))
        item_timestamp = time.mktime(time_struct.timetuple())
        print item_timestamp

        if ts - item_timestamp > 7 * 86400:
        #if ts - item_timestamp > 0:

            temp = recommend_redis.hget("decide_delete_list", item)
            if not temp:
                continue
            temp_list = json.loads(recommend_redis.hget("decide_delete_list", item))
            hdel("decide_delete_list", item)

            if temp_list == []:
                continue

            for uid in temp_list:
                del_data = expand_delete_action(uid)
                bulk_action.append(del_data)
                count += 1
                print bulk_action

                if count % 100 == 0:
                    es.bulk(bulk_action, index=index_destination, doc_type=index_destination_doctype, timeout=30)
                    bulk_action = []

    if bulk_action:
        es.bulk(bulk_action, index=index_destination, doc_type=index_destination_doctype, timeout=30)

if __name__ == "__main__":
    main()
