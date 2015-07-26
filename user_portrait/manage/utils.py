# -*- coding: UTF-8 -*-
import sys
import time
import json
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
from user_portrait.global_utils import R_CLUSTER_FLOW2 as r_cluster
from user_portrait.global_utils import es_user_portrait
from user_portrait.time_utils import ts2datetime, datetime2ts

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
        user_portrait_result[uid] = {
                'uname': source['uname'],
                'gender': source['gender'],
                'location':source['location'],
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
                'psycho_feature': psycho_feature
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
        ts = ts - 24*3600
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
    index_name = 'weibo_user'
    index_type = 'user'
    search_results = es_user_profile.mget(index=index_name, doc_type=index_type, body={'ids':uid_list})['docs']
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
    #compare_user_portrait(uid_list)
    compare_user_activity(uid_list)
    #compare_user_profile(uid_list)
