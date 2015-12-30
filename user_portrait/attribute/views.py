#-*- coding:utf-8 -*-

import os
import time
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from search import search_attribute_portrait, search_location, search_ip, search_mention, search_activity,\
                   search_attention, search_follower, search_portrait, get_geo_track, get_geo_track_ip, get_online_pattern
from search import delete_action, search_identify_uid, get_activeness_trend
from search import get_activity_weibo, search_comment, search_be_comment
from search import search_bidirect_interaction, search_preference_attribute, search_sentiment_trend, search_tendency_psy
from search import search_sentiment_weibo, get_influence_trend, search_remark, edit_remark
from search_daily_info import search_origin_attribute, search_retweeted_attribute, search_user_index
from search_mid import index_mid
from user_portrait.search_user_profile import es_get_source
from user_portrait.global_utils import es_user_portrait as es
from user_portrait.parameter import SOCIAL_DEFAULT_COUNT, SENTIMENT_TREND_DEFAULT_TYPE
from user_portrait.parameter import DEFAULT_SENTIMENT, DAY
from personal_influence import get_user_influence, influenced_detail, influenced_people, influenced_user_detail, statistics_influence_people, tag_vector, comment_on_influence, detail_weibo_influence, influence_summary
from description import conclusion_on_influence
# use to test 13-09-08
test_time = 1378569600

# custom_attribute
attribute_index_name = 'custom_attribute'
attribute_index_type = 'attribute'

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


#get preference attribute
#write in version: 15-12-08
#input: uid
#output: keywords, hashtag, domain, topic
@mod.route('/preference/')
def ajax_preference():
    uid = request.args.get('uid', '')
    uid = str(uid)
    results = search_preference_attribute(uid)
    if not results:
        results = {}
    return json.dumps(results)


#edit user remark
#write in version: 15-12-08
#input: uid, remark
#output: status
@mod.route('/edit_remark/')
def ajax_edit_remark():
    uid = request.args.get('uid', '')
    uid = str(uid)
    remark = request.args.get('remark', '')
    results = edit_remark(uid, remark) # results = 'yes' or 'no uid'
    return  results

#input remark
#write in version: 15-12-08
#input: uid
#output: remark
@mod.route('/get_remark/')
def ajax_get_remark():
    uid = request.args.get('uid', '')
    uid = str(uid)
    results = search_remark(uid)
    if not results:
        results = ''
    return json.dumps(results)

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
        for item in fuzz_item:
            if item_data:
                query_list.append({'wildcard':{item:'*'+item_data+'*'}})
                condition_num += 1
        query.append({'bool':{'should':query_list}})
    else:
        fuzz_item = ['uid', 'uname', 'location', 'activity_geo', 'keywords', 'hashtag']
        select_item = ['gender', 'verified', 'psycho_feature', 'psycho_status']
        range_item = ['fansnum', 'statusnum', 'friendsnum', 'importance', 'activeness', 'influence']
        multi_item = ['topic_string', 'domain']
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
        # custom_attribute
        tag_items = request.args.get('tag', '')
        if tag_items != '':
            tag_item_list = tag_items.split(',')
            for tag_item in tag_item_list:
                attribute_name_value = tag_item.split(':')
                attribute_name = attribute_name_value[0]
                attribute_value = attribute_name_value[1]
                if attribute_name and attribute_value:
                    query.append({'wildcard':{attribute_name:'*'+attribute_value+'*'}})
                    condition_num += 1

        for item in multi_item:
            nest_body = {}
            nest_body_list = []
            item_data = request.args.get(item, '')
            if item_data:
                term_list = item_data.split(',')
                for term in term_list:
                    nest_body_list.append({'wildcard':{item:'*'+term+'*'}})
                condition_num += 1
                query.append({'bool':{'should':nest_body_list}})
        
        
    #size = request.args.get('size', 1000)
    size = 1000
    sort = '_score'
    #sort = request.args.get('sort', 'influence')
    #print 'condition_num, query:', condition_num, query
    result = search_portrait(condition_num, query, sort, size)
    return json.dumps(result)

#use to get activity geo from user_portrait for week and month
#write in version:15-12-08
#input:uid and time type--day or week or month
#output:day geo or week geo track+conclusion(about activity geo module) or month geo track+month top 
@mod.route('/location/')
def ajax_location():
    uid = request.args.get('uid', '')
    uid = str(uid)
    time_type = request.args.get('time_type', '') # type = day; week; month
    now_ts = time.time()
    # test
    now_ts = test_time - DAY
    results = search_location(now_ts, uid, time_type)
    
    return json.dumps(results)


#use to get ip information for day and week
#write in version-15-12-08
#input: now_ts, uid
#output:{'day_ip':{}, 'week_ip':{}, 'description':''}
@mod.route('/ip/')
def ajax_ip():
    uid = request.args.get('uid', '')
    now_ts = time.time()
    # test
    now_ts = test_time - DAY
    result = search_ip(now_ts, uid)
    if not result:
        result = {}
    return json.dumps(result)


