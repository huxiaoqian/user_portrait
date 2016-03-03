#-*- coding:utf-8 -*-

import os
import time
import json
import math

from user_portrait.global_utils import es_user_portrait, portrait_index_name, portrait_index_type
from user_portrait.global_utils import es_group_result, group_index_name, group_index_type
from user_portrait.global_utils import es_flow_text, flow_text_index_name_pre, flow_text_index_type
from user_portrait.global_utils import es_user_profile, profile_index_name, profile_index_type
from user_portrait.global_utils import R_GROUP as r_group
from user_portrait.global_utils import group_detect_queue_name, group_analysis_queue_name
from user_portrait.global_utils import retweet_index_name_pre, retweet_index_type,\
                                       be_retweet_index_name_pre, be_retweet_index_type,\
                                       comment_index_name_pre, comment_index_type,\
                                       be_comment_index_name_pre, be_comment_index_type
from user_portrait.parameter import DETECT_ITER_COUNT, MAX_VALUE, MAX_PROCESS
from user_portrait.time_utils import ts2datetime, datetime2ts
from user_portrait.parameter import DAY

#use to save detect single task
#input: input_dict
#output: status # 'seed user invalid'/'task name invalid'
def save_detect_single_task(input_dict):
    results = {}
    #step1: identify the seed user is in user_portrait
    seed_user = input_dict['query_condition']['seed_user']
    query = []
    query_list = []
    for user_item in seed_user:
        query_list.append({'term':{user_item: seed_user[user_item]}})
    query.append({'bool':{'should': query_list}})
    try:
        seed_user_result = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type, \
                            body={'query':{'bool':{'must':query}}, 'size':1})['hits']['hits']
    except Exception, e:
        raise e
    try:
        seed_user_source = seed_user_result[0]['_source']
    except:
        return 'seed user invalid'

    #step2: identify the detect task name is valid----is not in group es
    task_information = input_dict['task_information']
    task_name = task_information['task_name']
    try:
        task_exist_result = es_group_result.get(index=group_index_name, doc_type=group_index_type, id=task_name)
    except:
        task_exist_result = {}
    if task_exist_result != {}:
        return 'task name invalid'

    #step3: save to es
    es_status = save_detect2es(input_dict)
    #step4: save to redis queue
    redis_status = save_detect2redis(input_dict)
    #identify the operation status
    if es_status==True and redis_status==True:
        status = True
    else:
        status = False

    return status

#use to identify the user is or not  in user_portrait
#input: uid_list
#output: in_user_list, sort_out_user_list
def identify_user_out(input_uid_list):
    out_user_list = []
    in_user_list = []
    input_len = len(input_uid_list)
    iter_count = 0
    print 'identify user out'
    #get user list who is out user_portrait
    while iter_count < input_len:
        iter_user_list = input_uid_list[iter_count: iter_count+DETECT_ITER_COUNT]
        try:
            portrait_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type, body={'ids':iter_user_list}, _source=False)['docs']
        except:
            portrait_result = []
        for item in portrait_result:
            uid = item['_id']
            if item['found'] != True:
                out_user_list.append(uid)
            else:
                in_user_list.append(uid)
        iter_count += DETECT_ITER_COUNT
    print 'get out user portrait information'
    #get user profile information for out user_portrait
    iter_count = 0
    out_user_count = len(out_user_list)
    out_user_result = []
    while iter_count < out_user_count:
        iter_user_list = out_user_list[iter_count: iter_count+DETECT_ITER_COUNT]
        try:
            profile_result = es_user_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={'ids':iter_user_list}, _source=True)['docs']
        except:
            profile_result = []
        for item in profile_result:
            uid = item['_id']
            if item['found']==True:
                source = item['_source']
                uname = source['nick_name']
                fansnum = source['fansnum']
                statusnum = source['statusnum']
                friendsnum = source['friendsnum']
            else:
                uname =  u'未知'
                fansnum =  u'未知'
                statusnum =  u'未知'
                friendsnum =  u'未知'
            out_user_result.append([uid, uname, fansnum, statusnum, friendsnum])
        iter_count += DETECT_ITER_COUNT 
    
    sort_out_user_result = sorted(out_user_result, key=lambda x:x[2], reverse=True)

    return in_user_list, sort_out_user_result


