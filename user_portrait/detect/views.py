#-*- coding:utf-8 -*-

import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect, send_from_directory
from utils import single_detect

from user_portrait.global_config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from user_portrait.time_utils import ts2datetime

mod = Blueprint('detect', __name__, url_prefix='/detect')

# use to submit parameter single-person group detection
@mod.route('/single_person/')
def ajax_single_parameter():
    results = {}
    results = single_detect()
    return results




# use to upload file to multi-person group detection
@mod.route('/upload_file/', methods=['GET', 'POST'])
def upload_file():
    results = {}
    upload_data = request.form['upload_data']
    task_name = request.form['task_name']
    state = request.form['state']
    now_ts = time.time()
    now_date = ts2datetime(now_ts)
    return results