#use to get user mention @ user
#write in version:15-12-08
#input: uid, top_count
#output: result
@mod.route('/mention/')
def ajax_mention():
    uid = request.args.get('uid', '')
    uid = str(uid)
    top_count = request.args.get('top_count', SOCIAL_DEFAULT_COUNT)
    top_count = int(top_count)
    now_ts = time.time()
    # test
    now_ts = test_time
    results = search_mention(now_ts, uid, top_count)

    return json.dumps(results)

#use to get now day activity trend ,week activity trend and conclusion
#write in version:15-12-08
#output: {'day_trend':[], 'week_trend':[], 'description':[]}
@mod.route('/activity/')
def ajax_activity_day():
    results = {}
    uid = str(request.args.get('uid', ''))
    now_ts = time.time()
    # test
    now_ts = test_time
    results = search_activity(now_ts, uid)
    if not results:
        results = {}
    return json.dumps(results)

#use to get weibo for activity trend in day or week
#write in version:15-12-08
#input: uid, time_type, start_ts
#output: weibo_list
@mod.route('/activity_weibo/')
def ajax_activity_weibo():
    results = {}
    uid = str(request.args.get('uid', ''))
    time_type = str(request.args.get('type', '')) # type = day or week
    start_ts = int(request.args.get('start_ts', ''))
    results = get_activity_weibo(uid, time_type, start_ts)
    if not results:
        results = []
    return json.dumps(results)

#abandon in version-15-12-08
'''
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
'''

#use to get user retweet from es:retweet_1 or be_retweet_2
#write in version:15-12-08
#input: uid, top_count
#output: in_portrait_list, in_portrait_result, out_portrait_list
@mod.route('/attention/')
def ajax_attention():
    uid = request.args.get('uid', '')
    top_count = request.args.get('top_count', SOCIAL_DEFAULT_COUNT)
    uid = str(uid)
    top_count = int(top_count)
    results = search_attention(uid, top_count)
    if not results:
        results = {}
    return json.dumps(results)

#use to get user be_retweet from es:be_retweet_1 or be_retweet_2
#write in version:15-12-08
#input: uid, top_count
#output: in_portrait_list, in_portrait_result, out_portrait_list
@mod.route('/follower/')
def ajax_follower():
    uid = request.args.get('uid', '')
    uid = str(uid)
    top_count = request.args.get('top_count', SOCIAL_DEFAULT_COUNT)
    top_count = int(top_count)
    results = search_follower(uid, top_count)
    if not results:
        results = {}
    return json.dumps(results)

#use to get user comment from es: comment_1 or comment_2
#write in version: 15-12-08
#input: uid, top_count
#output: in_portrait_list, in_portrait_result, out_portrait_list
@mod.route('/comment/')
def ajax_comment():
    uid = request.args.get('uid', '')
    uid = str(uid)
    top_count = request.args.get('top_count', SOCIAL_DEFAULT_COUNT)
    top_count = int(top_count)
    results = search_comment(uid, top_count)
    if not results:
        results = {}
    return json.dumps(results)


#use to get user be_comment from es: be_comment_1 or be_comment_2
#write in version: 15-12-08
#input: uid, top_count
#output: in_portrait_list. in_portrait_result, out_portrait_list
@mod.route('/be_comment/')
def ajax_be_comment():
    uid = request.args.get('uid', '')
    uid =str(uid)
    top_count = request.args.get('top_count', SOCIAL_DEFAULT_COUNT)
    top_count = int(top_count)
    results = search_be_comment(uid, top_count)
    if not results:
        results = {}
    return json.dumps(results)

#use to get user interaction from es:retweet_1+be_retweet_1, comment_1+be_comment_1
#write in version: 15-12-08
#input: uid, top_count
#output: retweet_inter_list, comment_inter_list
@mod.route('/bidirect_interaction/')
def ajax_interaction():
    uid = request.args.get('uid', '')
    uid = str(uid)
    top_count = request.args.get('top_count', SOCIAL_DEFAULT_COUNT)
    top_count = int(top_count)
    results = search_bidirect_interaction(uid, top_count)
    if not results:
        results = {}
    return json.dumps(results)


#use to get user sentiment trend
#write in version： 15-12-08
#input: uid, time_type
#output: sentiment_trend
@mod.route('/sentiment_trend/')
def ajax_sentiment_trend():
    uid = request.args.get('uid', '')
    uid = str(uid)
    time_type = request.args.get('time_type', SENTIMENT_TREND_DEFAULT_TYPE)
    now_ts = time.time()
    #test
    now_ts = test_time - DAY
    results = search_sentiment_trend(uid, time_type, now_ts)
    if not results:
        results = {}
    return json.dumps(results)


