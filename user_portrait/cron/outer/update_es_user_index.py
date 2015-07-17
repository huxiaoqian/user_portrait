# -*- coding: utf-8 -*-

"""
add all user in portrait database and this es is used as all users' activity record
scan the index of everyday active user in profile database and correspondded activity, and default index is 0
record format: {"uid": 1234567890, '20130901': 500', "20130904": 700}

"""

import logging
import sys
import time
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

reload(sys)
sys.path.append('./../../')
from global_utils import ES_CLUSTER_FLOW1

es = ES_CLUSTER_FLOW1
# index_date is everyday index
index_date = "20130906"
index_date_doctype = "bci"
index_destination = "user_index_profile"
index_destination_doctype = "manage"

def expand_update_action(data):
    _id = data['uid']
    action = {'update': {'_id': _id}}
    xdata = {"doc": data}
    return action, xdata


if __name__ == "__main__":

    tb = time.time()

    index_exist = es.indices.exists(index=index_destination)
    if not index_exist:
        es.indices.create(index=index_destination, ignore=400)

    s_re = scan(es, query={"query":{"match_all":{}},"size":1000}, index=index_destination, doc_type=index_destination_doctype)
    bulk_action = []
    count_index = 0
    count_n = 0
    search_list = []
    while 1:
        user_list = []
        while 1:
            try:
                scan_re = s_re.next()['_source']
            except StopIteration:
                print "no user left"
                sys.exit(0)
            except Exception, r:
                print Exception, r
                sys.exit(0)

            user_list.append(scan_re)
            count_n += 1
            if count_n % 1000 == 0:
                break

        for item in user_list:
            uid = item.get('uid', '0')
            search_list.append(uid)

        search_result = es.mget(index=index_date, doc_type=index_date_doctype, body={"ids": search_list}, _source=True)["docs"]


        for item in search_result:
            if not item["found"]:
                index_info = {}
                index_info['uid'] = item["_id"]
                index_number = search_list.index(index_info['uid'])
                index_info[index_date] = 0
                number = user_list[index_number].get("low_number", 0)
                index_info['low_number'] = number + 1
                xdata = expand_update_action(index_info)
                bulk_action.extend([xdata[0], xdata[1]])
                count_index += 1

            else:
                m_item = {}
                m_item['uid'] = item['_id']
                m_item[index_date] = item['_source'].get('user_index', 0)
                index_number = search_list.index(m_item['uid'])
                number = user_list[index_number].get("low_number", 0)
                if m_item[index_date] < 170: # self determined threshould
                    m_item['low_number'] = number + 1
                else:
                    m_item['low_number'] = 0
                xdata = expand_update_action(m_item)
                bulk_action.extend([xdata[0], xdata[1]])
                count_index += 1


            if count_index % 2000 == 0:
                while True:
                    try:
                        es.bulk(bulk_action, index=index_destination, doc_type=index_destination_doctype, timeout=30)
                        bulk_action=[]
                        break
                    except Exception, r:
                        print Exception,":",r
                        es = ES_CLUSTER_FLOW1
                print count_index

            if count_index % 10000 == 0:
                ts = time.time()
                print "%s  per  %s  second"  %(count_index, ts-tb)
                tb = ts

        search_list = []

    if bulk_action:
        es.bulk(bulk_action, index=index_destination, doc_type=index_destination_doctype, timeout=30)



