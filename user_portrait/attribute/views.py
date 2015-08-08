#-*- coding:utf-8 -*-

import os
import time
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from search import search_attribute_portrait, search_location, search_mention, search_activity,\
                   search_attention, search_follower, search_portrait, get_geo_track
from search import delete_action, search_identify_uid
from search_daily_info import search_origin_attribute, search_retweeted_attribute, search_user_index
from search_mid import index_mid
from user_portrait.search_user_profile import es_get_source

# use to test 13-09-08
test_time = 1378569600

"""
item_dict = {'psycho_feature':{'dzz':u'胆汁质', 'dxz':u'多血质', 'nyz':u'粘液质', 'yyz':u'抑郁质'},\
             'psycho_status':{'pos':u'积极', 'neg':u'消极', 'anx':u'焦虑', 'ang':u'生气', 'sad':u'悲伤'}}
"""

mod = Blueprint('attribute', __name__, url_prefix='/attribute')

@mod.route('/portrait_attribute/')
def ajax_portrait_attribute():
    uid = request.args.get('uid', '')
    uid = str(uid)
    results = search_attribute_portrait(uid)
    if results:
        return json.dumps(results)
    else:
        return None


@mod.route('/portrait_search/')
def ajax_portrait_search():
    stype = request.args.get('stype', '')
    result = {}
    query_data = {}
    query = []
    query_list = []
    condition_num = 0
    if stype == '1':
        fuzz_item = ['uid', 'uname']
        item_data = request.args.get('term', '')
        #if item_data:
        for item in fuzz_item:
            #item_data = request.args.get(item, '')
            if item_data:
                query_list.append({'wildcard':{item:'*'+item_data+'*'}})
                condition_num += 1
        query.append({'bool':{'should':query_list}})
    else:
        fuzz_item = ['uid', 'uname', 'location', 'activity_geo', 'keywords', 'hashtag']
        select_item = ['gender', 'verified', 'psycho_feature', 'psycho_status']
        range_item = ['fansnum', 'statusnum', 'friendsnum', 'importance', 'activeness', 'influence']
        multi_item = ['topic', 'domain']
        for item in fuzz_item:
            item_data = request.args.get(item, '')
            if item_data:
                if item=='keywords':
                    item = 'keywords_string'
                #print 'item_data:', item_data, type(item_data)
                query.append({'wildcard':{item:'*'+item_data+'*'}})
                condition_num += 1
        for item in select_item:
            item_data = request.args.get(item, '')
            if item_data:
                query.append({'match':{item: item_data}})
                condition_num += 1
        '''
        for item in range_item:
            item_data_low = request.args.get(item+'low', '')
            item_data_up = request.args.get(item+'up', '')
            if not item_data_low:
                item_data_low = 0
            else:
                item_data_low = float(item_data_low)
            if not item_data_up:
                item_data_up = 10000000
            else:
                item_data_up = float(item_data_up)
            query.append({'range':{item:{'from':item_data_low, 'to':item_data_up}}})
            condition_num += 1
        '''
        for item in multi_item:
            nest_body = {}
            nest_body_list = []
            item_data = request.args.get(item, '')
            if item_data:
                term_list = item_data.split(',')
                for term in term_list:
                    nest_body_list.append({'match':{item: term}})
                condition_num += 1
                query.append({'bool':{'should':nest_body_list}})
        
    #size = request.args.get('size', 1000)
    size = 1000
    sort = '_score'
    #sort = request.args.get('sort', 'influence')
    print 'condition_num, query:', condition_num, query
    result = search_portrait(condition_num, query, sort, size)
    return json.dumps(result)


@mod.route('/location/')
def ajax_location():
    uid = request.args.get('uid', '')
    uid = str(uid)
    now_ts = time.time()
    # test
    now_ts = test_time
    results = search_location(now_ts, uid)
    if results:
        return json.dumps(results)
    else:
        return None

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
    if results:
        return json.dumps(results)
    else:
        return None

@mod.route('/attention/')
def ajax_attention():
    uid = request.args.get('uid', '')
    uid = str(uid)
    results = search_attention(uid)
    if results:
        return json.dumps(results)
    else:
        return None

@mod.route('/follower/')
def ajax_follower():
    uid = request.args.get('uid', '')
    uid = str(uid)
    results = search_follower(uid)
    if results:
        return json.dumps(results)
    else:
        return None

# get user geo track
@mod.route('/geo_track/')
def ajax_geo_track():
    uid = request.args.get('uid', '')
    uid = str(uid)
    results = get_geo_track(uid)
    if results:
        return json.dumps(results)
    else:
        return None

@mod.route('/identify_uid/')
def ajax_identify_uid():
    uid = request.args.get('uid', '')
    uid = str(uid)
    results = search_identify_uid(uid)
    return json.dumps(results)


@mod.route('/delete/')
def ajax_delete():
    uid_list = request.args.get('uids', '') # uids = [uid1, uid2]
    if uid_list:
        uid_list = json.loads(uid_list)
        status = delete_action(uid_list)
    return json.dumps(status)
        

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

    # test
    #date = '2013/09/01'
    #uid = '1713926427'

    date = str(date).replace('/', '')

    results = search_retweeted_attribute(date, uid)

    """
    returm mid content

    results['retweeted_weibo_top_retweeted_content'] = index_mid(results['retweeted_weibo_top_retweeted_id'])
    results['retweeted_weibo_top_comment_content'] = index_mid(results['retweeted_weibo_top_comment_id'])
    """

    return json.dumps(results)

@mod.route('/basic_info/')
def ajax_basic_info():
    uid = request.args.get('uid', '')
    uid = str(uid)

    # test 
    uid = '1713926427'


    results = es_get_source(uid)

    return json.dumps(results)

@mod.route('/user_index/')
def ajax_user_index():
    uid = request.args.get('uid', '')
    date = request.args.get('date', '')
    uid = str(uid)
    date = str(date).replace('/', '')

    results = search_user_index(date, uid)

    return json.dumps(results)

