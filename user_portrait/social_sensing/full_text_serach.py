# -*- coding:utf-8 -*-

import sys
import time
import json
import numpy as np
from elasticsearch import Elasticsearch
from  mappings_social_sensing import mappings_sensing_task
reload(sys)
sys.path.append("./../")
from global_utils import es_flow_text as es_text
from global_utils import es_user_profile as es_profile
from global_utils import es_user_portrait
from global_utils import R_SOCIAL_SENSING as r
from time_utils import ts2datetime, datetime2ts
from global_utils import flow_text_index_name_pre, flow_text_index_type, profile_index_name, profile_index_type, \
                         portrait_index_name, portrait_index_type
from parameter import SOCIAL_SENSOR_TIME_INTERVAL as time_interval
from parameter import SOCIAL_SENSOR_FORWARD_RANGE as forward_time_range
from parameter import DETAIL_SOCIAL_SENSING as index_sensing_task
from parameter import INDEX_MANAGE_SOCIAL_SENSING as index_manage_social_task
from parameter import DOC_TYPE_MANAGE_SOCIAL_SENSING as task_doc_type
from parameter import FORWARD_N as forward_n
from parameter import INITIAL_EXIST_COUNT as initial_count
from parameter import IMPORTANT_USER_NUMBER, IMPORTANT_USER_THRESHOULD, signal_brust, signal_track, signal_count_varition, signal_sentiment_varition,signal_nothing, signal_nothing_variation, \
                      unfinish_signal, finish_signal


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



if __name__ == "__main__":
    ts1 = datetime2ts("2013-09-01")
    ts = ts1 + 1800*3

    print len(query_mid_list(ts, ['维权', '律师'],1800))
