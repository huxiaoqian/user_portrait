#-*- coding:utf-8 -*-

import os
import time
import json
from werkzeug import secure_filename
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect, send_from_directory
from utils import submit_task, search_task, get_group_results, get_group_list, delete_group_results
from user_portrait.global_config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from user_portrait.search_user_profile import es_get_source
from user_portrait.time_utils import ts2datetime

mod = Blueprint('group', __name__, url_prefix='/group')

# use to upload file
@mod.route('/upload_file/', methods=['GET', 'POST'])
def upload_file():
    upload_data = request.form['upload_data']
    task_name = request.form['task_name']
    state = request.form['state']
    now_ts = time.time()
    now_date = ts2datetime(now_ts)
    line_list = upload_data.split('\n')
    input_data = {}
    input_data['submit_date'] = now_date
    input_data['task_name'] = task_name
    input_data['state'] = state
    uid_list = []
    for line in line_list:
        uid = line[:10]
        if len(uid)==10:
            uid_list.append(uid)
            #print 'uid:', uid
    #print 'len uid list:', len(uid_list)
    input_data['uid_list'] = uid_list
    status = submit_task(input_data)
    return json.dumps(status)


# submit group analysis task and save to redis as lists
# submit group task: task name should be unique
# input_data is dict ---two types
# one type: {'submit_date':x, 'state': x, 'uid_list':[],'task_name':x}
# two type: {'submit_date':x, 'state': x, 'task_name':x, 'uid_file':filename}
@mod.route('/submit_task/',methods=['GET', 'POST'])
def ajax_submit_task():
    input_data = dict()
    """
    input_data['task_name'] = request.args.get('task_name', '')
    input_data['uid_list'] = request.args.get('uid_list', '') # uid_list=[uid1, uid2]
    input_data['submit_date'] = request.args.get('submit_date', '')
    input_data['state'] = request.args.get('state', '')
    """
    input_data = request.get_json()
    #print input_data, type(input_data)
    now_ts = time.time()
    now_date = ts2datetime(now_ts)
    input_data['submit_date'] = now_date
    status = submit_task(input_data)
    return json.dumps(status)

# show the group task table
@mod.route('/show_task/')
def ajax_show_task():
    results = {}
    task_name = request.args.get('task_name', '')
    submit_date = request.args.get('submit_date', '')
    state = request.args.get('state', '')
    status = request.args.get('status', '')
    results = search_task(task_name, submit_date, state, status)
    return json.dumps(results)


# show the group analysis result---different module
@mod.route('/show_group_result/')
def ajax_show_group_result_basic():
    results = {}
    task_name = request.args.get('task_name', '')
    module = request.args.get('module', 'basic')
    results = get_group_results(task_name, module)
    #print 'result:', results
    return json.dumps(results)

#show the group member list
@mod.route('/show_group_list/')
def sjax_show_group_list():
    results = []
    task_name = request.args.get('task_name', '')
    results = get_group_list(task_name)
    return json.dumps(results)

# delete the group task
@mod.route('/delete_group_task/')
def ajax_delete_group_task():
    results = {}
    task_name = request.args.get('task_name', '')
    results = delete_group_results(task_name)
    return json.dumps(results)

'''
below: track a group analysis result
deal procession:
work1: submit track a group analysis task
work2: search the track task-----a table
work3: look the track results
work4: end a track task
work5: delete a track task results
add a field to mark the group analysis task is track or once
add track group analysis information to overview
'''

# submit task to track a group analysis result
@mod.route('/submit_track_task/')
def ajax_submit_track_task():
    results = {}
    return json.dumps(results)

# search track task
@mod.route('/search_track_task/')
def ajax_search_track_task():
    results = {}
    return json.dumps(results)

# get the track results
@mod.route('/track_track_results/')
def ajax_get_track_results():
    results = {}
    return json.dumps()

# end a track task
@mod.route('/end_track_task/')
def ajax_end_track_task():
    results = {}
    return json.dumps(results)

# delete a track task results
@mod.route('delete_track_results')
def ajax_delete_track_tresults():
    results = {}
    return json.dumps(results)
