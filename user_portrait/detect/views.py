#-*- coding:utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect, send_from_directory
from utils import save_detect_single_task, save_detect_multi_task ,\
                  save_detect_attribute_task, save_detect_event_task, \
                  show_detect_task, detect2analysis, delete_task, \
                  show_detect_result, search_detect_task, submit_sensing

from user_portrait.global_config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from user_portrait.parameter import DETECT_QUERY_ATTRIBUTE, DETECT_QUERY_STRUCTURE,\
                                    DETECT_QUERY_FILTER, DETECT_DEFAULT_WEIGHT, \
                                    DETECT_DEFAULT_MARK, DETECT_DEFAULT_COUNT, \
                                    DETECT_FILTER_VALUE_FROM, DETECT_FILTER_VALUE_TO, \
                                    DETECT_TEXT_FUZZ_ITEM, DETECT_TEXT_RANGE_ITEM
from user_portrait.parameter import DETECT_ATTRIBUTE_FUZZ_ITEM, DETECT_ATTRIBUTE_MULTI_ITEM, \
                                    DETECT_ATTRIBUTE_SELECT_ITEM ,\
                                    DETECT_PATTERN_FUZZ_ITEM, DETECT_PATTERN_SELECT_ITEM ,\
                                    DETECT_PATTERN_RANGE_ITEM, DETECT_EVENT_ATTRIBUTE,\
                                    DETECT_EVENT_TEXT_FUZZ_ITEM, DETECT_EVENT_TEXT_RANGE_ITEM
from user_portrait.parameter import DAY
from user_portrait.time_utils import ts2datetime, datetime2ts
from social_sensing_utils import show_social_sensing_task, show_important_users

mod = Blueprint('detect', __name__, url_prefix='/detect')

