# -*- coding: UTF-8 -*-
import sys
import time
import json
reload(sys)
sys.path.append('../../')
from global_utils import es_user_portrait as es

index_name = 'group_result'
index_type = 'group'


def save_group_results(results):
    status = False
    return status


if __name__=='__main__':
    #test results
    uid_list = ['2010832710', '3482838791', '3697357313', '2496434537',\
                '1642591402', '2074370833', '1640601392', '1773489534',\
                '2722498861', '2803301701']
    results = {
        'task_name': 'test name',
        'submit_date': '2013-09-07',
        'state': 'it is a test',
        'uid_list': json.dumps(uid_list),
        'count': 10
    }
    save_group_results(results)
