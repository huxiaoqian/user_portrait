#-*- coding:utf-8 -*-

import os
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from search import search_location, search_mention, search_activity,\
                   search_attention, search_follower

# use to test 13-09-08
test_time = 1378569600

mod = Blueprint('attribtue', __name__, url_prefix='/attribute')

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


