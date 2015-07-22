#-*- coding:utf-8 -*-

import os
import time
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from utils import submit_task, get_group_results, delete_group_results

from user_portrait.search_user_profile import es_get_source

mod = Blueprint('group', __name__, url_prefix='/group')

# submit group analysis task and save to redis as lists
@mod.route('/submit_task/')
def ajax_submit_task():
    input_data = dict()
    input_data['task_name'] = request.args.get('task_name', '')
    input_data['uid_list'] = request.args.get('uid_list', '') # uid_list=[uid1, uid2]
    input_data['submit_ts'] = request.args.get('submit_ts', '')
    input_data['state'] = request.args.get('state', '')
    status = submit_task(input_data)
    return status

# show the group task table
@mod.route('/show_task/')
def ajax_show_task():
    results = {}
    task_name = request.args.get('task_name', '')
    submit_date = request.args.get('submit_date', '')
    
    return json.dumps(results)


# show the group analysis result
@mod.route('/show_group_result/')
def ajax_show_group_result():
    task_name = request.args.get('task_name', '')
    results = get_group_results(task_name)
    if results:
        return json.dumps(results)
    else:
        return None

# delete the group task
@mod.route('/delete_group_task/')
def ajax_delete_group_task():
    task_name = request.args.get('task_name', '')
    results = delete_group_results(task_name)
    if results:
        return json.dumps(results)
    else:
        return None
