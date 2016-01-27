# -*- coding:utf-8 -*-

import sys
import json
import math
import time
from get_task_detail import get_task_detail_2, get_detail_text
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
def get_text_detail(task_name, keywords, ts, text_type, size=100):
    results = dict()

    results = get_detail_text(task_name, keywords, ts, text_type)
    return results





