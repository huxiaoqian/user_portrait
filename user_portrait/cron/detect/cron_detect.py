#-*- coding:utf-8 -*-
import os
import sys
import time

reload(sys)
sys.path.append('../../')
from global_utils import R_GROUP as r_group # save detect and analysis queue
from global_utils import group_detect_queue_name
from global_utils import es_user_portrait, portrait_index_name, portrait_index_type
from global_utils import es_flow_text, flow_text_index_name_pre, flow_text_index_type
from global_utils import es_retweet, retweet_index_name_pre, retweet_index_type,\
                         be_retweet_index_name_pre, be_retweet_index_type
from global_utils import es_comment, comment_index_name_pre, comment_index_type,\
                         be_comment_index_name_pre, be_comment_index_type
from parameter import DETECT_QUERY_ATTRIBUTE_MULTI

#use to identify the task is exist
#input: task_name
#output: status True/False
def identify_task_exist(task_name):
    status = False
    try:
        task_exist_result = es_group_result.get(index=group_index_name, doc_type=group_index_type, id=task_name)['_source']
    except:
        task_exist_result = {}
    if task_exist_result != {}:
        status = True
    return status

#use to get single user portrait attribute
#input: seed_user_dict
#output: user_portriat_dict
def get_single_user_portrait(seed_user_dict):
    if 'uid' in seed_user_dict:
        uid = seed_user_dict['uid']
        try:
            user_portrait_result = es_user_portrait.get(index=portrait_index_name, doc_type=portrait_index_type, id=uid)['_source']
        except:
            user_portrait_result = {}
    else:
        uname = seed_user_dict['uname']
        query = {'term':{'uname': uname}}
        try:
            user_portrait_result = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type ,\
                      body={'query' query})['_source']
        except:
            user_portrait_result = {}

    return user_portrait_result


#use to detect group by single-person
#input: input_dict
#output: status True/False
def single_detect(input_dict):
    results = {}
    task_information_dict = input_dict['task_information']
    task_name = task_information_dict['task_name']
    task_exist_mark = identify_task_exist(task_name)
    seed_user_dict = input_dict['seed_user']
    query_condition_dict = input_dict['query_condition']
    #step1: get seed user portrait result
    user_portrait = get_single_user_portrait(seed_user_dict)
    #step2: search attribute user set
    #step2.1: get attribute query dict
    attribute_item = query_condition_dict['attribute']
    attribute_query_list = []
    for query_item in attribute_item:
        try:
            user_attribute_value = user_portrait[query_item]
        except:
            user_attribute_value = ''
        if user_attribute_value != '':
            if user_attribute_value in DETECT_QUERY_ATTRIBUTE_MULTI:
                nest_body_list = []
                user_attribute_value_list = user_attribute_value.split('&')
                for attribute_value_item in user_attribute_value_list:
                    nest_body_list.append({'wildcard': {query_item: '*'+attribute_value_item+'*'}})
                attribute_query_list.append({'bool':{'should': nest_body_list}})
            else:
                attribute_query_list.append({'wildcard': {query_item: '*'+attribute_value+'*'}})
    attribute_user_result = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type, \
            body={'query':{'bool':{'must':attribute_query_list}}})['hits']['hits']
    #step3: search structure user set
    #step4: union search and structure user set
    #step5: filter user by event
    #step6: filter by count and evaluation index
    return results

#use to detect group by multi-person
#input: {}
#output: {}
def multi_detect():
    results = {}
    #step1: get seed users attribute
    #step2: search attribute user set
    #step3: search structure user set
    #step4: union search and structure user set
    #step5: filter user by event
    #step6: filter by count and evaluation index
    return results

#use to detect group by attribute or pattern
#input: {}
#output: {}
def attribute_pattern_detect():
    results = {}
    #step1: search text user set(who is in user_portrait)
    #step2: search attribute user
    #step3: filter by count and evaluation index
    return results

#use to detect group by event
#input: {}
#output: {}
def event_detect():
    results = {}
    #step1: search text user set
    #step2: filter user by domain or topic
    #step3: filter by count and evaluation index
    return results

#use to save detect results to es
#input: uid list (detect results)
#output: status (True/False)
def save_detect_results(detect_results):
    mark = False
    try:
        task_exist_result = es_group_result.get(index=group_index_name, doc_type=group_index_type, id=task_name)['_source']
    except:
        task_exist_result = {}
    if task_exist_result != {}:
        task_exist_result['uid_list'] = json.dumps(detect_results)
        es_group_result.index(index=group_index_name, doc_type=group_index_type, id=task_name, body=task_exist_result)
        mark = True

    return mark

#use to change detect task process proportion
#input: task_name, proportion
#output: status (True/False)
def change_process_proportion(task_name, proportion):
    mark = False
    try:
        task_exist_result = es_group_result.get(index=group_index_name, doc_type=group_index_type, id=task_name)['_source']
    except:
        task_exist_result = {}
        print 'task is not exist'
    if task_exist_result != {}:
        task_exist_result['process'] = proportion
        es_group_result.index(index=group_index_name, doc_type=group_index_type, id=task_name, body=task_exist_result)
        mark = True

    return mark


#use to add task to redis queue when the task  detect process fail
#input: input_dict
#output: status
def add_task2queue(input_dict):
    status = True
    try:
        r_group.lpush(group_detect_queue_name, json.dumps(input_dict))
    except:
        status = False

    return status


#use to get detect information from redis queue
#input: NULL
#output: task_information_dict (from redis queue---gruop_detect_task)
def get_detect_information():
    task_information_dict = {}
    task_information_string = r_group.rpop(group_detect_queue_name)
    if task_information_string:
        task_information_dict = json.loads(task_information_string)
    else:
        task_information_dict = {}

    return task_information_dict

#main function to group detect
def compute_group_detect():
    results = {}
    while True:
        #step1:read detect task information from redis queue
        detect_task_information = get_detect_information()
        if detect_task_information != {}:
            start_ts = time.time()
            task_information_dict = detect_task_information['task_information']
            task_name = task_information_dict['task_name']
            #step2:according task type to do group detect
            detect_task_type = task_information_dict['detect_type']
            if detect_task_type == 'single':
                detect_results = single_detect(detect_task_information)
            elif detect_task_type == 'multi':
                detect_results == multi_detect(detect_task_information)
            elif detect_task_type == 'attribute':
                detect_results =  attribute_pattern_detect(detect_task_information)
            elif detect_task_type == 'event':
                detect_results = event_detect(detect_task_information)
            #step3:save detect results to es (status=1 and process=100 and add uid_list)
            mark = save_detect_results(detect_results)
            #step4:add task_information_dict to redis queue when detect process fail
            if mark == False:
                status = add_task2queue(detect_task_information)
            else:
                end_ts = time.time()
                print 'success detect task:' + task_name
                print 'time cost %s sec' % (end_ts - start_ts)


if __name__=='__main__':
    compute_group_detect()
