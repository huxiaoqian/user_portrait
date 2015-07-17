# -*- coding = utf-8 -*-
import math
import time
import sys
from elasticsearch import Elasticsearch
reload(sys)
sys.path.append('./../../')
from global_utils import ES_CLUSTER_FLOW1

es = ES_CLUSTER_FLOW1
index_name = "20130901"

"""
based on user_index, search users in different range

"""
def query_es(index_name,range_1, range_2, size=0, count=1):
    query_body = {
        "query":{
            "filtered": {
                "query": {
                    "match_all":{}
                },
                "filter": {
                    "range": {
                        "user_index": {
                            "gte": range_1,
                            "lt": range_2
                        }
                    }
                }
            }
        }
    }

    if size != 0:
        query_body["size"] = size

    if count == 0:
        result = es.search(index=index_name, doc_type="bci", body=query_body)['hits']['hits']
    else:
        result = es.count(index=index_name, doc_type="bci", body=query_body)['count']

    return result


def query_brust(index_name,range_1, range_2, count=0):
    query_body = {
        "query":{
            "filtered": {
                "query": {
                    "match_all":{}
                },
                "filter": {
                    "range": {
                        "retweeted_weibo_number": {
                            "gte": range_1,
                            "lt": range_2
                        }
                    }
                }
            }
        }
    }

    if count == 1:
        result = es.count(index=index_name, doc_type="bci", body=query_body)['count']
        return result

    else:
        query_body['size'] = 1000
        result = es.search(index=index_name, doc_type="bci", body=query_body)['hits']['hits']

        profile_list = []
        for item in result:
            profile_list.append(item['_id'])

        return profile_list


def search_top_index(index_name, top_k, index_type="bci"):
    query_body = {
        "query": {
            "match_all": {}
        },
        "size": top_k,
        "sort": [{"user_index": {"order": "desc"}}]
    }

    if top_k == 1:
        result = es.search(index=index_name, doc_type=index_type, body=query_body)['hits']['hits'][0]['_source']['user_index']
    else:
        search_result = es.search(index=index_name, doc_type=index_type, body=query_body)['hits']['hits']
        result = []
        for item in search_result:
            result.append(item['_source']['user_index'])
    return result

"""
based on uid_list, obtain detail active info

"""

def search_influence_detail(uid_list, index_name, doctype):
    result = es.mget(index=index_name, doc_type=doctype, body={"ids": uid_list}, _source=True)["docs"]
    result_dict = {}
    for item in result:
        result_dict[item['_id']] = item['_source']

    return result_dict

"""
search single field max value

"""

def search_max_single_field(field, index_name, doctype, top_k=3):

    # field = "origin_weibo_retweeted_top_number", "origin_weibo_comment_top_number"
    query_body = {
        "query": {
            "match_all": {}
        },
        "sort": [{field: {"order": "desc"}}],
        "size": top_k
    }

    result = es.search(index=index_name, doc_type=doctype, body=query_body, _source=False, \
            fields=["origin_weibo_top_retweeted_id", "origin_weibo_top_comment_id"])['hits']['hits']

    return_dict = {}
    rank = 0

    if field == 'origin_weibo_retweeted_top_number':
        for item in result:
            user_dict = {}
            rank += 1
            user_dict[field] = item['sort'][0]
            user_dict["origin_weibo_top_retweeted_id"] = item['fields']["origin_weibo_top_retweeted_id"][0]
            user_dict['rank'] = rank
            return_dict[item['_id']] = user_dict

    if field == 'origin_weibo_comment_top_number':
        for item in result:
            user_dict = {}
            rank += 1
            user_dict[field] = item['sort'][0]
            user_dict["origin_weibo_top_comment_id"] = item['fields']['origin_weibo_top_comment_id'][0]
            user_dict['rank'] = rank
            return_dict[item['_id']] = user_dict

    return return_dict


if __name__ == "__main__":

    es = ES_CLUSTER_FLOW1

    """
    all_range = []
    distribute_range = []
    top_index = search_top_index("20130901",5)
    print top_index
    max_score = int(math.ceil(top_index/100.0)) * 100

    # devide active user based on active degree


    score_range = [0, 100, 200, 500, 700, 900, 1100, 1300, 1500, max_score]
    for i in range(len(score_range)-1):
        temp_number = query_es(index_name, score_range[i], score_range[i+1])
        all_range.append(temp_number)
    print all_range



    # draw all active user seperately


    index_range = range(0, max_score+100, 100)
    for i in range(len(index_range)-1):
        temp_number = query_es(index_name, index_range[i], index_range[i+1])
        distribute_range.append(temp_number)
    print distribute_range



    # search brust
    ss = range(0,1000,10)
    ss_set = []
    for i in range(len(ss)-1):
        result = query_brust(index_name, ss[i], ss[i+1], count=1)
        ss_set.append(result)
    print ss_set


    uid_list = ['1713926427','2758565493']
    result_dict = search_influence_detail(uid_list, '20130901', 'bci')
    print result_dict

    """

    field_name = "origin_weibo_comment_top_number"
    result = search_max_single_field(field_name, '20130901', 'bci')
    print result