#use to save detect multi task
#input: intput_dict, extend_mark----input_dict={'task_information': task_information_dict}/{'task_information':task_information, 'query_dict':query_dict}, extend_mark=0/1
#output: user_list (who is not in user_portrait)
#step1: identify user is in user_portrait and not in user_portrait
#step2: identify task name is valid
#step3: identify whether or not to extend---extend mark
#step3.1: if extend mark==1:  save to redis and es
#step3.2: if extend mark==0:  save to es(type=compute)
def save_detect_multi_task(input_dict, extend_mark):
    results = {}
    task_information_dict = input_dict['task_information']
    input_uid_list = task_information_dict['uid_list']
    #step1: identify user is in user_portrait and not in user_portrait
    in_user_list, out_user_list = identify_user_out(input_uid_list)
    input_dict['task_information']['uid_list'] = in_user_list
    print 'step1'
    #step2: identify task name is valid
    task_name = input_dict['task_information']['task_name']
    try:
        task_exist_result = es_group_result.get(index=group_index_name, doc_type=group_index_type, id=task_name)['_source']
    except:
        task_exist_result = {}
    if task_exist_result != {}:
        return 'task name invalid'
    print 'step2'
    #step3: identify whether or not to extend----extend mark
    if extend_mark=='1':
        print 'step3 save'
        es_status = save_detect2es(input_dict)
        redis_status = save_detect2redis(input_dict) # detect redis queue
    elif extend_mark=='0':
        uid_list = input_dict['task_information']['uid_list']
        input_dict['task_information']['uid_list'] = uid_list
        input_dict['task_information']['status'] = 0
        print 'uid_list:', len(uid_list), uid_list, type(uid_list)
        input_dict['task_information']['count'] = len(uid_list)
        print 'step3 save'
        es_status = save_compute2es(input_dict)
        add_redis_dict = input_dict['task_information']
        redis_status = save_compute2redis(add_redis_dict) # compute redis queue
    #identify the operation status
    if es_status==True and redis_status==True:
        status = True
    else:
        status = False
        
    return status, out_user_list

#use to save detect attribute task
#input: input_dict {'task_information':{}, 'query_dict':{}}
#output: status True/False
def save_detect_attribute_task(input_dict):
    status = True
    #step1: identify the detect task name id valid---is not in group es
    task_information = input_dict['task_information']
    task_name = task_information['task_name']
    try:
        task_exist_result = es_group_result.get(index=group_index_name, doc_type=group_index_type, id=task_name)
    except:
        task_exist_result = {}
    if task_exist_result != {}:
        return 'task name invalid'
    #print 'input_dict:', input_dict
    
    #step2: save to es
    es_status = save_detect2es(input_dict)
    #step3: save to redis
    redis_status = save_detect2redis(input_dict)
    #identify the operation status
    if es_status==True and redis_status==True:
        status = True
    else:
        status = False
    

    return status

#use to save detect event task
#input: input_dict {'task_information':{}, 'query_dict':{}}
#output: status True/False
def save_detect_event_task(input_dict):
    status = True
    #step1:identify the task name is valid----is not in group es
    task_information = input_dict['task_information']
    task_name = task_information['task_name']
    try:
        task_exist_result = es_group_result.get(index=group_index_name, doc_type=group_index_type, id=task_name)
    except:
        task_exist_result = {}
    if task_exist_result != {}:
        return 'task name invalid'
    
    #step2:save to es
    es_status = save_detect2es(input_dict)
    #step3:save to redis
    redis_status = save_detect2redis(input_dict)
    #identify the operation status
    if es_status==True and redis_status==True:
        status = True
    else:
        status = False
    
    return status


#use to save parameter and task information to group redis queue---detect
#input: input_dict 
#output: status True/False
def save_detect2redis(input_dict):
    status = True
    try:
        r_group.lpush(group_detect_queue_name, json.dumps(input_dict))
        print 'success to save redis'
    except:
        status = False
    return status

#use to save parameter and task information to group redis queue---analysis
#input: input_dict
#output: status True/False
def save_compute2redis(input_dict):
    status = True
    try:
        r_group.lpush(group_analysis_queue_name, json.dumps(input_dict))
        print 'success add detect task to redis queue'
    except:
        status = False
    return status

#use to save parameter and task information to group es
#input: input_dict
#output: status   True/False
def save_detect2es(input_dict):
    add_dict = {}
    status = True
    add_dict = dict(add_dict, **input_dict['task_information'])
    task_name = input_dict['task_information']['task_name']
    add_dict['query_condition'] = json.dumps(input_dict['query_condition'])
    try:
        es_group_result.index(index=group_index_name, doc_type=group_index_type, id=task_name, body=add_dict)
        print 'success add detect task to es'
    except:
        status = False
    
    return status

