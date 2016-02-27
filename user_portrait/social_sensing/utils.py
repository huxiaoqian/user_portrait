# -*- coding:utf-8 -*-

import sys
import json
import math
import time
from get_task_detail import get_task_detail_2
from full_text_serach import get_origin_weibo_detail, get_retweet_weibo_detail, get_positive_weibo_detail, get_sensitive_weibo_detail
from user_portrait.global_utils import es_user_profile as es_profile
from user_portrait.global_utils import es_user_portrait as es
from user_portrait.global_utils import es_flow_text as es_text
from user_portrait.global_utils import profile_index_name, profile_index_type, portrait_index_name, portrait_index_type, \
                         flow_text_index_name_pre, flow_text_index_type
from user_portrait.parameter import INDEX_MANAGE_SOCIAL_SENSING as index_manage_sensing_task
from user_portrait.parameter import DOC_TYPE_MANAGE_SOCIAL_SENSING as task_doc_type
from user_portrait.parameter import DETAIL_SOCIAL_SENSING as index_sensing_task

def get_warning_detail(task_name, keywords, ts, task_type="2"):
    results = dict()
    index_name = task_name # 可能的index-name

    results = get_task_detail_2(task_name, keywords, ts)

    #flow_detail = es.mget(index=index_sensing_task, doc_type=index_name)

    return results

# 获得一段时间内的文本，按序排列
def get_text_detail(task_name, ts, text_type, size=100):
    results = []
    task_detail = es.get(index=index_manage_sensing_task, doc_type=task_doc_type, id=task_name)["_source"]
    keywords_list = json.loads(task_detail['keywords'])
    sensitive_words_list = json.loads(task_detail['sensitive_words'])
    social_sensors = json.loads(task_detail["social_sensors"])

    #print social_sensors
    if int(text_type) == 0: # 原创微博
        results = get_origin_weibo_detail(ts, social_sensors, keywords_list,  size)

    elif int(text_type) == 1: # 转发微博
        results = get_retweet_weibo_detail(ts, social_sensors, keywords_list, size, 3)
        #results = get_origin_weibo_detail(ts, social_sensors, keywords_list, size, 3)

    elif int(text_type) == 2: # 评论微博
        results = get_retweet_weibo_detail(ts, social_sensors, keywords_list, size, 2)
        #results = get_origin_weibo_detail(ts, social_sensors, keywords_list, size, 2)

    elif int(text_type) == 3: # 积极微博
        results = get_positive_weibo_detail(ts, social_sensors, keywords_list, size, "1")

    elif int(text_type) == 4: # 中性微博
        results = get_positive_weibo_detail(ts, social_sensors, keywords_list, size, "0")

    elif int(text_type) == 5: # 消极微博
        results = get_positive_weibo_detail(ts, social_sensors, keywords_list, size, "2")

    elif int(text_type) == 6 and social_sensors: # 原创敏感微博
        results = get_sensitive_weibo_detail(ts, social_sensors, sensitive_words_list, 1, size)

    elif int(text_type) == 7 and social_sensors: # 转发敏感微博
        results = get_sensitive_weibo_detail(ts, social_sensors, sensitive_words_list, 3, size)

    elif int(text_type) == 8 and social_sensors: # 评论敏感微博
        results = get_sensitive_weibo_detail(ts, social_sensors, sensitive_words_list, 2, size)

    else:
        print "input error"


    return results