# use to submit parameter single-person group detection
@mod.route('/single_person/')
def ajax_single_person():
    results = {}
    query_dict = {}   #query_dict = {'seed_user':{},'attribute':[],'attribute_weight': 0.5,'struture':[], 'structure_weight': 0.5, 'TEXT':{},'filter':{}}
    condition_num = 0 #condition_num != 0
    attribute_condition_num = 0
    structure_condition_num = 0
    #get seed user uname or uid
    seed_user_dict = {}
    seed_uname = request.args.get('seed_uname', '')
    if seed_uname != '':
        seed_user_dict['uname'] = seed_uname
    seed_uid = request.args.get('seed_uid', '')
    if seed_uid != '':
        seed_user_dict['uid'] = seed_uid
    if seed_user_dict == {}:
        return 'no seed user' # if no seed user information return notice
    query_dict['seed_user'] = seed_user_dict
    #get query dict: attribute
    attribute_list = []
    for attribute_item in DETECT_QUERY_ATTRIBUTE:
        attribute_mark = request.args.get(attribute_item, DETECT_DEFAULT_MARK) # '0':not select--default  '1': select
        if attribute_mark == '1':
            attribute_list.append(attribute_item)
            attribute_condition_num += 1
    attribute_condition_num = len(attribute_list)
    attribute_weight = request.args.get('attribute_weight', DETECT_DEFAULT_WEIGHT) #default weight: 0.5
    attribute_weight = float(attribute_weight)
    if attribute_condition_num==0:
        attribute_weight = 0
    query_dict['attribute'] = attribute_list
    query_dict['attribute_weight'] = attribute_weight
    #get query_dict: strucure
    structure_list = {}
    for structure_item in DETECT_QUERY_STRUCTURE:
        structure_mark = request.args.get(structure_item, DETECT_DEFAULT_MARK)
        structure_list[structure_item] = structure_mark
        if structure_mark != '0':
            structure_condition_num += 1
    struture_condition_num = len(structure_list)
    structure_weight = request.args.get('structure_weight', DETECT_DEFAULT_WEIGHT) #default weight 0.5
    structure_weight = float(structure_weight)
    if struture_condition_num==0:
        attribute_weight = 0
    query_dict['structure'] = structure_list
    query_dict['structure_weight'] = structure_weight
    #get query_dict: text
    text_query_list = []
    for text_item in DETECT_TEXT_FUZZ_ITEM:
        item_value_string = request.args.get(text_item, '') # a string joint by ' '
        item_value_list = item_value_string.split(' ')
        if len(item_value_list) > 0 and item_value_string != '':
            nest_body_list = []
            for item_value in item_value_list:
                nest_body_list.append({'wildcard':{text_item: '*'+item_value+'*'}})
            text_query_list.append({'bool':{'should':nest_body_list}})
    for text_item in DETECT_TEXT_RANGE_ITEM:
        item_value_from = request.args.get(text_item+'_from', '')
        item_value_to = request.args.get(text_item+'_to', '')
        if item_value_from!='' and item_value_to != '':
            if int(item_value_from) > int(item_value_to):
                return 'invalid input for range'
            else:
                text_query_list.append({'range':{text_item:{'gte':int(item_value_from), 'lt':int(item_value_to)}}})

    query_dict['text'] = text_query_list
    #identify the query condition num at least one
    if attribute_condition_num + structure_condition_num == 0:
        return 'no query condition'
    #get query_dict: filter
    filter_dict = {} # filter_dict = {'count': 100, 'influence':{'from':0, 'to':50}, 'importance':{'from':0, 'to':50}}
    for filter_item in DETECT_QUERY_FILTER:
        if filter_item=='count':
            filter_item_value = request.args.get(filter_item, DETECT_DEFAULT_COUNT)
            filter_item_value = int(filter_item_value)
        else:
            filter_item_from = request.args.get(filter_item+'_from', DETECT_FILTER_VALUE_FROM)
            filter_item_to = request.args.get(filter_item+'_to', DETECT_FILTER_VALUE_TO)
            if int(filter_item_from) > int(filter_item_to):
                return 'invalid input for filter'
            filter_item_value = {'gte': int(filter_item_from), 'lt': int(filter_item_to)}
        filter_dict[filter_item] = filter_item_value
    if filter_dict['count'] == 0:
        return 'invalid input for count'
    query_dict['filter'] = filter_dict
    #get detect task information
    task_information_dict = {}
    task_information_dict['task_name'] = request.args.get('task_name', '')
    task_information_dict['submit_date'] = int(time.time())
    task_information_dict['state'] = request.args.get('state', '')
    task_information_dict['submit_user'] = request.args.get('submit_user', 'admin')
    task_information_dict['task_type'] = 'detect'   #type: detect/analysis
    task_information_dict['detect_type'] = 'single' #type: single/multi/attribute/event
    task_information_dict['detect_process'] = 0     #type: 0/20/50/70/100
    
    #save task information
    input_dict = {}
    input_dict['task_information'] = task_information_dict
    input_dict['query_condition'] = query_dict
    
    status = save_detect_single_task(input_dict)
    print 'single task success'
    return json.dumps(status)