#use to save parameter and task information to group es
#input: input_dict
#output: status True/False
def save_compute2es(input_dict):
    add_dict = {}
    status = True
    add_dict = dict(add_dict, **input_dict['task_information'])
    task_name = input_dict['task_information']['task_name']
    uid_list = input_dict['task_information']['uid_list']
    if isinstance(uid_list, list):
        count = len(input_dict['task_information']['uid_list'])
    else:
        count = len(json.loads(input_dict['task_information']['uid_list']))
    add_dict['count'] = count
    if 'query_condition' not in input_dict:
        input_dict['query_condition'] = {}
    if isinstance(input_dict['query_condition'], str):
        add_dict['query_condition'] = input_dict['query_condition']
    else:
        add_dict['query_condition'] = json.dumps(input_dict['query_condition'])
    try:
        es_group_result.index(index=group_index_name, doc_type=group_index_type, id=task_name, body=add_dict)
        print 'success add compute task es'
    except:
        status = False

    return status

#use to show detect task information
#input: NULL
#output: detect task list
def show_detect_task():
    results = []
    query = [{'match':{'task_type': 'detect'}}]
    try:
        search_results = es_group_result.search(index=group_index_name, doc_type=group_index_type, \
                body={'query':{'bool':{'must':query}}, 'sort':[{'submit_date': 'desc'}], 'size':MAX_VALUE})['hits']['hits']
    except:
        search_results = []
    for group_item in search_results:
        source = group_item['_source']
        task_name = source['task_name']
        submit_date = ts2datetime(int(source['submit_date']))
        submit_user = source['submit_user']
        detect_type = source['detect_type']
        state = source['state']
        process = source['detect_process']
        results.append([task_name, submit_user, submit_date, detect_type, state, process])

    return results

#use to search detect task information
#input: task_name, 
def search_detect_task(task_name, submit_date, state, process, detect_type, submit_user):
    results = []
    query = [{'match':{'task_type': 'detect'}}]
    condition_num = 0
    if task_name:
        task_name_list = task_name.split(' ')
        for item in task_name_list:
            query.append({'wildcard':{'task_name': '*'+item+'*'}})
            condition_num += 1
    if submit_date:
        submit_date_ts = datetime2ts(submit_date)
        submit_date_from = submit_date_ts
        submit_date_to = submit_date_ts + DAY
        query.append({'range':{'submit_date':{'gte':submit_date_from, 'lt':submit_date_to}}})
        condition_num += 1
    if state:
        state_list = state.split(' ')
        for item in state_list:
            query.append({'wildcard':{'state': '*'+item+'*'}})
            condition_num += 1
    if process:
        query.append({'range':{'detect_process':{'from': int(process), 'to': MAX_PROCESS}}})
        condition_num += 1
    if detect_type:
        
        detect_type_list = detect_type.split(',')
        nest_body_list = []
        for type_item in detect_type_list:
            nest_body_list.append({'wildcard':{'detect_type': '*'+type_item+'*'}})
        query.append({'bool':{'should': nest_body_list}})
        
        condition_num += 1
    if submit_user:
        query.append({'wildcard':{'submit_user': '*'+submit_user+'*'}})
        condition_num += 1
    try:
        search_result = es_group_result.search(index=group_index_name, doc_type=group_index_type, \
                    body={'query':{'bool': {'must': query}}, 'sort':[{'submit_date': {'order': 'desc'}}], 'size':MAX_VALUE})['hits']['hits']
    except:
        search_result = []
    #get group information table
    for group_item in search_result:
        source = group_item['_source']
        task_name = source['task_name']
        submit_date = ts2datetime(int(source['submit_date']))
        submit_user = source['submit_user']
        detect_type = source['detect_type']
        state = source['state']
        process = source['detect_process']

        results.append([task_name, submit_user, submit_date, detect_type, state, process])
        
    return results

def get_evaluate_max():
    max_result = {}
    index_name = portrait_index_name
    index_type = portrait_index_type
    evaluate_index = ['activeness', 'importance', 'influence']
    for evaluate in evaluate_index:
        query_body = {
            'query':{
                'match_all':{}
                },
            'size':1,
            'sort':[{evaluate: {'order': 'desc'}}]
            }
        try:
            result = es_user_portrait.search(index=index_name, doc_type=index_type, body=query_body)['hits']['hits']
        except Exception, e:
            raise e
        max_evaluate = result[0]['_source'][evaluate]
        max_result[evaluate] = max_evaluate
    return max_result


