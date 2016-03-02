# -*- coding: UTF-8 -*-
import sys
import time
import json
import math
from user_portrait.global_utils import es_user_portrait as es
from user_portrait.global_utils import es_user_portrait, portrait_index_name, portrait_index_type
from user_portrait.global_utils import R_CLUSTER_FLOW2 as r_cluster
from user_portrait.global_utils import es_user_profile, profile_index_name, profile_index_type
from user_portrait.global_utils import es_flow_text, flow_text_index_name_pre, flow_text_index_type
from user_portrait.time_utils import ts2datetime, datetime2ts
from user_portrait.parameter import DAY, WEEK, MAX_VALUE, SENTIMENT_FIRST, SENTIMENT_SECOND
from user_portrait.parameter import RUN_TYPE, RUN_TEST_TIME

#use to get evaluate max
def get_evaluate_max():
    max_result = {}
    evaluate_index = ['influence', 'activeness', 'importance']
    for evaluate in evaluate_index:
        query_body = {
            'query':{
                'match_all':{}
                },
            'size': 1,
            'sort':[{evaluate: {'order': 'desc'}}]
            }
        try:
            result = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type,\
                    body=query_body)['hits']['hits']
        except Exception, e:
            raise e
        max_evaluate = result[0]['_source'][evaluate]
        max_result[evaluate] = max_evaluate
    
    return max_result

#use to get user psycho_status attribute
#input: uid_list
#output: {'uid1':{'first':{}, 'second':{}}, 'uid2':{},...}
def get_psycho_status(uid_list):
    results = {}
    uid_sentiment_dict = {}
    #time for es_flow_text
    now_ts = time.time()
    now_date_ts = datetime2ts(ts2datetime(now_ts))
    #test
    now_date_ts = datetime2ts('2013-09-08')
    start_date_ts = now_date_ts - DAY * WEEK
    for i in range(0, WEEK):
        iter_date_ts = start_date_ts + DAY * i
        flow_text_index_date = ts2datetime(iter_date_ts)
        flow_text_index_name = flow_text_index_name_pre + flow_text_index_date
        try:
            flow_text_exist = es_flow_text.search(index=flow_text_index_name, doc_type=flow_text_index_type,\
                    body={'query':{'filtered':{'filter':{'terms':{'uid': uid_list}}}}, 'size': MAX_VALUE}, _source=False,  fields=['uid', 'sentiment'])['hits']['hits']
        except:
            flow_text_exist = []
        for flow_text_item in flow_text_exist:
            uid = flow_text_item['fields']['uid'][0]
            sentiment = flow_text_item['fields']['sentiment'][0]
            if uid in uid_sentiment_dict:
                try:
                    uid_sentiment_dict[uid][str(sentiment)] += 1
                except:
                    uid_sentiment_dict[uid][str(sentiment)] = 1
            else:
                uid_sentiment_dict[uid] = {str(sentiment): 1}
    #compute first and second psycho_status
    for uid in uid_list:
        results[uid] = {'first':{}, 'second':{}}
        try:
            user_sentiment_result = uid_sentiment_dict[uid]
        except:
            user_sentiment_result = {}
        all_count = sum(user_sentiment_result.values())
        #compute second level sentiment---negative type sentiment
        second_sentiment_count_list = [user_sentiment_result[item] for item in user_sentiment_result if item in SENTIMENT_SECOND]
        second_sentiment_all_count = sum(second_sentiment_count_list)
        for sentiment_item in SENTIMENT_SECOND:
            try:
                results[uid]['second'][sentiment_item] = float(user_sentiment_result[sentiment_item]) / all_count
            except:
                results[uid]['second'][sentiment_item] = 0
        #compute first level sentiment---middle, postive, negative
        user_sentiment_result['7'] = second_sentiment_all_count
        for sentiment_item in SENTIMENT_FIRST:
            try:
                sentiment_ratio = float(user_sentiment_result[sentiment_item]) / all_count
            except:
                sentiment_ratio = 0
            results[uid]['first'][sentiment_item] = sentiment_ratio

    return results


#use to get user_list compare attr
#input: uid_list
#output: results
def compare_user_portrait_new(uid_list):
    try:
        user_portrait_result = es.mget(index=portrait_index_name, doc_type=portrait_index_type,\
                body={'ids':uid_list})['docs']
    except:
        user_portrait_result = []
    if user_portrait_result == []:
        return 'uid_list not exist'
    #get max evaluate:
    max_result = get_evaluate_max()
    user_result = {}
    #get user psycho status from flow_text
    user_psycho_status_result = get_psycho_status(uid_list)
    #iter to get user attr
    for item in user_portrait_result:
        if item['found'] != True:
            return 'uid_list not exist'
        uid = item['_id']
        user_result[uid] = {}
        source = item['_source']
        #attr: uname
        user_result[uid]['uname'] = source['uname']
        #attr: location
        user_result[uid]['location'] = source['location']
        #attr: evaluate index
        importance = source['importance']
        normal_importance = math.log(importance/ max_result['importance'] * 9 + 1, 10)
        user_result[uid]['importance'] = int(normal_importance * 100)
        influence = source['influence']
        normal_influence = math.log(influence / max_result['influence'] * 9 + 1, 10)
        user_result[uid]['influence'] = int(normal_influence * 100)
        activeness = source['activeness']
        normal_activeness = math.log(activeness / max_result['activeness'] * 9 + 1, 10)
        user_result[uid]['activeness'] = int(normal_activeness * 100)
        #attr: domain
        user_result[uid]['domain'] = source['domain']
        #attr: topic
        topic_string = source['topic_string']
        user_result[uid]['topic'] = topic_string.split('&')
        #attr: activity geo dict
        activity_geo_dict_list = json.loads(source['activity_geo_dict'])
        week_activity_geo_list = activity_geo_dict_list[-7:]
        week_geo_result = {}
        for day_geo_dict in week_activity_geo_list:
            for geo_item in day_geo_dict:
                try:
                    week_geo_result[geo_item] += 1
                except:
                    week_geo_result[geo_item] = 1
        sort_week_geo_result = sorted(week_geo_result.items(), key=lambda x:x[1], reverse=True)
        user_result[uid]['activity_geo'] = [geo_item[0] for geo_item in sort_week_geo_result[:2]]
        #attr: keywords
        user_result[uid]['keywords'] = json.loads(source['keywords'])
        #attr: hashtag
        user_result[uid]['hashtag'] = json.loads(source['hashtag_dict'])
        #attr: psycho status
        user_result[uid]['psycho_status'] = user_psycho_status_result[uid]
    
    return user_result


