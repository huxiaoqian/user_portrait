# -*- coding:utf-8 -*-

import sys
import time
import json
from aggregation_weibo import specific_keywords_burst_dection
reload(sys)
sys.path.append("./../")
from global_utils import es_user_profile as es_profile
from global_utils import es_user_portrait as es
from global_utils import R_SOCIAL_SENSING as r
from parameter import DOC_TYPE_MANAGE_SOCIAL_SENSING as task_doc_type
from parameter import INDEX_MANAGE_SOCIAL_SENSING as index_name
from parameter import DETAIL_SOCIAL_SENSING as index_sensing_task


def social_sensing_task():
    while 1:
        temp = r.rpop("task_name")
        if not temp:
            break  # finish all task in task_list
        task_detail = json.loads(temp)
        print "task_detail: ", task_detail
   #     print specific_keywords_burst_dection(task_detail)


if __name__ == "__main__":
    social_sensing_task()
