# -*- coding = utf-8 -*-
import math
import time
import sys
from elasticsearch import Elasticsearch
reload(sys)
sys.path.append('./../../')
from global_utils import ES_CLUSTER_FLOW1

es = ES_CLUSTER_FLOW1
index_name = "20150605_top_10000"

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


def search_top_index(index_name, index_type="bci"):
    query_body = {
        "query": {
            "match_all": {}
        },
        "size": 1,
        "sort": [{"user_index": {"order": "desc"}}]
    }
    result = es.search(index=index_name, doc_type=index_type, body=query_body)['hits']['hits'][0]['_source']['user_index']
    return result

if __name__ == "__main__":

    es = ES_CLUSTER_FLOW1

    """
    all_range = []
    distribute_range = []
    top_index = search_top_index("20130901")
    max_score = int(math.ceil(top_index/100.0)) * 100

    devide active user based on active degree


    score_range = [0, 100, 200, 500, 700, 900, 1100, 1300, 1500, max_score]
    for i in range(len(score_range)-1):
        temp_number = query_es(index_name, score_range[i], score_range[i+1])
        all_range.append(temp_number)
    print all_range



    draw all active user seperately


    index_range = range(0, max_score+100, 100)
    for i in range(len(index_range)-1):
        temp_number = query_es(index_name, index_range[i], index_range[i+1])
        distribute_range.append(temp_number)
    print distribute_range

    """


    # search brust
    ss = range(0,1000,10)
    ss_set = []
    for i in range(len(ss)-1):
        result = query_brust(index_name, ss[i], ss[i+1], count=1)
        ss_set.append(result)
    print ss_set
