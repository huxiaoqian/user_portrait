# -*- coding: utf-8 -*-
"""
copy es_portrait to a new es, for the use of record user_index

"""

import sys
import time
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

reload(sys)
sys.path.append('./../../')
from global_utils import ES_CLUSTER_FLOW1, es_user_profile

es = ES_CLUSTER_FLOW1
user_portrait = "20130901" # act as portrait database
user_portrait_doctype = "bci"
index_destination = "test" # act as user active database
index_destination_doctype = "manage"

def expand_index_action(data):
    _id = data['uid']
    action = {'index': {'_id': _id}}
    return action, data


if __name__ == "__main__":

    tb = time.time()

    index_exist = es.indices.exists(index=index_destination)
    if not index_exist:
        es.indices.create(index=index_destination, ignore=400)

    s_re = scan(es, query={"query":{"match_all":{}},"size":1000}, index=user_portrait, doc_type=user_portrait_doctype)
    bulk_action = []
    count = 0
    count_n = 0
    search_list = []
    while 1:
        user_list = []
        while 1:
            try:
                scan_re = s_re.next()['_source']
                count += 1
            except StopIteration:
                print "all done"
                sys.exit(0)
            except Exception, r:
                print Exception, r
                sys.exit(0)

            user_list.append(scan_re)
            if count % 1000 == 0:
                break

        for item in user_list:
            uid = item.get('user', '0') # obtain uid, notice "uid" or "user"
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
            if count_n % 2000 == 0:
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
                print "%s  per  %s  second"  %(count_n, ts-tb)
                tb = ts

    if bulk_action:
        es.bulk(bulk_action, index=index_destination, doc_type=index_destination_doctype, timeout=30)


