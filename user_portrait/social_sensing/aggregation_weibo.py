# -*- coding:utf-8 -*-


import sys
import time
import json
from elasticsearch import Elasticsearch
reload(sys)
sys.path.append("./../")
from global_utils import es_flow_text as es_text
from global_utils import es_user_profile as es_profile
from global_utils import es_user_portrait
from time_utils import ts2datetime, datetime2ts
from global_utils import flow_text_index_name_pre, flow_text_index_type, profile_index_name, profile_index_type, \
                         portrait_index_name, portrait_index_type
from parameter import SOCIAL_SENSOR_TIME_INTERVAL as time_interval
from parameter import SOCIAL_SENSOR_FORWARD_RANGE as forward_time_range

# aggragate weibo keywords of timestamp ts1 and ts2
def aggregation_range(ts1, ts2): 
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "range":{
                        "timestamp":{
                            "gte": ts1,
                            "lt": ts2
                        }
                    }
                }
            }
        },
        "aggs":{
            "all_interests":{
                "terms": {"field": "keywords_string",
                          "size": 100
                }
            }
        }
    }

    return query_body

# aggregate sentiment with a specified keyword or keywords----list
# 在给定关键词时，聚合某段时间内相关微博的关键词、情绪
def aggregation_sentiment(ts1, ts2, keyword_list, aggregation_word, size=10):
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[{
                            "range":{
                                "timestamp":{
                                    "gte": ts1,
                                    "lt": ts2
                                }
                            }},
                            {"terms":{
                                "keywords_string": keyword_list
                            }
                        }]
                    }
                }
            }
        },
        "aggs":{
            "all_sentiment":{
                "terms":{"field": aggregation_word, "size": size}
            }
        }
    }

    return query_body


#聚合一段时间内特定社会传感器的微博的关键词/情绪
def aggregation_sensor_keywords(ts1, ts2, uid_list, aggregation_word, size=10):
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[{
                            "range":{
                                "timestamp":{
                                    "gte": ts1,
                                    "lt": ts2
                                }
                            }}
                        ],
                        "should":[
                        ]
                    }
                }
            }
        },
        "aggs":{
            "all_keywords":{
                "terms":{ "field": aggregation_word, "size": size}
            }
        }
    }

    if len(uid_list) == 0:
        pass
    elif len(uid_list) == 1:
        query_body["query"]["filtered"]["filter"]["bool"]["must"].append({"term": {"uid": uid_list[0]}})
    else:
        for iter_uid in uid_list:
            query_body["query"]["filtered"]["filter"]["bool"]["should"].append({"term": {"uid": iter_uid}})

    return query_body


def temporal_keywords(ts1, ts2):
    keywords_set = set()
    date = ts2datetime(time.time())
    date = "2013-09-07"
    index_date = flow_text_index_name_pre + date
    #search_results = es_text.search(index=index_date, doc_type=flow_text_index_type, body=aggregation_range(ts1, ts2))['aggregations']['all_interests']['buckets']
    search_results = es_text.search(index=index_date, doc_type=flow_text_index_type, body=aggregation_sentiment(ts1, ts2, ["舟曲", "泥石流"], "keywords_string", 20))['aggregations']['all_sentiment']['buckets']

    # print keywords
    for item in search_results:
        print item["key"].encode("utf-8", "ignore"), item["doc_count"], "\n"
        #keywords_set.add(item["key"].encode("utf-8", "ignore"))

    return keywords_set



# 事件检测中用于查询给定关键词，在某段时间内的原创微博列表

def query_mid_list(ts, keywords_list, time_segment):
    # 第一步，聚合前六个小时相关微博mid, 首先获得原创微博
    #ts = time.time()
    #ts = 1377964800+3600
    query_body = {
        "query": {
            "filtered": {
                "filter": {
                    "bool": {
                        "must": [
                            {"range": {
                                "timestamp": {
                                    "gte": ts - time_segment,
                                    "lt": ts
                                }
                            }},
                            {"terms": {"keywords_string": keywords_list}},
                            {"term": {"message_type": 1}} # origin weibo
                        ]
                    }
                }
            }
        },
        "sort": {"sentiment": {"order": "desc"}},
        "size": 10000
    }

    datetime = ts2datetime(ts)
    # test
    #datetime = "2013-09-07"
    index_name = flow_text_index_name_pre + datetime
    exist_es = es_text.indices.exists(index_name)
    if exist_es:
        search_results = es_text.search(index=index_name, doc_type=flow_text_index_type, body=query_body, _source=False)["hits"]["hits"]
    else:
        search_results = []
    origin_mid_list = [] # all related weibo mid list
    if search_results:
        for item in search_results:
            origin_mid_list.append(item["_id"])

    datetime_1 = ts2datetime(ts-time_segment)
    index_name_1 = flow_text_index_name_pre + datetime_1
    exist_bool = es_text.indices.exists(index_name_1)
    if datetime != datetime_1 and exist_bool:
        search_results_1 = es_text.search(index=index_name_1, doc_type=flow_text_index_type, body=query_body, _source=False)["hits"]["hits"]
        if search_results_1:
            for item in search_results_1:
                origin_mid_list.append(item["_id"])

    return origin_mid_list



