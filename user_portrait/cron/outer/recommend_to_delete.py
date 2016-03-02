# -*- coding: utf-8 -*-

"""
based on user activity, recommend to delete the user in portrait database

recommend_delete_list:只保留一天记录，因为前一天未出库，又没有操作的用户在第二天还是会被推荐出来
"""

import os
import sys
import time
import json
import redis
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

reload(sys)
sys.path.append('./../../')
from global_utils import R_RECOMMENTATION_OUT as recommend_redis
from global_utils import es_user_portrait as es
from global_utils import copy_portrait_index_name as index_destination
from global_utils import copy_portrait_index_type as index_destination_doctype
from filter_uid import all_delete_uid
from time_utils import ts2datetime, datetime2ts
from parameter import RECOMMEND_OUT_THRESHOULD

threshould = RECOMMEND_OUT_THRESHOULD

def search_low_number(low_range, index_name=index_destination, index_type=index_destination_doctype):
    query_body = {
        "query": {
            "filtered": {
                "query": {
                    "match_all": {}
                 },
                "filter": {
                    "range": {
                        "low_number":{
                            "gt": low_range
                        }
                    }
                }
            }
        },
        "size": 1000
    }

    results = es.search(index=index_name, doc_type=index_type, body=query_body)["hits"]["hits"]

    user_list = []
    if results:
        for item in results:
            user_list.append(item['_id'])

    return user_list


def main():
    filter_uid = all_delete_uid()
    #record_time = time.strftime("%Y%m%d", time.localtime(time.time()))
    record_time = ts2datetime(time.time()) # 2013-09-08
    former_time = ts2datetime(time.time() - 24*3600) # 2013-09-07
    recommend_list = search_low_number(threshould) # recommended user to delete in portrait database
    print len(recommend_list)
    recommend_list = list(set(recommend_list).difference(filter_uid))
    recommend_redis.hset("recommend_delete_list", record_time, json.dumps(recommend_list)) # 今日推荐出库名单
    recommend_redis.hdel("recommend_delete_list", former_time) # 删除昨日推荐名单，只维护一个推荐出库名单

    return 1

if __name__ == "__main__":
    current_path = os.getcwd()
    file_path = os.path.join(current_path, 'recommend_to_delete.py')
    now_ts = ts2datetime(ts)
    print_log = "&".join([file_path, "start", now_ts])
    print print_log #打印开始信息

    main()

    now_ts = ts2datetime(ts)
    print_log = "&".join([file_path, "end", now_ts])
    print print_log # 打印终止信息