# use to upload file to multi-person group detection
@mod.route('/multi_person/', methods=['GET', 'POST'])
def ajax_multi_person():
    results = {}
    query_dict = {} # query_dict = {'attribute':[], 'attribute_weight':0.5, 'structure':[], 'structure_weight':0.5, 'text':{} ,'filter':{}}
    task_information_dict = {} # task_information_dict = {'uid_list':[], 'task_name':xx, 'state':xx, 'submit_user':xx}
    input_dict = {}
    input_data = request.get_json()
    #upload user list
    upload_data = input_data['upload_data']
    line_list = upload_data.split('\n')
    uid_list = []
    for line in line_list:
        uid = line[:10]
        if len(uid)==10:
            uid_list.append(uid)
    task_information_dict['uid_list'] = uid_list
    if len(uid_list)==0:
        return 'no seed user'
    #task information
    task_information_dict['task_name'] = input_data['task_name']
    task_information_dict['state'] = input_data['state']
    task_information_dict['submit_date'] = int(time.time())
    task_information_dict['submit_user'] = input_data['submit_user']
    #identify whether to extend
    extend_mark = input_data['extend'] # extend_mark = 0/1
    if extend_mark == '0':
        task_information_dict['task_type'] = 'analysis'
        task_information_dict['status'] = 0
        input_dict['task_information'] = task_information_dict
        print 'no extend save'
        results = save_detect_multi_task(input_dict, extend_mark)
    else:
        print 'extend save'
        task_information_dict['task_type'] = 'detect'
        task_information_dict['detect_type'] = 'multi'
        task_information_dict['detect_process'] = 0
        #get query dict: attribute
        attribute_list = []
        for attribute_item in DETECT_QUERY_ATTRIBUTE:
            attribute_mark = input_data[attribute_item]
            if attribute_mark == '1':
                attribute_list.append(attribute_item)
        attribute_condition_num = len(attribute_list)
        if attribute_condition_num != 0:
            attribute_weight = input_data['attribute_weight']
        else:
            attribute_weight = 0
        query_dict['attribute_weight'] = float(attribute_weight)
        query_dict['attribute'] = attribute_list
        #get query dict: structure
        structure_list = {}
        for structure_item in DETECT_QUERY_STRUCTURE:
            structure_mark = input_data[attribute_item]
            structure_list[structure_item] = structure_mark
            if structure_mark != '0':
                structure_condition_num += 1
        
        structure_condition_num = len(structure_list)
        if structure_condition_num != 0:
            structure_weight = input_data['structure_weight']
        else:
            structure_weight = 0
        query_dict['structure_weight'] = float(structure_weight)
        query_dict['structure'] = structure_list
        #get query_dict: text
        text_query_list = []
        for text_item in DETECT_TEXT_FUZZ_ITEM:
            item_value_string = input_data[text_item] # a string joint by ' '
            item_value_list = item_value_string.split(' ')
            nest_body_list = []
            if len(item_value_list)>0 and item_value_string != '':
                for item_value in item_value_list:
                    nest_body_list.append({'wildcard':{text_item: '*'+item_value+'*'}})
                text_query_list.append({'bool':{'should':nest_body_list}})
        for text_item in DETECT_TEXT_RANGE_ITEM:
            try:
                item_value_from = input_data[text_item+'_from']
            except:
                item_value_from = ''
            try:
                item_value_to = input_data[text_item+'_to']
            except:
                iter_value_to = ''
            if item_value_from != '' and item_value_to != '':
                if int(item_value_from) > int(item_value_to):
                    return 'invalid input for range'
                else:
                    text_query_list.append({'range':{text_item:{'gte':int(item_value_from), 'lt':int(item_value_to)}}})
        query_dict['text'] = text_query_list
        #identify the comdition num at least 1
        if attribute_condition_num + structure_condition_num == 0:
            return 'no query condition'
        #get query dict: filter
        filter_dict = {} # filter_dict = {'count':100, 'influence':{'from':0, 'to':50}, 'importance':{'from':0, 'to':50}}
        filter_condition_num = 0
        for filter_item in DETECT_QUERY_FILTER:
            if filter_item == 'count':
                filter_item_value = input_data[filter_item]
                filter_item_value = int(filter_item_value)
                if filter_item_value != '0':
                    filter_condition_num += 1
            else:
                filter_item_from = input_data[filter_item+'_from']
                filter_item_to = input_data[filter_item+'_to']
                if int(filter_item_from) > int(filter_item_to):
                    return 'valid input for filter'
                if filter_item_to != '0':
                    filter_condition_num += 1
                filter_item_value = {'gte':int(filter_item_from), 'lt':int(filter_item_to)}
            filter_dict[filter_item] = filter_item_value
        if filter_condition_num == 0:
            return 'valid input for filter'
        query_dict['filter'] = filter_dict
        #save task information
        input_dict = {}
        input_dict['task_information'] = task_information_dict
        input_dict['query_condition'] = query_dict
        print 'views multi save'
        results = save_detect_multi_task(input_dict, extend_mark)
    results = json.dumps(results) # [True/False, out_user_list]
    return results

