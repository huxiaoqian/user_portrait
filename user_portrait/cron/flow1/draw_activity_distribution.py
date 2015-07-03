# -*- coding = utf-8 -*-
import math
import time
from elasticsearch import Elasticsearch

def query_es(index_name,range_1, range_2):
    query_body = {
        "query":{
            "filtered": {
                "query": {
                    "match_all":{}
                },
                "filter": {
                    "range": {
                        "index": {
                            "gte": range_1,
                            "lt": range_2
                        }
                    }
                }
            }
        }
    }
    result = es.count(index=index_name, doc_type="bci", body=query_body)['count']
    
    return result


def query_brust(index_name,range_1, range_2):
    query_body = {
        "query":{
            "filtered": {
                "query": {
                    "match_all":{}
                },
                "filter": {
                    "range": {
                        "origin_weibo_retweeted_brust": {
                            "gte": range_1,
                            "lt": range_2
                        }
                    }
                }
            }
        }
    }

    result = es.count(index=index_name, doc_type="bci", body=query_body)['count']
    
    return result


def search_top_index(k, index_name, index_type="bci"):
    query_body = {
        "query": {
            "match_all": {}
        },
        "size": k,
        "sort": [{"index": {"order": "desc"}}]
    }
    result = es.search(index=index_name, doc_type=index_type, body=query_body)['hits']['hits'][0]['_source']['index']
    return result

if __name__ == "__main__":
    es = Elasticsearch("219.224.135.93")
    all_range = []
    top_index = search_top_k(1,"20130901")
    total_range = int(math.ceil(top_index/100.0))
    for i in range(total_range):
        temp_number = query_es("20130901",i*100,(i+1)*100)
        all_range.append(temp_number)
    print all_range