#use to get user weibo from sentiment trend
#write in version: 15-12-08
#input: uid, start_time, time_type, sentiment_type
#output: weibo_list
@mod.route('/sentiment_weibo/')
def ajax_sentiment_weibo():
    uid = request.args.get('uid', '')
    uid = str(uid)
    start_ts = request.args.get('start_ts', '')
    start_ts = int(start_ts)
    time_type = request.args.get('time_type', SENTIMENT_TREND_DEFAULT_TYPE)
    sentiment_type = request.args.get('sentiment', DEFAULT_SENTIMENT)
    results = search_sentiment_weibo(uid, start_ts, time_type, sentiment_type)
    if not results:
        results = ''
    return json.dumps(results)


#use to get user tendency and psy
#write in version: 15-12-08
#input: uid
#output: tendency, psy(first level and second level)
@mod.route('/tendency_psy/')
def ajax_tendency_psy():
    uid = request.args.get('uid', '')
    uid = str(uid)
    results = search_tendency_psy(uid)
    if not results:
        results = {}
    return json.dumps(results)


#abandon in version: 15-12-08
'''
# get user geo track
@mod.route('/geo_track/')
def ajax_geo_track():
    uid = request.args.get('uid', '')
    uid = str(uid)
    results = get_geo_track(uid)
    #geo track by ip-timestamp
    #results = get_geo_track_ip(uid)
    if results:
        return json.dumps(results)
    else:
        return None
'''


#get user online pattern by week
#write in version: 15-12-08
#input: uid
#output: [(pattern1:count1), (pattern2:count2),...]
@mod.route('/online_pattern/')
def ajax_online_pattern():
    uid = request.args.get('uid', '')
    uid = str(uid)
    now_ts = time.time()
    #test
    now_ts = test_time
    results = get_online_pattern(now_ts, uid)
    if not results:
        results = {}
    return json.dumps(results)


#get user evaluate_index: activeness trend
#write in version: 15-12-08
#input: uid
#output: {'time_line':[], 'activeness':[]}
@mod.route('/activeness_trend/')
def ajax_activeness_trend():
    uid = request.args.get('uid', '')
    uid = str(uid)
    results = get_activeness_trend(uid)
    if not results:
        results = {}
    return json.dumps(results)

#get user influence trend
#write in version: 15-12-08
#input: uid
#output: {'time_line':[], 'influence':[]}
@mod.route('/influence_trend/')
def ajax_influence_trend():
    uid = request.args.get('uid', '')
    uid = str(uid)
    results = get_influence_trend(uid)
    if not results:
        results = {}
    return json.dumps(results)

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


@mod.route('/user_influence_detail/')
def ajax_user_influence_detail():
    uid = request.args.get('uid', '')
    date = request.args.get('date', '')
    uid = str(uid)
    date = str(date).replace('/', '')

    results = get_user_influence(uid, date)

    return json.dumps(results)


# get top 3 weibo
# date: 2013-09-01 (must be)
@mod.route('/get_top_weibo/')
def ajax_get_top_weibo():
    uid = request.args.get('uid', '')
    date = request.args.get('date', '')
    style = request.args.get("style", 0)
    uid = str(uid)
    date = str(date).replace('/', '-')

    results = influenced_detail(uid, date, style)

    return json.dumps(results)

# date: 2013-09-01
# all influenced user by a weibo
@mod.route('/influenced_users/')
def ajax_influenced_users():
    uid = request.args.get('uid', '')
    date = request.args.get('date', '')
    mid = request.args.get('mid', '')
    style = request.args.get('style', '')
    number = request.args.get("number", 20)
    uid = str(uid)
    date = str(date).replace('/', '-')
    mid = str(mid)
    style = int(style)
    number = int(number)

    results = detail_weibo_influence(uid, mid, style, date, number)

    return json.dumps(results)


# style: 0: all retweeted users, 1: all comment users
@mod.route('/all_influenced_users/')
def ajax_all_influenced_users():
    uid = request.args.get('uid', '')
    date = request.args.get('date', '')
    style = request.args.get("style", 0)
    uid = str(uid)
    date = str(date).replace('/', '-')
    style = int(style)

    results = statistics_influence_people(uid, date, style)

    return json.dumps(results)



# date: 2013-09-01
@mod.route('/current_influence_comment/')
def ajax_current_influence_comment():
    uid = request.args.get('uid', '')
    date = request.args.get("date", '')
    uid = str(uid)
    date = str(date)

    results = comment_on_influence(uid, date)

    return json.dumps(results)



# date: 2013-09-01
@mod.route('/current_tag_vector/')
def ajax_current_tag_vector():
    uid = request.args.get('uid', '')
    date = request.args.get("date", '')
    uid = str(uid)
    date = str(date)

    results = tag_vector(uid, date)

    return json.dumps(results)


@mod.route('/history_activeness_influence/')
def ajax_history_activeness_influence():
    uid = request.args.get('uid', '')
    uid = str(uid)

    results = []
    results.append(conclusion_on_influence(uid))

    return json.dumps(results)

# 影响力总评价，大小，类型，领域和话题
@mod.route("/summary_influence/")
def ajax_summary_influence():
    uid = request.args.get('uid', '')
    date = request.args.get('date', '')

    result = influence_summary(uid, date)

    return json.dumps(result)
