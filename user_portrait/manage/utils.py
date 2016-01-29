# -*- coding: UTF-8 -*-
import sys
import time
import json
import math
#test
'''
reload(sys)
sys.path.append('../')
from global_utils import es_user_portrait as es
from global_utils import R_CLUSTER_FLOW2 as r_cluster
from global_utils import es_user_profile
from time_utils import ts2datetime, datetime2ts,ts2date
'''
from user_portrait.global_utils import es_user_portrait as es
from user_portrait.global_utils import es_user_portrait, portrait_index_name, portrait_index_type
from user_portrait.global_utils import R_CLUSTER_FLOW2 as r_cluster
from user_portrait.global_utils import es_user_profile, profile_index_name, profile_index_type
from user_portrait.time_utils import ts2datetime, datetime2ts
from user_portrait.parameter import DAY

#test
portrait_index_name = 'user_portrait_1222'
portrait_index_type = 'user'

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
        user_result[uid]['psycho_status'] = json.loads(source['psycho_status'])
    
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
    ts = datetime2ts(date)
    # test
    ts = datetime2ts('2013-09-08')
    for i in range(1,8):
        ts = ts - DAY
        hash_name = 'activity_' + str(ts)
        r_result = r_cluster.hmget(hash_name, uid_list)
        if r_result:
            #r_result = json.loads(r_result)
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
    #print 'user_list, user_timesegment_list, ts_list:', user_list, user_timesegment_list, ts_list
    return user_list, user_timesegment_list, ts_list

# compare the user profile
def compare_user_profile(uid_list):
    results = {}

    search_results = es_user_profile.mget(index=profile_index_name, doc_type=profile_index_type,\
            body={'ids':uid_list})['docs']
    #print 'results:', search_results
    for result in search_results:
        uid = result['_id']
        results[uid] = []
        try:
            item = result['_source']
        except:
            next
        photo_url = item['photo_url']
        results[uid] = photo_url
    #print 'results:', results
    return results

if __name__=='__main__':
    #test
    uid_list = ['1642591402', '2948738352', '2803301701']
    compare_user_portrait(uid_list)
    compare_user_activity(uid_list)
    compare_user_profile(uid_list)
