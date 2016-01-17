#-*- coding:utf-8 -*-

import os
import time
import json

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
from user_portrait.parameter import DETECT_ITER_COUNT

#test
portrait_index_name = 'user_portrait_1222'
portrait_index_type = 'user'

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
        query_list.append({'wildcard':{user_item: '*'+seed_user[user_item]+'*'}})
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
                uanme =  u'未知'
                fansnum =  u'未知'
                statusnum =  u'未知'
                friendsnum =  u'未知'
            out_user_result.sppend([uid, uname, fansnum, statusnum, friendsnum])
    sort_out_user_result = sorted(out_user_result, key=lambda x:x[2], reverse=True)

    return in_user_list, sort_out_user_list


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
    #step2: identify task name is valid
    task_name = input_dict['task_information']['task_name']
    try:
        task_exist_result = es_group_result.get(index=group_index_name, doc_type=group_index_type, id=task_name)['_source']
    except:
        task_exsit_result = {}
    if task_exist_result != {}:
        return 'task name invalid'
    #step3: identify whether or not to extend----extend mark
    if extend_mark=='1':
        es_status = save_detect2es(input_dict)
        redis_status = save_detect2redis(input_dict) # detect redis queue
    elif extend=='0':
        es_status = save_compute2es(input_dict)
        redis_status = save_compute2redis(input_dict) # compute redis queue
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
    results = {}
    #step1: identify the detect task name id valid---is not in group es
    task_information = input_dict['task_information']
    task_name = task_information['task_name']
    try:
        task_exist_result = es_group_result.get(index=group_index_name, doc_type=group_index_type, id=task_name)
    except:
        task_exist_result = {}
    if task_exist_result != {}:
        return 'task name invalid'
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
def save_detect_event_task():
    results = {}
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
    add_dict['query_condition'] = json.dumps(input_dict['query_condition'])
    try:
        es_group_result.index(index=group_index_name, doc_type=group_index_type, id=task_name, body=add_dict)
        print 'success add compute task es'
    except:
        status = False

    return status

#use to show detect task information
#input: {}
#output: {}
def show_detect_task():
    results = {}
    return results

#use to add detect task having been done to group analysis
#input:{}
#output: {}
def detect2analysis():
    results = {}
    return results

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
