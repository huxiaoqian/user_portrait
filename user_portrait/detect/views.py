#-*- coding:utf-8 -*-

import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect, send_from_directory
from utils import save_detect_single_task, save_detect_multi_task ,\
                  save_detect_task, show_detect_task, detect2analysis

from user_portrait.global_config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from user_portrait.parameter import DETECT_QUERY_ATTRIBUTE, DETECT_QUERY_STRUCTURE,\
                                    DETECT_QUERY_FILTER, DETECT_DEFAULT_WEIGHT, \
                                    DETECT_DEFAULT_MARK, DETECT_DEFAULT_COUNT, \
                                    DETECT_FILTER_VALUE_FROM, DETECT_FILTER_VALUE_TO
from user_portrait.time_utils import ts2datetime

mod = Blueprint('detect', __name__, url_prefix='/detect')

# use to submit parameter single-person group detection
@mod.route('/single_person/')
def ajax_single_person():
    results = {}
    query_dict = {}   #query_dict = {'task_information':{}, 'seed_user':{},'attribute':[],'attribute_weight': 0.5,'struture':[], 'structure_weight': 0.5, 'filter':{}}
    condition_num = 0 #condition_num != 0
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
            attribute_list.append(attribute_mark)
    attribute_condition_num = len(attribute_list)
    attribute_weight = request.args.get('attribute_weight', DETECT_DEFAULT_WEIGHT) #default weight: 0.5
    if attribute_condition_num==0:
        attribute_weight = 0
    query_dict['attribute'] = attribute_list
    query_dict['attribute_weight'] = attribute_weight
    #get query_dict: strucure
    struture_list = []
    for stucture_item in DETECT_QUERY_STURCTURE:
        structure_mark = request.args.get(struture_item, DETECT_DEFAULT_MARK)
        if structure_mark == '1':
            structure_list.append(structure_mark)
    struture_condition_num = len(structure_list)
    structure_weight = request.args.get('structure_weight', DETECT_DEFAULT_WEIGHT) #default weight 0.5
    if struture_condition_num==0:
        attribute_weight = 0
    query_dict['structure'] = structure_list
    query_dict['structure_weight'] = structure_weight
    #identify the query condition num at least one
    if attribute_condition_num + stucture_condition_num == 0:
        return 'no query condition'
    #get query_dict: filter
    filter_dict = {} # filter_dict = {'count': 100, 'influence':{'from':0, 'to':50}, 'importance':{'from':0, 'to':50}}
    for filter_item in DETECT_DEFAULT_FILTER:
        if filter_item=='count':
            filter_item_value = request.args.get(filter_item, DETECT_DEFAULT_COUNT)
        else:
            filter_item_from = request.args.get(filter_item+'_from', DETECT_FILTER_VALUE_FROM)
            filter_item_to = request.args.get(filter_item+'_to', DETECT_FILTER_VALUE_TO)
            if int(filter_item_from) > int(filter_item_to):
                return 'valid input for ' + filter_item
            filter_item_value = {'from': filter_item_from, 'to': filter_item_to}
        filter_dict[filter_item] = filter_item_value
    if filter_dict['count'] == 0:
        return 'valid input for count'
    query_dict['filter'] = filter_dict
    #get detect task information
    task_name = request.args.get('task_name', '')
    submit_date = time.time()
    state = request.args.get('state', '')
    submit_user = request.args.get('submit_user', 'admin')
    task_information_dict = {'task_name':task_name, 'submit_date':submit_date, 'state':state, 'submit_user':submit_user}
    #save task information
    query_dict['task_information'] = task_information_dict
    status = save_detect_single_task(query_dict)
    
    return status

# use to upload file to multi-person group detection
@mod.route('/multi_person/', methods=['GET', 'POST'])
def ajax_multi_person():
    results = {}
    upload_data = request.form['upload_data']
    task_name = request.form['task_name']
    state = request.form['state']
    now_ts = time.time()
    now_date = ts2datetime(now_ts)
    results = save_detect_task()
    return results

#use to group detect by attribute or pattern
@mod.route('/attribute_pattern/')
def ajax_attribute_pattern():
    results = {}
    results = save_detect_task()
    return results

#use to group detect by event
@mod.route('/event/')
def ajax_event_detect():
    results = {}
    results = save_detect_task()
    return results

#use to show group detect task information
@mod.route('/show_detect_task/')
def ajax_show_detect_task():
    results = {}
    results = show_detect_task()
    return results

#use to add detect task having been done to group analysis
@mod.route('/add_detect2analysis/')
def ajax_add_detect2analysis():
    results = {}
    results = detect2analysis()
    return results
