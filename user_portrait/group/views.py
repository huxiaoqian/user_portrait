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
#test_time = 1378569600

mod = Blueprint('group', __name__, url_prefix='/group')

@mod.route('/location/')
def ajax_location():
    uid_list = ['1713926427','1798289842']
    uid = request.args.get('uid', '')
    date = request.args.get('date', '')
    uid = str(uid)
    uid_list.append(uid)
    results = dict()
    count = 0
    for i in uid_list:
        result = search_location(date, i)
        for k,v in result.items():
            for key in v:
                count += v[key]
            results[k] = count
    return json.dumps(results)
@mod.route('/mention/')
def ajax_mention():
    uid_list = ['1713926427']
    uid = request.args.get('uid', '')
    uid = str(uid)
    uid_list.append(uid)
    date = request.args.get('date', '')
    results = dict()
    for i in uid_list:
        result = search_mention(date, i)
        if result == None:
            continue
        else:
            for k,v in result.items():
                if k in results.keys():
                    try:
                        results[k] += v
                    except:
                        continue
                else:
                    results[k] = v
    return json.dumps(results)

@mod.route('/activity/')
def ajax_activity():
    uid_list = ['1713926427']
    uid = request.args.get('uid', '')
    uid = str(uid)
    uid_list.append(uid)
    date = request.args.get('date', '')
    results = dict()
    for i in uid_list:
        result = search_activity(date, i)
        for k,v in result.items():
            if k in results.keys():
                try:
                    results[k] += v
                except:
                    continue
            else:
                results[k] = v
    return json.dumps(results)

@mod.route('/attention/')
def ajax_attention():
    uid_list = ['1713926427']
    uid = request.args.get('uid', '')
    uid = str(uid)
    uid_list.append(uid)
    results = dict()
    for i in uid_list:
        result = search_attention(i)
        for k,v in result.items():
            if k in results.keys():
                try:
                    results[k] += v
                except:
                    continue
            else:
                results[k] = v
    return json.dumps(results)

@mod.route('/follower/')
def ajax_follower():
    uid_list = ['1798289842']
    uid = request.args.get('uid', '')
    uid = str(uid)
    uid_list.append(uid)
    results = dict()
    for i in uid_list:
        result = search_follower(i)
        if result == None:
            continue
        else:
            for k,v in result.items():
                if k in results.keys():
                    try:
                        results[k] += v
                    except:
                        continue
                else:
                    results[k] = v
    return json.dumps(results)

"""
attention: the format of date from request must be vertified
format : '2015/07/04'
"""

@mod.route('/origin_weibo/')
def ajax_origin_weibo():
    uid_list = ['1713926427']
    uid = request.args.get('uid', '')
    date = request.args.get('date', '') # which day you want to see
    uid = str(uid)
    uid_list.append(uid)
    results = dict()
    date = str(date).replace('/', '')
    for i in uid_list:
        result = search_origin_attribute(date, i)
        for k,v in result.items():
            if k in results.keys():
                try:
                    results[k] += v
                except:
                    continue
            else:
                results[k] = v
    return json.dumps(results)

@mod.route('/retweeted_weibo/')
def ajax_retweetd_weibo():
    uid_list = ['1798289842']
    uid = request.args.get('uid', '')
    date = request.args.get('date', '')
    uid = str(uid)
    date = str(date).replace('/', '')
    uid_list.append(uid)
    results = dict()
    for i in uid_list:
        result = search_retweeted_attribute(date, i)
        for k,v in result.items():
            if k in results.keys():
                try:
                    results[k] += v
                except:
                    continue
            else:
                results[k] = v
    return json.dumps(results)
    """
    results['retweeted_weibo_top_retweeted_content'] = index_mid(results['retweeted_weibo_top_retweeted_id'])
    results['retweeted_weibo_top_comment_content'] = index_mid(results['retweeted_weibo_top_comment_id'])
    """

    
                        
@mod.route('/basic_info/')
def ajax_basic_info():
    uid_list = ['1798289842']
    uid = request.args.get('uid', '')
    date = request.args.get('date', '')
    uid = str(uid)
    uid_list.append(uid)
    # test  
    #date = '2013/09/01'
    #uid = '1713926427'

    date = str(date).replace('/', '')
    results = dict()
    for i in uid_list:
        fans = search_fans_attribute(date, i)
        result = es_get_source(i)
        for k,v in result.items():
            if k in results.keys():
                try:
                    results[k] += v
                except:
                    continue
            else:
                results[k] = v
        results['fansnum'] = fans['user_fansnum']
    #fans = search_fans_attribute(date, uid)
    #results = es_get_source(uid)
    #results['fansnum'] = fans['user_fansnum']
    return json.dumps(results)
