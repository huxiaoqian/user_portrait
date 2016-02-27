# -*- coding: utf-8 -*-

"""
destination index has stored all users in user_portrait, 
scan the index of everyday active user in profile database and correspondded activity, and default index is 0
record format: {"uid": 1234567890, '20130901': 500', "20130904": 700}

"""

import logging
import sys
import datetime
import time
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

reload(sys)
sys.path.append('./../../')
from global_utils import ES_CLUSTER_FLOW1

es = ES_CLUSTER_FLOW1
# index_date is everyday active index
index_date = "20130907"
index_date_doctype = "bci"
index_destination = "copy_user_portrait" # record all active user index on the Internet
index_destination_doctype = "user"

#index_destination = "this_is_a_copy_user_portrait" # record only portrait user index
#index_destination_doctype = "manage"

def expand_index_action(data):
    _id = data['uid']
    action = {'index': {'_id': _id}}
    return action, data

def delete_former_field(active_info, index_date):
    time_struct = datetime.date(int(index_date[0:4]), int(index_date[4:6]), int(index_date[6:]))
    timestamp = time.mktime(time_struct.timetuple())
    former_field = time.strftime("%Y%m%d", time.localtime(timestamp-7*86400))
    active_info.pop(former_field, 0)

    return active_info

def co_search(es, user_list, bulk_action, count_index, tb):
    search_list = []
    for item in user_list:
        uid = item.get('uid', '0')
        search_list.append(uid)

    search_result = es.mget(index=index_date, doc_type=index_date_doctype, body={"ids": search_list}, _source=True)["docs"]

    for item in search_result:
        index_number = search_result.index(item)
        index_info = {}
        index_info = user_list[index_number]
        if not item["found"]:
            index_info[index_date] = 0
            number = index_info.get("low_number", 0)
            index_info['low_number'] = number + 1
            index_info = delete_former_field(index_info, index_date)
            xdata = expand_index_action(index_info)
            bulk_action.extend([xdata[0], xdata[1]])
            count_index += 1

        else:
            index_info[index_date] = item['_source'].get('user_index', 0)
            number = user_list[index_number].get("low_number", 0)
            if index_info[index_date] < 170: # self determined threshould
                index_info['low_number'] = number + 1
            else:
                index_info['low_number'] = 0
            index_info = delete_former_field(index_info, index_date)
            xdata = expand_index_action(index_info)
            bulk_action.extend([xdata[0], xdata[1]])
            count_index += 1


        if count_index % 2000 == 0:
            t1 = time.time()
            print "%s"  %t1
            es.bulk(bulk_action, index=index_destination, doc_type=index_destination_doctype, timeout=30)
            bulk_action=[]
            t2 = time.time()
            print "%s"  %(t2-t1)
            print count_index
            print search_list[1]

        if count_index % 10000 == 0:
            ts = time.time()
            print "count_index %s per  %s  second"  %(count_index, ts-tb)
            tb = ts

    return bulk_action, count_index, tb

def main(index_date, index_date_doctype, index_destination, index_destination_doctype):

    tb = time.time()
    es = ES_CLUSTER_FLOW1

    index_exist = es.indices.exists(index=index_destination)
    if not index_exist:
        es.indices.create(index=index_destination, ignore=400)

    t1 = time.time()
    s_re = scan(es, query={"query":{"match_all":{}},"size":1000}, index=index_destination, doc_type=index_destination_doctype)
    bulk_action = []
    count_index = 0
    count_n = 0
    search_list = []
    user_list = []
    while 1:
        try:
            scan_re = s_re.next()['_source']
            user_list.append(scan_re)
            count_n += 1
            if count_n % 2000 == 0:
                bulk_action, count_index, tb = co_search(es, user_list, bulk_action, count_index, tb)
                user_list = []
        except StopIteration:
            print "all done"
            bulk_action, count_index, tb = co_search(es, user_list, bulk_action, count_index, tb)
            break
        except Exception, r:
            print Exception, r
            sys.exit(0)


    if bulk_action:
        es.bulk(bulk_action, index=index_destination, doc_type=index_destination_doctype, timeout=30)

    print count_n
    print count_index


if __name__ == "__main__":
    # index_date = time.strftime("%Y%m%d", time.localtime(time.time()-86400))
    main(index_date, index_date_doctype, index_destination, index_destination_doctype)
