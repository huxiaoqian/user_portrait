# -*- coding: UTF-8 -*-
import sys
import time
import json
reload(sys)
sys.path.append('../../')
from global_utils import es_group_result as es
from global_utils import group_index_name as index_name
from global_utils import group_index_type as index_type


def save_group_results(results):
    status = False
    #step1: identify the task is exist
    try:
        task_exist_result = es.get(index=index_name, doc_type=index_type, id=results['task_name'])['_source']
    except:
        task_exist_result = {}

    #step2: save result
    if task_exist_result != {}:
        es.index(index=index_name, doc_type=index_type, body=results, id=results['task_name'])
        status = True

    return status