# compare two or three user
# need json.lodas to read the dict attribute
def compare_user_portrait(uid_list):
    user_portrait_result = {}
    index_name = 'user_portrait'
    index_type = 'user'
    user_result = es.mget(index=index_name, doc_type=index_type, body={'ids':uid_list})['docs']
    #user_portrait_result = [item['_source'] for item in user_result]
    #print 'user_result:', user_portrait_result
    for item in user_result:
        uid = item['_id']
        user_portrait_result[uid] = {}
        try:
            source = item['_source']
        except:
            next
        try:
            psycho_status = json.loads(source['psycho_status'])
        except:
            pasycho_status = {}
        try:
            psycho_feature = json.loads(source['psycho_feature'])
        except:
            psycho_feature = {}
        try:
            activity_geo_dict = json.loads(source['activity_geo_dict'])
            sort_activity_geo = sorted(activity_geo_dict.items(), key=lambda x:x[1], reverse=True)
            activity_geo_list = sort_activity_geo[:2]
            activity_list = []
            for item in activity_geo_list:
                city_list = item[0].split('\t')
                city = city_list[len(city_list)-1]
                activity_list.append(city)
        except:
            activity_geo = []
        try:
            hashtag_dict = json.loads(source['hashtag_dict'])
        except:
            hashtag_dict = {}
        user_portrait_result[uid] = {
                'uname': source['uname'],
                'gender': source['gender'],
                'location': source['location'],
                'importance': source['importance'],
                'activeness': source['activeness'],
                'influence': source['influence'],
                'fansnum':source['fansnum'],
                'statusnum':source['statusnum'],
                'friendsnum': source['friendsnum'],
                'domain': source['domain'],
                'topic': json.loads(source['topic']),
                'keywords': json.loads(source['keywords']),
                'psycho_status': psycho_status,
                'psycho_feature': psycho_feature,
                'activity_geo': activity_list,
                'hashtag_dict': hashtag_dict
                }

    #print 'user_portrait_result:', user_portrait_result
    return user_portrait_result

# compare user activity and activity time segment
def compare_user_activity(uid_list):
    result = {} # output data: {user:[weibo_status]}, {user:[(date,weibo)]}, ts_list
    timesegment_result = {}
    now_ts = time.time()
    date = ts2datetime(now_ts)
    #run_type
    if RUN_TYPE == 1:
        ts = datetime2ts(date)
    else:
        ts = datetime2ts(RUN_TEST_TIME)
    for i in range(1,8):
        ts = ts - DAY
        hash_name = 'activity_' + str(ts)
        r_result = r_cluster.hmget(hash_name, uid_list)
        if r_result:
            count = 0
            for r_item in r_result:
                if r_item:
                    r_item = json.loads(r_item)
                if uid_list[count] not in result:
                    result[uid_list[count]] = {}
                if uid_list[count] not in timesegment_result:
                    timesegment_result[uid_list[count]] = {}
                count += 1
                if r_item:
                    time_result = dict()
                    for segment in r_item:
                        try:
                            result[uid_list[count-1]][int(segment)/16*15*60*16+ts] += r_item[segment]
                        except:
                            result[uid_list[count-1]][int(segment)/16*15*60*16+ts] = r_item[segment]
                        try:
                            timesegment_result[uid_list[count-1]][int(segment)/16*15*60*16] += r_item[segment]
                        except:
                            timesegment_result[uid_list[count-1]][int(segment)/16*15*60*16] = r_item[segment]

    user_list = {}
    user_timesegment_list = {}
    ts_list = []
    for user in result:
        timesegment_dict = timesegment_result[user]
        sort_segment = sorted(timesegment_dict.items(), key=lambda x:x[1], reverse=True)
        segment_top = sort_segment[:3]
        user_timesegment_list[user] = segment_top
        user_dict = result[user]
        for i in range(0, 42):
            timestamp = ts + 15*60*16*i
            if len(ts_list)<42:
                ts_list.append(timestamp)
            try:
                count = user_dict[timestamp]
            except:
                count = 0
            try:
                user_list[user].append(count)
            except:
                user_list[user] = [count]
    return user_list, user_timesegment_list, ts_list

# compare the user profile
def compare_user_profile(uid_list):
    results = {}

    search_results = es_user_profile.mget(index=profile_index_name, doc_type=profile_index_type,\
            body={'ids':uid_list})['docs']
    for result in search_results:
        uid = result['_id']
        results[uid] = []
        try:
            item = result['_source']
        except:
            item = {}
        try:
            photo_url = item['photo_url']
        except:
            photo_url = 'unkown'

        results[uid] = photo_url
    return results

if __name__=='__main__':
    #test
    uid_list = ['1642591402', '2948738352', '2803301701']
    compare_user_portrait(uid_list)
    compare_user_activity(uid_list)
    compare_user_profile(uid_list)
