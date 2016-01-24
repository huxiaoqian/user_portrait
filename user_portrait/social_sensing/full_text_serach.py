# -*- coding:utf-8 -*-

import sys
import time
import json
import numpy as np
from elasticsearch import Elasticsearch

from user_portrait.global_utils import es_flow_text as es_text
from user_portrait.global_utils import es_user_profile as es_profile
from user_portrait.global_utils import es_user_portrait
from user_portrait.global_utils import R_SOCIAL_SENSING as r
from user_portrait.time_utils import ts2datetime, datetime2ts
from user_portrait.global_utils import flow_text_index_name_pre, flow_text_index_type, profile_index_name, profile_index_type, \
                         portrait_index_name, portrait_index_type
from user_portrait.parameter import SOCIAL_SENSOR_TIME_INTERVAL as time_interval
from user_portrait.parameter import SOCIAL_SENSOR_FORWARD_RANGE as forward_time_range
from user_portrait.parameter import DETAIL_SOCIAL_SENSING as index_sensing_task
from user_portrait.parameter import INDEX_MANAGE_SOCIAL_SENSING as index_manage_social_task
from user_portrait.parameter import DOC_TYPE_MANAGE_SOCIAL_SENSING as task_doc_type
from user_portrait.parameter import FORWARD_N as forward_n
from user_portrait.parameter import INITIAL_EXIST_COUNT as initial_count
from user_portrait.parameter import IMPORTANT_USER_NUMBER, IMPORTANT_USER_THRESHOULD, signal_brust, signal_track, signal_count_varition, signal_sentiment_varition,signal_nothing, signal_nothing_variation, \
                      unfinish_signal, finish_signal, AGGRAGATION_KEYWORDS_NUMBER, PRE_AGGREGATION_NUMBER

day_time = 24*3600
"""
def query_mid_list(ts, keywords_list, time_segment):
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"range":{
                                "timestamp":{
                                    "gte":ts - time_segment,
                                    "lt": ts
                                }
                            }},
                        ],
                    }
                },
                "query":{
                    "bool":{
                        "should":[
                        ]
                    }
                }
            }
        },
        "sort":{"sentiment": {"order": "desc"}},
        "size": 10000
    }
    if keywords_list:
        for word in keywords_list:
            query_body['query']['filtered']['query']['bool']['should'].append({'wildcard':{"text": "*"+word+"*"}})

    datetime = ts2datetime(ts)
    index_name = flow_text_index_name_pre + datetime
    exist_es = es_text.indices.exists(index_name)
    if exist_es:
        search_results = es_text.search(index=index_name, doc_type=flow_text_index_type, body=query_body, fields=["root_mid"])["hits"]["hits"]
    else:
        search_results = []
    origin_mid_list = [] # all related weibo mid list
    if search_results:
        for item in search_results:
            if item.get("fields", ""):
                origin_mid_list.append(item["fields"]["root_mid"][0])
            else:
                origin_mid_list.append(item["_id"])

    datetime_1 = ts2datetime(ts-time_segment)
    index_name_1 = flow_text_index_name_pre + datetime_1
    exist_bool = es_text.indices.exists(index_name_1)
    if datetime != datetime_1 and exist_bool:
        search_results_1 = es_text.search(index=index_name_1, doc_type=flow_text_index_type, body=query_body, fields=['root_mid'])["hits"]["hits"]
        if search_results_1:
            for item in search_results_1:
                if item.get("fields", ""):
                    origin_mid_list.append(item["fields"]["root_mid"][0])
                else:
                    origin_mid_list.append(item["_id"])

    return origin_mid_list
"""


def count_hot_uid(uid, start_time, stop_time, keywords_list):
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"range":{
                                "timestamp":{
                                    "gte":start_time,
                                    "lt": stop_time
                                }
                            }},
                            {"term": {"root_uid": uid}}
                        ]
                    }
                }
#                "query":{
#                    "bool":{
#                        "should":[
#                        ]
#                    }
#                }
            }
        }
    }

    if keywords_list:
        query_body['query']['filtered']['filter']['bool']['must'].append({"terms": {"keywords_string": keywords_list}})
        #for word in keywords_list:
            #query_body['query']['filtered']['query']['bool']['should'].append({'wildcard':{"text": "*"+word+"*"}})

    count = 0
    datetime = ts2datetime(float(stop_time))
    index_name = flow_text_index_name_pre + datetime
    exist_es = es_text.indices.exists(index_name)
    if exist_es:
        count = es_text.count(index=index_name, doc_type=flow_text_index_type, body=query_body)["count"]
    else:
        count = 0

    datetime_1 = ts2datetime(float(start_time))
    if datetime_1 == datetime:
        pass
    else:
        ts = float(stop_time)
        while 1:
            ts = ts-day_time
            datetime = ts2datetime(ts)
            index_name = flow_text_index_name_pre + datetime
            exist_es = es_text.indices.exists(index_name)
            if exist_es:
                count = es_text.count(index=index_name, doc_type=flow_text_index_type, body=query_body)["count"]
            else:
                count += 0
            if datetime_1 == datetime:
                break

    return count



def aggregation_hot_keywords(start_time, stop_time, keywords_list):
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"terms": {"keywords_string": keywords_list}},
                            {"range":{
                                "timestamp":{
                                    "gte":start_time,
                                    "lt": stop_time
                                }
                            }}
                        ]
                    }
                }
            }
        },
        "aggs":{
            "all_keywords":{
                "terms": {"field": "keywords_string", "size": PRE_AGGREGATION_NUMBER}
            }
        }
    }


    keywords_dict = dict()
    datetime = ts2datetime(float(stop_time))
    index_name = flow_text_index_name_pre + datetime
    exist_es = es_text.indices.exists(index_name)
    if exist_es:
        search_results = es_text.search(index=index_name, doc_type=flow_text_index_type, body=query_body)["aggregations"]['all_keywords']['buckets']
        if search_results:
            for item in search_results:
                keywords_list[item['key']] = item['doc_count']

    datetime_1 = ts2datetime(float(start_time))
    if datetime_1 == datetime:
        pass
    else:
        ts = float(stop_time)
        while 1:
            keywords_dict_1 = dict()
            ts = ts-day_time
            datetime = ts2datetime(ts)
            index_name = flow_text_index_name_pre + datetime
            exist_es = es_text.indices.exists(index_name)
            if exist_es:
                search_results_1 = es_text.search(index=index_name, doc_type=flow_text_index_type, body=query_body)["aggregations"]['all_keywords']['buckets']
                if search_results_1:
                    print search_results_1
                    for item in search_results_1:
                        keywords_dict_1[item['key']] = item['doc_count']
                for iter_key in keywords_dict_1.keys():
                    if keywords_dict.has_key(iter_key):
                        keywords_dict[iter_key] += keywords_dict_1[iter_key]
                    else:
                        keywords_dict[iter_key] = keywords_dict_1[iter_key]
            if datetime_1 == datetime:
                break
    print keywords_dict
    return_dict = sorted(keywords_dict.items(), key=lambda x:x[1], reverse=True)[:AGGRAGATION_KEYWORDS_NUMBER]
    return return_dict
