# -*- coding: UTF-8 -*-
'''
search attribute : attention, follower, mention, location, activity
'''
import IP
import sys
import csv
import time
import json
import redis

from user_portrait.time_utils import ts2datetime, datetime2ts
from user_portrait.global_config import R_CLUSTER_FLOW2 as r_cluster
from user_portrait.global_config import R_DICT
from user_portrait.search_user_profile import search_uid2uname

#search:'retweet_'+uid return attention {r_uid1:count1, r_uid2:count2...}
def search_attention(uid):
    ruid_results = r.hgetall('retweet_'+str(uid))
    print 'ruid_results:', ruid_results
    # search uid
    '''
    uname = search_uid2uname(at_uid)
    if not uname:
    uname = '未知'
    '''
    if ruid_results:    
        return ruid_results
    else:
        return None

#search:'be_retweet_' + str(uid) return followers {br_uid1:count1, br_uid2:count2}
def search_follower(uid):
    br_uid_results = r.hgetall('be_retweet_'+str(uid))
    print 'br_uid_results:', br_uid_results
    # search uid
    '''
    uname = search_uid2uname(at_uid)
    if not uname:
    uname = '未知'
    '''
    if br_uid_results:
        return results
    else:
        return None

#search:now_ts , uid return 7day at uid list  {uid1:count1, uid2:count2}
#{Date:{str(uid):''}}
def search_mention(now_ts, uid):
    date = ts2datetime(now_ts)
    ts = datetime2ts(date)
    #print 'at date-ts:', ts
    results = dict()
    for i in range(1,8):
        ts = ts - 24 * 3600
        result_string = r_cluster.hget('at_' + str(ts), str(uid))
        if not result_string:
            continue
        result_dict = json.loads(result_string)
        for at_uid in result_dict:
            # search uid
            '''
            uname = search_uid2uname(at_uid)
            if not uname:
                uname = '未知'
            '''
            try:
                results[at_uid] += result_dict[at_uid]
            except:
                results[at_uid] = result_dict[at_uid]
    
    return results

#search:now_ts, uid return 7day loaction list {location1:count1, location2:count2}
#{'ip_'+str(Date_ts):{str(uid):'{city:count}'}
def search_location(now_ts, uid):
    date = ts2datetime(now_ts)
    #print 'date:', date
    ts = datetime2ts(date)
    #print 'date-ts:', ts
    results = dict()
    for i in range(1, 8):
        ts = ts - 24 * 3600
        #print 'for-ts:', ts
        result_string = r_cluster.hget('ip_' + str(ts), str(uid))
        if not result_string:
            continue
        result_dict = json.loads(result_string)
        for ip in result_dict:
            city = ip2city(ip)
            try:
                results['ip'][ip] += result_dict['ip'][ip]
                results['city'][city] += 1
            except:
                results['ip'][ip] = result_dict['ip'][ip]
                results['city'][city] = 1
    print 'location results:', results
    return results

#search: now_ts, uid return 7day activity trend list {time_segment:weibo_count}
# {Date:{str(uid): '{time_segment: weibo_count}'}}
def search_activity(now_ts, uid):
    date = ts2datetime(now_ts)
    #print 'date:', date
    ts = datetime2ts(date)
    #print 'date-ts:', ts
    results = dict()
    for i in range(1, 8):
        ts = ts - 24 * 3600
        #print 'for-ts:', ts
        result_string = r_cluster.hget('activity_' + str(ts), str(uid))
        #print 'activity:', result_string
        if not result_string:
            continue
        result_dict = json.loads(result_string)
        for time_segment in result_dict:
            try:
                results[time_segment] += result_dict[time_segment]
            except:
                results[time_segment] = result_dict[time_segment]
                
    return results

# ip to city
def ip2city(ip):
    try:
        city = IP.find(str(ip))
        if city:
            city = city.encode('utf-8')
        else:
            return None
    except Exception,e:
        return None
    return city

if __name__=='__main__':
    uid = '1798289842'
    now_ts = 1377964800 + 3600 * 24 * 4
    
    results1 = search_attention(uid)
    print 'attention:', results1
    results2 = search_follower(uid)
    print 'follow:', results2
    results3 = search_at(now_ts, uid)
    print 'at_user:', results3 
    results4 = search_location(now_ts, uid)
    print 'location:', results4
    results5 = search_activity(now_ts, uid)
    print 'activity:', results5

    
