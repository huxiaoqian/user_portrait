# -*- coding:utf-8 -*-

import os
import sys
import time
import json
from aggregation_weibo import specific_keywords_burst_dection
from sensing_strategy import sensors_keywords_detection
reload(sys)
sys.path.append("./../")
from global_utils import es_user_profile as es_profile
from global_utils import es_user_portrait as es
from global_utils import R_SOCIAL_SENSING as r
from parameter import DOC_TYPE_MANAGE_SOCIAL_SENSING as task_doc_type
from parameter import INDEX_MANAGE_SOCIAL_SENSING as index_name
from parameter import DETAIL_SOCIAL_SENSING as index_sensing_task


def social_sensing_task(ts):
    # 1. print start info
    count = 0
    current_path = os.getcwd()
    file_path = os.path.join(current_path, 'social_sensing.py')
    now_ts = str(ts)
    print_log = "&".join([file_path, "start", now_ts])
    print print_log #打印开始信息

    while 1:
        temp = r.rpop("task_name")
        if not temp:
            print count
            now_ts = str(int(time.time()))
            print_log = "&".join([file_path, "end", now_ts])
            print print_log # 打印终止信息
            break  # finish all task in task_list
        task_detail = json.loads(temp)
        count += 1
#        """
        if int(task_detail[6]) == 2:
            specific_keywords_burst_dection(task_detail)
        elif int(task_detail[6]) == 3:
            sensors_keywords_detection(task_detail)
        else:
            pass
#        """

if __name__ == "__main__":
    social_sensing_task()
