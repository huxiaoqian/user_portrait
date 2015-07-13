# -*- coding: utf-8 -*-

"""
compare user' influence between different days

"""

import sys
from elasticsearch import Elasticsearch

reload(sys)
sys.path.append("./../../")
from global_utils import ES_CLUSTER_FLOW1

es = ES_CLUSTER_FLOW1
former_index = "20130901"
later_index = "20130902"

def rank_change(index_name, doctype):
    query_body={
        "query": {
            "match_all": {}
            },
        "sort": [{"user_index": {"order": "desc"}}],
        "size": 10000
    }


    result = es.search(index=index_name, doc_type=doctype, body=query_body)['hits']['hits']
    uid_set = set()
    for item in result:
        uid_set.add(item["_id"])

    return uid_set

def expand_update_action(data):
    _id = data['uid']
    action = {'index': {'_id': _id}}
    return action, data

if __name__ == "__main__":

    set_1 = rank_change("20130901", "bci")
    set_2 = rank_change("20130902", "bci")

    common_set = set_1.intersection(set_2) # intersection
    difference_set_12 = set_1.difference(set_2) # 1 - 2
    difference_set_21 = set_2.difference(set_1) # 2 - 1

    # obtain common user's rank
    former_index_common = es.mget(index=former_index, doc_type="bci", body={"ids":list(common_set)}, _source=False, fields=["rank"])["docs"]
    former_index_common_dict = {}
    for item in former_index_common:
        former_index_common_dict[item['_id']] = item['fields']['rank'][0]

    later_index_common = es.mget(index=later_index, doc_type="bci", body={"ids":list(common_set)}, _source=False, fields=["rank"])["docs"]
    later_index_common_dict = {}
    for item in later_index_common:
        later_index_common_dict[item['_id']] = item['fields']['rank'][0]

    for each in list(common_set):
        rank_info = {}
        rank_info['uid'] = each
        rank_info['vary'] = later_index_common_dict[each] - former_index_common_dict[each]
        print rank_info
        sys.exit(0)


