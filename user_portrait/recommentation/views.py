#-*- coding:utf-8 -*-

import os
import redis
import time
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from utils import recommentation_in, identify_in, show_in_history, show_compute, identify_compute
from utils import show_out_uid,decide_out_uid, search_history_delete
from user_portrait.global_utils import R_RECOMMENTATION_OUT as r_out
from user_portrait.time_utils import datetime2ts
from update_activeness_record import update_record_index

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
    '''
    data = request.args.get('data','') # data '[(date, uid)]'
    data = json.loads(data)
    if data:
        #test
        # data = [('2013-09-07','1767905823')]
        results = identify_in(data) # success:1
        print 'results:', data
    '''
    date = request.args.get('date', '') # date = '2013-09-07'
    uid_string = request.args.get('uid_list', '')
    uid_list = uid_string.split(',')
    data = []
    if date and uid_list:
        #test
        #date = '2013-09-07'
        for uid in uid_list:
            data.append([date, uid])
        results = identify_in(data)
        print 'results:', results
    else:
        results = None
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
    results = []
    date = request.args.get('date','')
    if date:
        results = show_compute(date)
    return json.dumps(results)

#identify the uid :list to compute
@mod.route('/identify_compute/')
def ajax_compute_identify():
    results = {}
    date = request.args.get('date', '') # 'date1, date2'
    uid_string = request.args.get('uid_list', '') # 'uid1, uid2'
    input_data = []
    if date and uid_string:
        #test
        #input_data = [('2015-07-15','1767905823')]
        date_list = date.split(',')
        uid_list = uid_string.split(',')
        for i in range(0,len(date_list)):
            date = date_list[i]
            uid = uid_list[i]
            input_data.append([date ,uid])
        print 'input_data:', input_data
        results = identify_compute(input_data)
    return json.dumps(results)

# show recommentaion out uid
@mod.route('/show_out/')
def ajax_recommentation_out():
    results = []
    date = request.args.get('date', '') # date 2013-09-01
    fields = request.args.get('fields','')
    if fields:
        fields = fields.split(',')
    if date and fields:
        results = show_out_uid(date, fields)
    return json.dumps(results)

# identify recommentation out uid
@mod.route('/identify_out/')
def ajax_identify_out():
    results = 0
    date = request.args.get("date", '') # date, 2015-07-25
    data = request.args.get('data', '') # uid,uid,uid
    if date and data:
        date = date.replace('-','')
        results = decide_out_uid(date, data)

    return json.dumps(results)

# show history delete out uid
@mod.route('/history_delete/')
def ajax_history_delete():
    results = {}
    date = request.args.get('date', '') # date 2013-09-01
    date = date.replace('-', '')
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
        delete_list = json.loads(r_out.hget('decide_delete_list',date))
        revise_list = list(set(delete_list).difference(set(uid_list)))
        r_out.hset('decide_delete_list', date, json.dumps(revise_list))

        delete_list = json.loads(r_out.hget('history_delete_list',date))
        revise_list = list(set(delete_list).difference(set(uid_list)))
        r_out.hset('history_delete_list',date, json.dumps(revise_list))

        #update_record_index(uid_list) temporary 

    return json.dumps(1)

@mod.route('/search_delete/')
def ajax_search_delete():
    date = request.args.get('date', '') # date, 2013-09-01
    uid_list = request.args.get('uid_list', '') # uid_list, 12345,123456,

    if not date or not uid_list:
        return "no define date or uid_list"
    else:
        date = str(date).replace('-')
        remove_list = str(uid_list).split(',')

        temp = r_out.hget('decide_delete_list', date)
        if temp:
            exist_data = json.loads(r_out.hget('decide_delete_list',date))
            remove_list.extend(exist_data)
        r_out.hset('decide_delete_list', date, json.dumps(remove_list))

        delte_list = str(uid_list).split(',')
        temp = r_out.hget('history_delete_list', date)
        if temp:
            exist_data = json.loads(r_out.hget('history_delete_list',date))
            delete_list.extend(exist_data)
        r_out.hset('history_delete_list',date, json.dumps(delete_list))

    return json.dumps(1)

@mod.route('/cancel_recommend_out/')
def ajax_cancel_recommend_out():
    date = request.args.get('date', '') # date, 2013-09-01
    uid_list = request.args.get('uid_list', '') # uid_list, 12345,123456,

    if not date or not uid_list:
        return "no define date or uid_list"
    else:
        date = str(date).replace('-')
        uid_list = str(uid_list).split(',')

        recommend_list = r_out.hget('recommend_delete_list',date)
        revise_list = list(set(recommend_list).difference(set(uid_list)))
        r_out.hset('recommend_delete_list',date, json.dumps(revise_list))

        update_record_index(uid_list)

    return json.dumps(1)