#use to group detect by attribute or pattern
@mod.route('/attribute_pattern/')
def ajax_attribute_pattern():
    results = {}
    input_dict = {} # input_dict = {'task_information':task_information_dict, 'query_dict': query_list}
    attribute_query_list = []
    pattern_query_list = [] 
    query_dict = {} # query_dict = {'attribute':attribute_query_list, 'pattern':pattern_query_list, 'filter':{}}
    condition_num = 0
    attribute_condition_num  = 0
    pattern_condition_num = 0
    #step1:get attribute query list
    #step1.1: fuzz item
    for item in DETECT_ATTRIBUTE_FUZZ_ITEM:
        item_value = request.args.get(item, '')
        if item_value:
            attribute_condition_num += 1
            attribute_query_list.append({'wildcard':{item: '*'+item_value+'*'}})
    #step1.2: multi select item
    for item in DETECT_ATTRIBUTE_MULTI_ITEM:
        nest_body_list = []
        item_value_string = request.args.get(item, '')
        if item_value_string != '':
            item_value_list = item_value_string.split(',')
            for item_value in item_value_list:
                nest_body_list.append({'wildcard':{item: '*'+item_value+'*'}})
            attribute_query_list.append({'bool':{'should': nest_body_list}})
            attribute_condition_num += 1
    #step1.3: select item
    for item in DETECT_ATTRIBUTE_SELECT_ITEM:
        if item=='tag':
            tag_string = request.args.get(item, '')
            if tag_string != '':
                tag_string_list = tag_string.split(',')
                for tag_item in tag_string_list:
                    tag_item_list = tag_item.split('-')
                    item_name = tag_item_list[0]
                    item_value = tag_item_list[1]
                if item_name and item_value:
                    attribute_condition_num += 1
                    attribute_query_list.append({'match':{item_name: item_value}})
        else:
            item_value = request.args.get(item, '')
            if item_value:
                attribute_condition_num += 1
                attribute_query_list.append({'match':{item: item_value}})
    query_dict['attribute'] = attribute_query_list
    #step2:get pattern query list
    #step2.1: fuzz item
    for item in DETECT_PATTERN_FUZZ_ITEM:
        item_value  = request.args.get(item, '')
        if item_value:
            pattern_condition_num += 1
            pattern_query_list.append({'wildcard':{item: '*'+item_value+'*'}})
    #step2.2: select item
    for item in DETECT_PATTERN_SELECT_ITEM:
        item_value_string = request.args.get(item, '')
        if item_value_string != '':
            item_value_list = item_value_string.split(',')
            nest_body_list = []
            for item_value in item_value_list:
                nest_body_list.append({'wildcard': {item: '*'+item_value+'*'}})
            pattern_condition_num += 1
            pattern_query_list.append({'bool':{'should': nest_body_list}})
    #step2.3: range item
    for item in DETECT_PATTERN_RANGE_ITEM:
        item_value_from = request.args.get(item+'_from', '')
        item_value_to = request.args.get(item+'_to', '')
        if item_value_from != '' and item_value_to != '':
            pattern_condition_num += 1
            if int(item_value_from) > int(item_value_to):
                return 'invalid input for condition'
            else:
                pattern_query_list.append({'range':{item:{'gte': int(item_value_from), 'lt':int(item_value_to)}}})
        
    #identify attribute and pattern condition num >= 1
    if attribute_condition_num + pattern_condition_num < 1:
        return 'invalid input for condition'
    query_dict['pattern'] = pattern_query_list
    #step3:get filter query dict
    filter_dict = {}
    for filter_item in DETECT_QUERY_FILTER:
        if filter_item=='count':
            filter_item_value = request.args.get(filter_item, DETECT_DEFAULT_COUNT)
            filter_item_value = int(filter_item_value)
        else:
            filter_item_from = request.args.get(filter_item+'_from', DETECT_FILTER_VALUE_FROM)
            filter_item_to = request.args.get(filter_item+'_to', DETECT_FILTER_VALUE_TO)
            if int(filter_item_from) > int(filter_item_to):
                return 'invalid input for filter'
            filter_item_value = {'gte': int(filter_item_from), 'lt':int(filter_item_to)}
        filter_dict[filter_item] = filter_item_value
    if filter_dict['count'] == 0:
        return 'invalid input for count'
    query_dict['filter'] = filter_dict
    #step4:get task information dict
    task_information_dict = {}
    task_information_dict['task_name'] = request.args.get('task_name', '')
    task_information_dict['state'] = request.args.get('state', '')
    task_information_dict['submit_user'] = request.args.get('submit_user', 'admin')
    task_information_dict['submit_date'] = int(time.time())
    task_information_dict['task_type'] = 'detect'
    task_information_dict['detect_type'] = 'attribute'
    task_information_dict['detect_process'] = 0
    #save task information
    input_dict = {}
    input_dict['task_information'] = task_information_dict
    input_dict['query_condition'] = query_dict

    status = save_detect_attribute_task(input_dict)
    return json.dumps(status)

