#-*- coding:utf-8 -*-

import os
import time
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from search import search_location, search_mention, search_activity,\
                   search_attention, search_follower
from search_daily_info import search_origin_attribute, search_retweeted_attribute, search_fans_attribute

# use to test 13-09-08
test_time = 1378569600

mod = Blueprint('attribute', __name__, url_prefix='/attribute')

@mod.route('/location/')
def ajax_location():
    uid = request.args.get('uid', '')
    uid = str(uid)
    now_ts = time.time()
    # test
    now_ts = test_time
    results = search_location(now_ts, uid)
        
    return json.dumps(results)

@mod.route('/mention/')
def ajax_mention():
    uid = request.args.get('uid', '')
    uid = str(uid)
    now_ts = time.time()
    # test
    now_ts = test_time
    results = search_mention(now_ts, uid)

    return json.dumps(results)

@mod.route('/activity/')
def ajax_activity():
    uid = request.args.get('uid', '')
    uid = str(uid)
    now_ts = time.time()
    # test
    now_ts = test_time
    results = search_activity(now_ts, uid)

    return json.dumps(results)

@mod.route('/attention/')
def ajax_attention():
    uid = request.args.get('uid', '')
    uid = str(uid)
    results = search_attention(uid)

    return json.dumps(results)

@mod.route('/follower/')
def ajax_follower():
    uid = request.args.get('uid', '')
    uid = str(uid)
    results = search_follower(uid)

    return json.dumps(results)

"""
attention: the format of date from request must be vertified
format : '2015/07/04'

"""

@mod.route('/origin_weibo/')
def ajax_origin_weibo():
    uid = request.args.get('uid', '')
    date = request.args.get('date', '') # which day you want to see
    uid = str(uid)
    date = str(date).replace('/', '')

    results = search_origin_attribute(date, uid)

    return json.dumps(results)

@mod.route('/retweeted_weibo/')
def ajax_retweet_weibo():
    uid = request.args.get('uid', '')
    date = request.args.get('date', '')
    uid = str(uid)
    date = str(date).replace('/', '')

    results = search_retweeted_attribute(date, uid)

    return json.dumps(results)

@mod.route('/fans_number/')
def ajax_fans_number():
    uid = request.args.get('uid', '')
    date = request.args.get('date', '')
    uid = str(uid)
    date = str(date).replace('/', '')

    results = search_fans_attribute(date, uid)

    return json.dumps(results)