#use to show detect task result
#input: task_name
#output: uid_list
def show_detect_result(task_name):
    user_result = []
    #step1:identify the task name id exist
    try:
        task_exist_result = es_group_result.get(index=group_index_name, doc_type=group_index_type, id=task_name)['_source']
    except:
        task_exist_result = {}
    if task_exist_result == {}:
        return 'task name is not exist'
    #step2:get uid list
    uid_list = json.loads(task_exist_result['uid_list'])
    #step3:get user evaluation information---uid/uname/activeness/importance/influence
    iter_count = 0
    uid_count = len(uid_list)
    while iter_count < uid_count:
        iter_user_list = uid_list[iter_count: iter_count+DETECT_ITER_COUNT]
        try:
            portrait_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type, \
                                                    body={'ids':iter_user_list}, _source=True)['docs']
        except:
            portrait_result = []
        for item in portrait_result:
            uid = item['_id']
            if item['found']==True:
                source = item['_source']
                uname = source['uname']
                evaluate_max = get_evaluate_max()
                activeness = math.log(source['activeness']/evaluate_max['activeness'] * 9 + 1 ,10)*100
                importance = math.log(source['importance']/evaluate_max['importance'] * 9 + 1 ,10)*100
                influence = math.log(source['influence']/evaluate_max['influence'] * 9 + 1 ,10)*100
            
            else:
                uname = u'未知'
                activeness = u'未知'
                importance = u'未知'
                influence = u'未知'
            user_result.append([uid, uname, activeness, importance, influence])
        iter_count += DETECT_ITER_COUNT
    sort_user_result = sorted(user_result, key=lambda x:x[4], reverse=True)
  
    return sort_user_result


#use to add detect task having been done to group analysis
#input:  input_data  {'task_name':xx, 'uid_list':[]}
#output: status
def detect2analysis(input_data):
    results = {}
    status = True
    task_name = input_data['task_name']
    uid_list = input_data['uid_list']
    #step1: identify the task is exist
    try:
        task_exist_result = es_group_result.get(index=group_index_name, doc_type=group_index_type, id=task_name)['_source']
    except:
        task_exist_result = {}
    if task_exist_result == {}:
        return 'task name is not exsit'
    #step2: update task uid list
    task_exist_result['uid_list'] = uid_list
    #step3: update task_type in es
    task_exist_result['status'] = 0 # mark the compute status
    task_exist_result['count'] = len(uid_list)
    task_exist_result['task_type'] = 'analysis'
    #get task information dict
    task_information_dict = {'task_name':task_name, 'uid_list':uid_list, 'status':0, 'count':len(uid_list),\
            'task_type':'analysis', 'submit_user':task_exist_result['submit_user'], 'submit_date':task_exist_result['submit_date'], \
            'detect_type':task_exist_result['detect_type'], 'detect_process':task_exist_result['detect_process'], \
            'state': task_exist_result['state']}
    
    add_es_dict = {'task_information':task_information_dict, 'query_condition':task_exist_result['query_condition']}
    es_status = save_compute2es(add_es_dict)
    #step4: add task to analysis queue
    redis_status = save_compute2redis(task_exist_result)
    #identify the operation status
    if es_status==True and redis_status==True:
        status = True
    else:
        status = False

    return status

#use to delete detect task
#input: task_name
#output: status
def delete_task(task_name):
    status = True
    try:
        result = es_group_result.delete(index=group_index_name, doc_type=group_index_type, id=task_name)
    except Exception, e:
        raise e
    
    return status

#use to submit sensing result to analysis
def submit_sensing(input_dict):
    status = True
    #step1: identify the task name is valid
    task_name = input_dict['task_information']['task_name']
    try:
        task_exist_result = es_group_result.get(index=group_index_name, doc_type=group_index_type, id=task_name)
    except:
        task_exist_result = {}
    if task_exist_result != {}:
        return 'task name invalid'

    #step2: save to compute es
    submit_date = int(time.time())
    input_dict['task_information']['submit_date'] = submit_date
    input_dict['task_information']['count'] = len(input_dict['task_information']['uid_list'])
    input_dict['task_information']['state'] = input_dict['task_information']['state']
    input_dict['task_information']['status'] = 0
    input_dict['task_information']['detect_type'] = 'sensing'
    input_dict['task_information']['task_type'] = input_dict['task_information']['task_type']
    es_status = save_compute2es(input_dict)
    #step3: save to compute redis
    add_dict2redis = input_dict['task_information']
    redis_status = save_compute2redis(add_dict2redis)
    #identify the operation status
    if es_status == True and redis_status ==True:
        status = True
    else:
        status = False
    return status
