# -*- coding: utf-8 -*-

"""
this procedure use the elasticsearch with single search, which the effiency
is not comparable to multi-get, so it's worth your attention

"""
import logging
from timeit import Timer
import time
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

es = Elasticsearch("219.224.135.93")
index_date = "20130902"

def expand_index_action(data):
    _id = data['uid']
    action = {'index': {'_id': _id}}
    return action, data

def compare_activity(new_item, old_item):
    update_item={}
    average_index = (old_item['max_index'] + old_item['min_index'])/2.0
    if new_item['user_index'] < average_index:
        update_item['lower_than_average_number'] = old_item['lower_than_average_number'] + 1
    else:
        update_item['lower_than_average_number'] = old_item['lower_than_average_number']
    if update_item['lower_than_average_number'] > 4:
        update_item['remove'] = 1 # remove
    else:
        update_item['remove'] = 0

    update_item['uid'] = old_item['uid']
    update_item['max_index'] = max(new_item['user_index'], old_item['max_index'])
    update_item['min_index'] = min(new_item['user_index'], old_item['min_index'])
    update_item['index_number'] = old_item['index_number'] + 1

    return update_item

def test_speed(es, count, bulk_data):
    while 1:
        try:
            es.bulk(bulk_data, index="activity", doc_type="manage", timeout=30)
            break
        except Exception, r:
            print Exception,":",r
            es = Elasticsearch("219.224.135.93")
            print "retry"
    print count


if __name__ == "__main__":

    tb = time.time()

    es_logger = logging.getLogger("elasticsearch")
    es_logger.setLevel(logging.ERROR)
    FileHandler = logging.FileHandler("es.log")
    formatter = logging.Formatter("%(asctime)s_%(name)s_%(levelname)s_%(message)s")
    FileHandler.setFormatter(formatter)
    es_logger.addHandler(FileHandler)

    try:
        index_exist = es.indices.exists(index="activity")
        if not index_exist:
            es.indices.create(index="activity", ignore=400)
    except Exception,r:
        print Exception,":",r

    s_re = scan(es, query={"query":{"match_all":{}},"size":1000}, index="20130901",doc_type='bci')
    bulk_action = [] # new uid record to es
    count_index = 0
    while 1:
        try:
            item = s_re.next()['_source']
        except:
            break
        user_id = item['user']
        doc_exist = es.exists(index="activity", id=user_id)
        if not doc_exist:
            activity_info = {}
            activity_info['uid'] = user_id
            activity_info['max_index'] = item['user_index']
            activity_info['min_index'] = item['user_index']
            activity_info['index_number'] = 1
            activity_info['lower_than_average_number'] = 0
            activity_info['remove'] = 0 # 0 denotes not remove
            xdata = expand_index_action(activity_info)
            bulk_action.extend([xdata[0], xdata[1]])
            count_index += 1
            if count_index % 2000 == 0:
                test_speed(es, count_index, bulk_action)
                bulk_action = []

            if count_index % 10000 == 0:
                ts = time.time()
                print "%s  per  %s  second"  %(count_index, ts-tb)
                tb = ts

        else:
            exist_item = es.get(index="activity", doc_type="manage", id=user_id, _source=True)['_source']
            update_item = compare_activity(item, exist_item)
            xdata = expand_index_action(update_item)
            bulk_action.extend([xdata[0], xdata[1]])
            count_index += 1
            if count_index % 2000 == 0:
                test_speed(es, count_index, bulk_action)
                bulk_action = []

            if count_index % 10000 == 0:
                ts = time.time()
                print "%s  per  %s  second"  %(count_index, ts-tb)
                tb = ts

    es.bulk(bulk_action, index="activity", doc_type="manage", timeout=30)