def query_related_weibo(ts, origin_mid_list, time_segment):
    query_all_body = {
        "query": {
            "filtered": {
                "filter": {
                    "bool": {
                        "must": [
                            {"range": {
                                "timestamp":{
                                    "gte": ts - time_segment,
                                    "lt": ts
                                }
                            }}
                        ]
                    }
                }
            }
        }
    }

    datetime = ts2datetime(ts)
    # test
    #datetime = "2013-09-07"
    index_name = flow_text_index_name_pre + datetime
    exist_es = es_text.indices.exists(index_name)
    if origin_mid_list and exist_es:
        query_all_body["query"]["filtered"]["filter"]["bool"]["must"].append({"terms": {"root_mid": origin_mid_list}})
        repost_count = es_text.count(index=index_name, doc_type=flow_text_index_type, body=query_all_body)["count"]
    else:
        repost_count = 0

    datetime_1 = ts2datetime(ts-time_segment)
    index_name_1 = flow_text_index_name_pre + datetime_1
    exist_bool = es_text.indices.exists(index_name_1)
    if datetime != datetime_1 and exist_bool:
        repost_count_1 = 0
        if origin_mid_list:
            query_all_body["query"]["filtered"]["filter"]["bool"]["must"].append({"terms": {"root_mid": origin_mid_list}})
            repost_count_1 = es_text.count(index=index_name_1, doc_type=flow_text_index_type, body=query_all_body)["count"]
        repost_count += repost_count_1

    total_count = len(origin_mid_list) + repost_count

    return total_count



# event detection
# 给定某个关键词，首先聚合出前6个小时内的平均微博量，再计算当前时间片段内的微博量
# 以两个的比值大小决定是不是有事件爆发
# keywords_list---关键词列表, ts--当前时间, time_segment---时间区间长度
def burst_detection(keywords_list, ts):
    # 前一段时间内原创微博列表
    n_range = forward_time_range/time_interval
    forward_origin_weibo_list = query_mid_list(ts-time_interval, keywords_list, forward_time_range)
    forward_total_count = query_related_weibo(ts-time_interval, forward_origin_weibo_list, forward_time_range)
    #print "forward origin weibo: ", len(forward_origin_weibo_list)
    #print "forward total count: ", forward_total_count
    forward_average_count = forward_total_count/n_range
    #print "forward average count: ", forward_average_count


    current_mid_list = query_mid_list(ts, keywords_list, time_interval)
    #print "current weibo list :", len(current_mid_list)
    all_mid_list = []
    all_mid_list.extend(current_mid_list)
    all_mid_list.extend(forward_origin_weibo_list)
    current_total_count = query_related_weibo(ts, all_mid_list, time_interval)
    # 额外计算了前6个小时原创微博数的量值，需要修正
    current_total_count -= len(forward_origin_weibo_list)
    #print "now total count :", current_total_count
    try:
        ratio = float(current_total_count)/forward_average_count
    except:
        ratio = 0
    return current_total_count, forward_average_count, ratio

if __name__ == "__main__":

    temporal_keywords(1378557829, 1378557829+10000)
    """
    ts2 = datetime2ts("2013-09-08")
    ts1 = datetime2ts("2013-09-01")
    ts = ts1
    while ts < ts2:
        current_total_count, forward_average_count, ratio = burst_detection(["洪水", "洪灾"], ts)
        if current_total_count > 100 and ratio > 3:
            index_date = flow_text_index_name_pre + ts2datetime(ts)
            search_results = es_text.search(index=index_date, doc_type=flow_text_index_type, body=aggregation_sentiment(ts-time_interval, ts, ["洪水", "洪灾"], "keywords_string", 20))['aggregations']['all_sentiment']['buckets']
            print search_results
        ts += time_interval
    """
