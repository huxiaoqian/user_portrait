# -*- coding:utf-8 -*-

import sys
import json
import math
import time

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
    task_detail = es.get(index=index_manage_sensing_task, doc_type=task_doc_type, id=index_name)["_source"]
    history_status = json.loads(task_detail['hiatory_status'])
    time_series = []
    burst_time_list = []
    ts = int(ts)
    for item in history_status:
        if int(item[0]) <= ts:
            time_series.append(item[0]) # 到目前为止的所有的时间戳
            if int(item[2]) == 1:
                burst_time_list.append(item[0])

    #flow_detail = es.mget(index=index_sensing_task, doc_type=index_name)

    return results

# 获得一段时间内的文本，按序排列
def get_text_detail(task_name, keywords, ts):
    results = dict()

    return results