#use to group detect by event
@mod.route('/event/')
def ajax_event_detect():
    results = {}
    query_dict = {} # {'attribute':attribute_query_list, 'event':event_query_list, 'filter':filter_dict}
    input_dict = {} # {'task_information':task_information_dict, 'query_dict': query_dict}
    attribute_query_list = []
    event_query_list = []
    query_condition_num = 0
    #step1: get attribtue query dict
    for item in DETECT_EVENT_ATTRIBUTE:
        item_value_string = request.args.get(item, '')
        if item_value_string != '':
            item_value_list = item_value_string.split(',')
            nest_body_list = []
            for item_value in item_value_list:
                nest_body_list.append({'wildcard':{item: '*'+item_value+'*'}})
            query_condition_num += 1
            attribute_query_list.append({'bool':{'should': nest_body_list}})

    query_dict['attribute']  = attribute_query_list
    #step2: get event query dict
    #step2.1: get event fuzz item
    for item in DETECT_TEXT_FUZZ_ITEM:
        item_value_string = request.args.get(item, '')
        item_value_list = item_value_string.split(' ')
        nest_body_list = []
        if item_value_string != '':
            for item_value in item_value_list:
                nest_body_list.append({'wildcard':{item: '*'+item_value+'*'}})
            event_query_list.append({'bool':{'should':nest_body_list}})
            query_condition_num += 1

    #step2.2: get event range item
    for item in DETECT_EVENT_TEXT_RANGE_ITEM:
        now_time = int(time.time())
        now_date_ts = datetime2ts(ts2datetime(now_time))
        item_value_from = request.args.get(item+'_from', now_date_ts - DAY)
        item_value_to = request.args.get(item+'_to', now_date_ts)
        if item_value_from != '' and item_value_to != '':
            if int(item_value_from) > int(item_value_to):
                return 'invalid input for range'
            else:
                query_condition_num += 1
                event_query_list.append({'range':{item: {'gte': int(item_value_from), 'lt':int(item_value_to)}}})
        else:
            return 'invalid input for range'
    query_dict['event'] =  event_query_list
    #identify the query condition at least 1
    if query_condition_num < 1:
        return 'invalid input for query'
    #step3: get filter dict
    filter_dict = {}
    for filter_item in DETECT_QUERY_FILTER:
        if filter_item == 'count':
            filter_item_value = request.args.get(filter_item, DETECT_DEFAULT_COUNT)
            filter_item_value = int(filter_item_value)
        else:
            filter_item_from = request.args.get(filter_item+'_from', DETECT_FILTER_VALUE_FROM)
            filter_item_to = request.args.get(filter_item+'_to', DETECT_FILTER_VALUE_TO)
            if int(filter_item_from) > int(filter_item_to) or (not item_value_from) or (not item_value_to):
                return 'invalid input for filter'
            filter_item_value = {'gte': int(filter_item_from), 'lt': int(filter_item_to)}
        filter_dict[filter_item] = filter_item_value
    if filter_dict['count'] == 0:
        return 'invalid input for count'
    query_dict['filter'] = filter_dict
    #step4: get task information dict
    task_information_dict = {}
    task_information_dict['task_name'] = request.args.get('task_name', '')
    task_information_dict['submit_date'] = int(time.time())
    task_information_dict['state'] = request.args.get('state', '')
    task_information_dict['submit_user'] = request.args.get('submit_user', 'admin')
    task_information_dict['task_type'] = 'detect'
    task_information_dict['detect_type'] = 'event'
    task_information_dict['detect_process'] = 0

    #step5: save to es and redis
    input_dict['task_information'] = task_information_dict
    input_dict['query_condition'] = query_dict

    status = save_detect_event_task(input_dict)
    
    return json.dumps(status)

