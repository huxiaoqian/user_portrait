#-*- coding:utf-8 -*-

import os
import time
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from utils import recommentation_in, identify_in, show_compute, identify_compute

from user_portrait.time_utils import datetime2ts

# use to test 13-09-08
test_time = 1378569600
test_date = '2013-09-08'

mod = Blueprint('recommentation', __name__, url_prefix='/recommentation')

@mod.route('/show_in/')
def ajax_recommentation_in():
    date = request.args.get('date', '') # '2013-09-01'
    # test
    date = test_date 
    input_ts = datetime2ts(date)
    now_ts = time.time()
    now_ts = test_time
    if now_ts - 3600*24*7 > input_ts:
        return None
    else:
        results = recommentation_in(input_ts)

        return json.dumps(results)


# identify_in 
# input:[(date, uid)]
# deal :write to compute
@mod.route('/identify_in/')
def ajax_identify_in():
    results = 0 # mark fail
    data = request.args.get('data','') # data '[(date, uid)]'
    data = json.loads(data)
    if data:
        results = identify_in(data) # success:1
    return json.dumps(results)


#show uid has not compute but have been identify in
@mod.route('/show_compute/')
def ajax_compute_show():
    results = {}
    date = request.args.get('date','')
    if date:
        results = show_compute(date)
    return json.dumps(results)

#identify the uid list to compute
@mod.route('/identify_compute/')
def ajax_compute_identify():
    results = {}
    data = request.args.get('date', '') # data '[(date, uid)]'
    if data:
        results = identify_compute(data)
    return json.dumps(results)

# show recommentaion out uid
@mod.route('/show_out/')
def ajax_recommentation_out():
    results = dict()
    return json.dumps(results)

# identify recommentation out uid
@mod.route('/identify_out/')
def ajax_identify_out():
    results = 0
    return json.dumps(results)
