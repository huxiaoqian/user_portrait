#-*- coding:utf-8 -*-

import os
import time
import json

from user_portrait.global_utils import es_user_portrait, portrait_index_name, portrait_index_type
from user_portrait.global_utils import es_group_result, group_index_name, group_index_type
from user_portrait.global_utils import es_flow_text, flow_text_index_name_pre, flow_text_index_type
from user_portrait.global_utils import R_GROUP as r_group
from user_portrait.global_utils import group_detect_queue_name
from user_portrait.global_utils import retweet_index_name_pre, retweet_index_type,\
                                       be_retweet_index_name_pre, be_retweet_index_type,\
                                       comment_index_name_pre, comment_index_type,\
                                       be_comment_index_name_pre, be_comment_index_type

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
    query = {}
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
        seed_user_source = seed_user_result['_source']
    except:
        return 'seed user invalid'

    #step2: identify the detect task name is valid----is not in group es
    task_information = input_dict['task_information']
    task_name = task_information['task_name']
    try:
        task_exist_result = es_group_result.search(index=group_index_name, doc_type=group_index_type, id=task_name)
    except:
        task_exist_result = {}
    if task_exist_result != {}:
        return 'task name invalid'

    #step3: save to es
    save_detect2es(input_dict)
    #step4: save to redis queue
    save_detect2redis(input_dict)
    return results


#use to save detect multi task
#input: {}
#output: {}
def save_detect_multi_task():
    results = {}
    #step1: identify user is in user_portrait and not in user_portrait
    return results


def save_detect_task():
    results = {}
    return results


#use to save parameter and task information to group redis queue
#input: input_dict 
#output: status True/False
def save_detect2redis(input_dict):
    status = True
    try:
        r_group.lpush(group_detect_queue_name, json.dumps(input_dict))
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
