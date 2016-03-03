# -*- coding:utf-8 -*-

# 本程序定时启动，是监控任务的入口，从manag es中读取尚未完成的任务，送入redis的任务队列中，
# 由子程序从队列中pop出任务信息进行监控计算

import sys
import time
import json
import os
from aggregation_weibo import specific_keywords_burst_dection
from social_sensing import social_sensing_task
reload(sys)
sys.path.append("./../")
from global_utils import es_user_profile as es_profile
from global_utils import R_SOCIAL_SENSING as r
from global_utils import es_user_portrait as es
from time_utils import ts2datetime, datetime2ts, ts2date
from parameter import DOC_TYPE_MANAGE_SOCIAL_SENSING as task_doc_type
from parameter import INDEX_MANAGE_SOCIAL_SENSING as index_name
from parameter import DETAIL_SOCIAL_SENSING as index_sensing_task
from parameter import SOCIAL_SENSOR_TIME_INTERVAL as time_interval

def create_task_list(ts):
    # 1. search from manage_sensing_task
    # 2. push to redis list-----task_work

    # print start info
    current_path = os.getcwd()
    file_path = os.path.join(current_path, 'task_list.py')
    now_ts = str(int(time.time()))
    print_log = "&".join([file_path, "start", now_ts])
    print print_log

    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"term":{"finish": "0"}},
                            {"term":{"processing_status": "1"}}
                        ]
                    }
                }
            }
        }
    }

    search_results = es.search(index=index_name, doc_type=task_doc_type, body=query_body)['hits']['hits']

    count = 0
    if search_results:
        for iter_item in search_results:
            item = iter_item['_source']
            task = []
            task.append(item['task_name']) # task_name
            task.append(json.loads(item['social_sensors'])) # social sensors
            task.append(json.loads(item['keywords'])) # filter keywords
            task.append(json.loads(item['sensitive_words'])) #load sensitive_words
            task.append(item['stop_time']) # stop time
            task.append(item['warning_status']) # last step status
            task.append(item['task_type']) # task type
            task.append(ts)
            r.lpush('task_name', json.dumps(task))
            count += 1

    print count
    now_ts = str(int(time.time()))
    print_log = "&".join([file_path, "end", now_ts])
    print print_log


if __name__ == "__main__":

    ts2 = datetime2ts("2013-09-08")
    #ts1 = datetime2ts("2013-09-01")
    ts1 = 1377984600
    ts = ts1 + time_interval
    while 1:
        if ts <= ts2:
            print ts
            create_task_list(ts)
            social_sensing_task(ts)
            ts += time_interval
        else:
            break

    """

    ts = time.time()
    create_task_list(ts)
    social_sensing_task(ts)
    """
