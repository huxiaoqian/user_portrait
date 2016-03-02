# -*- coding: utf-8 -*-

"""
preset time to delete the users (uid) recommended and stored in redis

"""

import os
import sys
import redis
import time
import json
import datetime
from elasticsearch import Elasticsearch

reload(sys)
sys.path.append('./../../')
from global_utils import es_user_portrait as es
from global_utils import R_RECOMMENTATION_OUT as recommend_redis
from global_utils import portrait_index_name, portrait_index_type
from global_utils import copy_portrait_index_name, copy_portrait_index_type
from time_utisl import ts2datetime, datetime2ts

recommend_redis = R_RECOMMENTATION_OUT


def expand_delete_action(data, index_name, doctype):
    action = {"delete": {"_index": index_name, "_type": doctype, "_id": data}}
    return action

def main():
    ts = time.time()

    bulk_action = []
    copy_bulk_action = []
    count = 0

    delete_key = ts2datetime(ts - 7*86400) # 每天删除7天前的数据
    temp_list = recommend_redis.hget("decide_delete_list", item)
    if temp_list:
        delete_list = json.loads(temp_list) # 待删除的用户列表
        hdel("decide_delete_list", item)

        for uid in delete_list:
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
    current_path = os.getcwd()
    file_path = os.path.join(current_path, 'timer_to_delete_uid.py')
    now_ts = ts2datetime(ts)
    print_log = "&".join([file_path, "start", now_ts])
    print print_log #打印开始信息

    main()

    now_ts = ts2datetime(ts)
    print_log = "&".join([file_path, "end", now_ts])
    print print_log # 打印终止信息
