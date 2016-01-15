#-*- coding:utf-8 -*-

import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect, send_from_directory
from utils import save_detect_task, show_detect_task

from user_portrait.global_config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from user_portrait.time_utils import ts2datetime

mod = Blueprint('detect', __name__, url_prefix='/detect')

# use to submit parameter single-person group detection
@mod.route('/single_person/')
def ajax_single_person():
    results = {}
    results = save_detect_task()
    return results

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
