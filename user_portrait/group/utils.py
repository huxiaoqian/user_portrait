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

#submit new task and identify the task name unique
def submit_task(input_data):
    status = 0
    result = r.lrange('group_task', 0, -1)
    #print 'result:',result
    for task in result:
        task_dict = json.loads(task)
        task_name = task['task_name']
        if input_data==task_name:
            status += 1
    result = es.get(index=index_name, doc_type=index_type, id=task_name)
    try:
        task_exist = result['_source']
    except:
        status += 1
    if status != 0:
        return False
    else:
        r.lpush('group_task', json.dumps(input_data))
    return True

#search task by some condition -whether add download
def search_task(task_name, submit_date, state, size):
    results = []
    query = []
    condition_num = 0
    if task_name:
        query.append({'wildcard':{'task_name': '*' + task_name + '*'}})
        condition_num += 1
    if submit_date:
        query.append({'match':{'submit_date': submit_date}})
        condition_num += 1
    if state:
        query.append({'wildcard':{'state': '*' + state + '*'}})
        condition_num += 1
    if num > 0:
        try:
            source = es.search(
                    index = 'group_result',
                    doc_type = 'group',
                    body = {
                        'query':{
                            'bool':{
                                'must':query
                                }
                            },
                        'sort': [{'count':{'order': 'desc'}}],
                        'size': size
                        }
                    )
        except Exception as e:
            raise e
    else:
        source = es.search(
                index = 'group_task',
                doc_type = 'group',
                body = {
                    'query':{'match_all':{}
                        },
                    'sort': [{'count': {'order': 'desc'}}],
                    'size' : size
                    }
                )

    
    return source

#show group results
def get_group_results(task_name):
    result = {}
    result = es.get(index=index_name, doc_type=index_type, id=task_name)['docs']
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
    print 'result:', result
    '''
    if result['_indices']['twitter']['_shards']['failed'] == 0:
        return True
    else:
        return False
    '''
    return True


if __name__=='__main__':
    #test group task
    input_data = {}
    input_data['task_name'] = 'test_task'
    input_data['uid_list'] = ['2010832710', '3482838791', '3697357313', '2496434537',\
                '1642591402', '2074370833', '1640601392', '1773489534',\
                '2722498861', '2803301701']
    input_data['submit_date'] = '2013-09-08'
    input_data['state'] = 'it is a test'
    #submit_task(input_data)
    test_task_name = 'test name'
    status = delete_group_results(test_task_name)
    print 'status:', status
