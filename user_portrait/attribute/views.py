#-*- coding:utf-8 -*-

import os
import time
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from search import search_location, search_mention, search_activity,\
                   search_attention, search_follower
from search_daily_info import search_origin_attribute, search_retweeted_attribute, search_fans_attribute
from search_mid import index_mid
from user_portrait.search_user_profile import es_get_source

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

    # test
    date = '2013/09/01'
    uid = '1713926427'

    date = str(date).replace('/', '')

    results = search_origin_attribute(date, uid)

    """
    results['origin_weibo_top_retweeted_comtent'] = index_mid(results["origin_weibo_top_retweeted_id"])
    results['origin_weibo_top_comment_content'] = index_mid(results["origin_weibo_top_comment_id"])
    """

    return json.dumps(results)

@mod.route('/retweeted_weibo/')
def ajax_retweetd_weibo():
    uid = request.args.get('uid', '')
    date = request.args.get('date', '')
    uid = str(uid)
    date = str(date).replace('/', '')

    results = search_retweeted_attribute(date, uid)

    """
    results['retweeted_weibo_top_retweeted_content'] = index_mid(results['retweeted_weibo_top_retweeted_id'])
    results['retweeted_weibo_top_comment_content'] = index_mid(results['retweeted_weibo_top_comment_id'])
    """

    return json.dumps(results)

@mod.route('/basic_info/')
def ajax_basic_info():
    uid = request.args.get('uid', '')
    date = request.args.get('date', '')
    uid = str(uid)

    # test 
    date = '2013/09/01'
    uid = '1713926427'

    date = str(date).replace('/', '')

    fans = search_fans_attribute(date, uid)
    results = es_get_source(uid)
    results['fansnum'] = fans['user_fansnum']
    return json.dumps(results)


