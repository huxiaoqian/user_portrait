# -*- coding: utf-8 -*-

"""
compare user' influence between different days, and obtain user rank

"""

import sys
from elasticsearch import Elasticsearch

reload(sys)
sys.path.append("./../../")
from global_utils import ES_CLUSTER_FLOW1

es = ES_CLUSTER_FLOW1
vary_index = "vary"
size = 10000

def uid_rank_change(index_name, doctype, size):
    query_body={
        "query": {
            "match_all": {}
            },
        "sort": [{"user_index": {"order": "desc"}}],
        "size": size
    }


    result = es.search(index=index_name, doc_type=doctype, body=query_body)['hits']['hits']
    uid_set = set()
    for item in result:
        uid_set.add(item["_id"])

    return uid_set

def expand_index_action(data):
    _id = data['uid']
    action = {'index': {'_id': _id}}
    return action, data

def bulk_function(es, uid_list, former_index_common_dict, later_index_common_dict, later_index,size=size):
    bulk_action = []
    count_n = 0
    for each in uid_list:
        rank_info = {}
        rank_info['uid'] = each
        rank_info['vary'] = former_index_common_dict.get(each, size) - later_index_common_dict.get(each, size)
        xdata = expand_index_action(rank_info)
        bulk_action.extend([xdata[0], xdata[1]])
        count_n += 1

        if count_n % 2000 == 0:
            es.bulk(bulk_action, index=vary_index, doc_type="bci", timeout=30)
            bulk_action = []
            print count_n
    if bulk_action:
        es.bulk(bulk_action, index=vary_index, doc_type="bci", timeout=30)


def main(former_index="20130902", later_index="20130903", size=10000):

    set_1 = uid_rank_change(former_index, "bci", size)
    set_2 = uid_rank_change(later_index, "bci", size)

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

    bulk_function(es, list(common_set), former_index_common_dict, later_index_common_dict, later_index, size)

    # first day active, but second day no

    former_index_alone = es.mget(index=former_index, doc_type="bci", body={"ids":list(difference_set_12)}, _source=False, fields=["rank"])["docs"]
    former_index_alone_dict = {}
    for item in former_index_alone:
        former_index_alone_dict[item['_id']] = item['fields']['rank'][0]

    bulk_function(es, list(difference_set_12), former_index_alone_dict, {}, later_index, size)

    # first day not active, second day active

    later_index_alone = es.mget(index=later_index,  doc_type="bci", body={"ids":list(difference_set_21)}, _source=False, fields=["rank"])["docs"]
    later_index_alone_dict = {}
    for item in later_index_alone:
        later_index_alone_dict[item['_id']] = item['fields']['rank'][0]

    bulk_function(es, list(difference_set_21), {}, later_index_alone_dict, later_index)


if __name__ == "__main__":
    main()