#use to show group detect task information
#output: group detect task information list
@mod.route('/show_detect_task/')
def ajax_show_detect_task():
    results = show_detect_task()
    return json.dumps(results)

#use to search group detect task
#input: search condition
#output: group detect task information list
@mod.route('/search_detect_task/')
def ajax_search_detect_task():
    task_name = request.args.get('task_name', '')
    submit_date = request.args.get('submit_date', '')
    state = request.args.get('state', '')
    process = request.args.get('process', '')
    detect_type = request.args.get('detect_type', '')
    submit_user = request.args.get('submit_user', '')
    results = search_detect_task(task_name, submit_date, state, process, detect_type, submit_user)
    return json.dumps(results)

#use to show group detect task result
#input: task_name
#output: uid list
@mod.route('/show_detect_result/')
def ajax_show_detect_result():
    results = {}
    task_name = request.args.get('task_name', '')
    results = show_detect_result(task_name)
    return json.dumps(results)


#use to add detect task having been done to group analysis
#input: task_name, identify_uid_list
#output: results
@mod.route('/add_detect2analysis/',methods=['GET', 'POST'])
def ajax_add_detect2analysis():
    input_data = request.get_json() #input_data = {'uid_list':[], 'task_name':xx}
    results = detect2analysis(input_data)

    return json.dumps(results)

#use to delete detect task
@mod.route('/delete_task/')
def ajax_delete_task():
    status = True
    task_name = request.args.get('task_name', '')
    status = delete_task(task_name)
    return json.dumps(status)

#use to get social sensing group detect results
#input:
#output:
@mod.route('/show_sensing_task/') #获得所有的已经完成的社会感知任务列表
def ajax_socail_sensing():
    results = []
    results = show_social_sensing_task()
    return json.dumps(results)

@mod.route('/show_user_in_sensing_task/')
def ajax_show_user_in_sensing_task():
    task_name = request.args.get('task_name', '') # 获取某个任务名，返回相应重要的人
    results = show_important_users(task_name)

    return json.dumps(results)

#use to submit social sensing group to analysis
#input: get_json
#output:
@mod.route('/submit_sensing/', methods=['GET', 'POST'])
def ajax_submit_sensing():
    status = False
    input_dict = request.get_json() # input_dict ={'task_information': {'task_name':xx, 'uid_list':[], 'state':[], submit_user:admin'}}
    status = submit_sensing(input_dict)
    return json.dumps(status)
