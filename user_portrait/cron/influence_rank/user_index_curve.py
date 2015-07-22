# -*- coding: utf-8 -*-

"""
return a period of index of an active user

"""


import sys
import time
import datetime
from elasticsearch import Elasticsearch

reload(sys)
sys.path.append('./../../')
from global_utils import ES_CLUSTER_FLOW1

es = ES_CLUSTER_FLOW1
index_name = 'user_index'

def get_index_curve(uid):
    result = es.get(index=index_name, doc_type='manage', id=uid, _source=True)['_source']
    result.pop('uid')
    result.pop('low_number')
    return result

def all_index_curve(index_curve, start_date, stop_date):
    """
    return all time index data, set default to 0
    format : start_date = 2013/09/01,
             stop_date = 2013/09/10

    """
    iter_keys = []
    start = start_date.split('/')
    stop = stop_date.split('/')
    start_struct = datetime.date(int(start[0]), int(start[1]), int(start[2]))
    stop_struct = datetime.date(int(stop[0]), int(stop[1]), int(stop[2]))
    start_timestamp = time.mktime(start_struct.timetuple())
    stop_timestamp = time.mktime(stop_struct.timetuple())
    print start_timestamp
    print stop_timestamp

    if stop_timestamp > time.time():
        stop_timestamp = time.time()

    if start_timestamp > stop_timestamp:
        return "time error"

    next_timestamp = start_timestamp
    while 1:
        next_timestamp += 86400
        if next_timestamp <= stop_timestamp:
            iter_keys.append(time.strftime('%Y%m%d',time.localtime(next_timestamp)))
        else:
            break

    iter_keys = set(iter_keys)
    keys = index_curve.keys()
    for key in keys:
        if key in iter_keys:
            iter_keys.pop(key)

    for key in iter_keys:
        index_curve[key] = 0

    """
    # return list which contains sorted tuple

    index_curve = sorted(index_curve.iteritems(), key=lambda asd:asd[0], reverse=False) 
    return index_curve
    """

    result = {}
    for item in index_curve:
        result[item[0]] = item[1]

    return result



if __name__ == "__main__":
    uid = '2809342322'
    index_curve =  get_index_curve(uid)
    print all_index_curve(index_curve, '2015/09/01', '2015/09/04')

