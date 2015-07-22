#-*- coding:utf-8 -*-

import os
import time
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from utils import recommentation_in, identify_in, show_in_history, show_compute, identify_compute
from utils import show_out_uid,decide_out_uid, search_history_delete

from user_portrait.time_utils import datetime2ts

# use to test 13-09-08
test_time = 1378569600
test_date = '2013-09-07'

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
        #test
        # data = [('2013-09-07','1767905823')]
        results = identify_in(data) # success:1
        print 'results:', data
    return json.dumps(results)


#show recomment history
#input:date
@mod.route('/show_in_history/')
def ajax_show_in_history():
    results = {}
    date = request.args.get('date', '')
    input_ts = datetime2ts(date)
    now_ts = time.time()
    now_ts = test_time
    if now_ts - 24*3600*7 > input_ts:
        return None
    else:
        results = show_in_history(date)
    return json.dumps(results)


#show uid has not compute but have been identify in
@mod.route('/show_compute/')
def ajax_compute_show():
    results = {}
    date = request.args.get('date','')
    if date:
        results = show_compute(date)
    for item in results:
        results[item] = json.loads(results[item])
    print results
    return json.dumps(results)

#identify the uid :list to compute
@mod.route('/identify_compute/')
def ajax_compute_identify():
    results = {}
    data = request.args.get('data', '') # data '[(date, uid)]'
    if data:
        #test
        data = [('2015-07-15','1767905823')]
        results = identify_compute(data)
    return json.dumps(results)

# show recommentaion out uid
@mod.route('/show_out/')
def ajax_recommentation_out():
    results = []
    date = request.args.get('date', '') # date 2013-09-01
    if date:
        results = show_out_uid(date)
    return json.dumps(results)

# identify recommentation out uid
@mod.route('/identify_out/')
def ajax_identify_out():
    results = 0
    data = request.args.get('data', '') # uid,uid,uid
    results = decide_out_uid(data)

    return json.dumps(results)

# show history delete out uid
@mod.route('/history_delete/')
def ajax_history_delete():
    results = {}
    date = request.args.get('date', '') # date 2013-09-01, 2013-09-02
    results = search_history_delete(date)

    return results # return {"20150715": "[uid]"}

@mod.route('/cancel_delete/')
def ajax_cancel_delete():
    data = request.args.get('data','') # uid,uid
    date = request.args.get('date', '') # date, 2013-09-01
    if not data or not date:
        return "no one cancelled"
    else:
        uid_list = data.split(',')
        date = date.replace('-','')
        delete_list = json.loads(hget('decide_delete_list',date))
        revise_list = list(set(delete_list).difference(set(uid_list)))
        hset('decide_delete_list', date, json.dumps(revise_list))

    return 1
