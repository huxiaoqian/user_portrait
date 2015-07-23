# -*- coding: UTF-8 -*-
import sys
import time
import json
#test
'''
reload(sys)
sys.path.append('../')
from global_utils import R_GROUP as r
from global_utils import es_user_portrait as es
from time_utils import ts2datetime, datetime2ts
'''
from user_portrait.global_utils import R_GROUP as r
from user_portrait.global_utils import es_user_portrait
from user_portrait.time_utils import ts2datetime, datetime2ts


index_name = 'group_result'
index_type = 'group'


def submit_task(input_data):
    r.lpush('group_task', json.dumps(input_data))
    return True

def get_group_results(task_name):
    result = {}
    query_body = {
        'query':{
            'term':{
                'task_name': task_name
                }
            }
            }
    result = es.search(index=index_name, doc_type=index_type, body=query_body)['hits']['hits']
    try:
        source = result['_source']
    except:
        source = None

    return source

# delete group results from es_user_portrait 'group_analysis'
def delete_group_results(task_name):
    query_body = {
        'query':{
            'term':{
                'task_name': task_name
                }
            }
        }
    result = es.delete_by_query(index=index_name, doc_type=index_type, body=query_body)
    if result['_indices']['twitter']['_shards']['failed'] == 0:
        return True
    else:
        return False


if __name__=='__main__':
    #test group task
    input_data = {}
    input_data['task_name'] = 'test_task'
    input_data['uid_list'] = ['2010832710', '3482838791', '3697357313', '2496434537',\
                '1642591402', '2074370833', '1640601392', '1773489534',\
                '2722498861', '2803301701']
    input_data['submit_date'] = '2013-09-08'
    input_data['state'] = 'it is a test'
    submit_task(input_data)

