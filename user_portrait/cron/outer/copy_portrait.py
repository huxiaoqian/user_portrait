# -*- coding: utf-8 -*-
"""
定时任务：
    将user_portrait中，未复制到copy_user_portrait的用户复制过来，以作后用
"""

import os
import sys
import time
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

reload(sys)
sys.path.append('./../../')
from global_utils import es_user_portrait as es
from global_utils import es_user_profile
from global_utils import portrait_index_name, portrait_index_type, copy_portrait_index_name, copy_portrait_index_type
user_portrait = portrait_index_name # act as portrait database
user_portrait_doctype = portrait_index_type
index_destination = copy_portrait_index_name
index_destination_doctype = copy_portrait_index_type

def expand_index_action(data):
    _id = data['uid']
    action = {'index': {'_id': _id}}
    return action, data

def co_search(es, user_list, bulk_action, count_n, tb):
    search_list = []
    for item in user_list:
        uid = item.get('uid', '0') # obtain uid, notice "uid" or "user"
        search_list.append(uid)

    search_result = es.mget(index=index_destination, doc_type=index_destination_doctype, body={"ids": search_list}, _source=False)["docs"]
    search_list = []

    for item in search_result:
        if not item['found']:
            user_info = {}
            user_info['uid'] = item['_id']
            user_info['low_number'] = 0
            xdata = expand_index_action(user_info)
            bulk_action.extend([xdata[0], xdata[1]])
            count_n += 1
            if count_n % 1000 == 0:
                while True:
                    try:
                        es.bulk(bulk_action, index=index_destination, doc_type=index_destination_doctype, timeout=30)
                        bulk_action = []
                        break
                    except:
                        es = ES_CLUSTER_FLOW1
                print count_n

            if count_n % 10000 == 0:
                ts = time.time()
                print "count_n %s  per  %s  second"  %(count_n, ts-tb)
                print "count %s " % count
                tb = ts

    return bulk_action, count_n, tb

if __name__ == "__main__":

    # 1. print start info
    tb = time.time()
    current_path = os.getcwd()
    file_path = os.path.join(current_path, 'copy_portrait.py')
    now_ts = ts2datetime(tb)
    print_log = "&".join([file_path, "start", now_ts])
    print print_log #打印开始信息

    index_exist = es.indices.exists(index=index_destination)
    if not index_exist:
        es.indices.create(index=index_destination, ignore=400)

    s_re = scan(es, query={"query":{"match_all":{}},"size":1000}, index=user_portrait, doc_type=user_portrait_doctype)
    bulk_action = []
    count = 0
    count_n = 0
    search_list = []
    user_list = []
    while 1:
        try:
            scan_re = s_re.next()['_source']
            count += 1
            user_list.append(scan_re)
            if count % 1000 == 0:
                bulk_action, count_n, tb = co_search(es, user_list, bulk_action, count_n, tb)
                user_list = []
        except StopIteration:
            print "all done"
            bulk_action, count_n, tb = co_search(es, user_list, bulk_action, count_n,tb)
            break
        except Exception, r:
            print Exception, r
            sys.exit(0)


    if bulk_action:
        es.bulk(bulk_action, index=index_destination, doc_type=index_destination_doctype, timeout=30)

    print count, count_n #数字相等才匹配

    # 2. 打印终止信息
    now_ts = ts2datetime(time.time())
    print_log = "&".join([file_path, "end", now_ts])
    print print_log

