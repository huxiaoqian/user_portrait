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
from description import active_geo_description, active_time_description, hashtag_description
sys.path.append('../../')

from user_portrait.time_utils import ts2datetime, datetime2ts
from user_portrait.global_utils import R_CLUSTER_FLOW2 as r_cluster
from user_portrait.global_utils import R_DICT
from user_portrait.global_utils import es_user_portrait
from user_portrait.search_user_profile import search_uid2uname


emotion_mark_dict = {'126': 'positive', '127':'negative', '128':'anxiety', '129':'angry'}



#search:'retweet_'+uid return attention {r_uid1:count1, r_uid2:count2...}
#redis:{'retweet_'+uid:{ruid:count}}
#return results: {ruid:[uname,count]}
def search_attention(uid):
    stat_results = dict()
    results = dict()
    for db_num in R_DICT:
        r = R_DICT[db_num]
        ruid_results = r.hgetall('retweet_'+str(uid))
        if ruid_results:
            for ruid in ruid_results:
                try:
                    stat_results[ruid] += ruid_results[ruid]
                except:
                    stat_results[ruid] = ruid_results[ruid]
    # print 'results:', stat_results
    for ruid in stat_results:
        # search uid
        '''
        uname = search_uid2uname(ruid)
        if not uname:
        '''
        uname = '未知'
        
        count = stat_results[ruid]
        results[ruid] = [uname, count]
    if results:    
        return results
    else:
        return None

#search:'be_retweet_' + str(uid) return followers {br_uid1:count1, br_uid2:count2}
#redis:{'be_retweet_'+uid:{br_uid:count}}
#return results:{br_uid:[uname, count]}
def search_follower(uid):
    results = dict()
    stat_results = dict()
    for db_num in R_DICT:
        r = R_DICT[db_num]
        br_uid_results = r.hgetall('be_retweet_'+str(uid))
        #print 'br_uid_results:', br_uid_results
        if br_uid_results:
            for br_uid in br_uid_results:
                try:
                    stat_results[br_uid] += br_uid_results[br_uid]
                except:
                    stat_results[br_uid] = br_uid_results[br_uid]
    # print 'stat_results:', stat_results
    for br_uid in stat_results:
        # search uid
        '''
        uname = search_uid2uname(br_uid)
        if not uname:
        '''
        uname = '未知'
        
        count = stat_results[br_uid]
        results[br_uid] = [uname, count]
    if results:
        return results
    else:
        return None

#search:now_ts , uid return 7day at uid list  {uid1:count1, uid2:count2}
#{'at_'+Date:{str(uid):'{at_uid:count}'}}
#return results:{at_uid:[uname,count]}
def search_mention(now_ts, uid):
    date = ts2datetime(now_ts)
    ts = datetime2ts(date)
    #print 'at date-ts:', ts
    stat_results = dict()
    results = dict()
    for i in range(1,8):
        ts = ts - 24 * 3600
        try:
            result_string = r_cluster.hget('at_' + str(ts), str(uid))
        except:
            result_string = ''
        if not result_string:
            continue
        result_dict = json.loads(result_string)
        for at_uid in result_dict:
            try:
                stat_results[at_uid] += result_dict[at_uid]
            except:
                stat_results[at_uid] = result_dict[at_uid]
    
    for at_uid in stat_results:
        # search uid
        '''
        uname = search_uid2uname(at_uid)
        if not uname:
        '''    
        uname = '未知'
        count = stat_results[at_uid]
        results[at_uid] = [uname, count]
    if results:
        return results
    else:
        return False

#search:now_ts, uid return 7day loaction list {location1:count1, location2:count2}
#{'ip_'+str(Date_ts):{str(uid):'{city:count}'}
# return results: {city:{ip1:count1,ip2:count2}}
def search_location(now_ts, uid):
    date = ts2datetime(now_ts)
    #print 'date:', date
    ts = datetime2ts(date)
    #print 'date-ts:', ts
    stat_results = dict()
    results = dict()
    for i in range(1, 8):
        ts = ts - 24 * 3600
        #print 'for-ts:', ts
        result_string = r_cluster.hget('ip_' + str(ts), str(uid))
        if not result_string:
            continue
        result_dict = json.loads(result_string)
        for ip in result_dict:
            try:
                stat_results[ip] += result_dict[ip]
            except:
                stat_results[ip] = result_dict[ip]
    for ip in stat_results:
        city = ip2city(ip)
        if city:
            try:
                results[city][ip] = stat_results[ip]
            except:
                results[city] = {ip: stat_results[ip]}
                

    description = active_geo_description(results)
    results['description'] = description
    print 'location results:', results
    return results

#search: now_ts, uid return 7day activity trend list {time_segment:weibo_count}
# redis:{'activity_'+Date:{str(uid): '{time_segment: weibo_count}'}}
# return :{time_segment:count}
def search_activity(now_ts, uid):
    date = ts2datetime(now_ts)
    #print 'date:', date
    ts = datetime2ts(date)
    timestamp = ts
    #print 'date-ts:', ts
    activity_result = dict()
    results = dict()
    segment_result = dict()
    for i in range(1, 8):
        ts = timestamp - 24 * 3600*i
        #print 'for-ts:', ts
        try:
            result_string = r_cluster.hget('activity_' + str(ts), str(uid))
        except:
            result_string = ''
        #print 'activity:', result_string
        if not result_string:
            continue
        result_dict = json.loads(result_string)
        for time_segment in result_dict:
            try:
                results[int(time_segment)/16*15*60*16+ts] += result_dict[time_segment]
            except:
                
                results[int(time_segment)/16*15*60*16+ts] = result_dict[time_segment]
            try:
                segment_result[int(time_segment)/16*15*60*16] += result_dict[time_segment]
            except:
                segment_result[int(time_segment)/16*15*60*16] = result_dict[time_segment]


    trend_list = []
    for i in range(1,8):
        ts = timestamp - i*26*3600
        for j in range(0, 6):
            time_seg = ts + j*15*60*16
            if time_seg in results:
                trend_list.append((time_seg, results[time_seg]))
            else:
                trend_list.append((time_seg, 0))
    sort_trend_list = sorted(trend_list, key=lambda x:x[0], reverse=False)
    #print 'sort_trend_list:', sort_trend_list
    activity_result['activity_trend'] = sort_trend_list
    activity_result['activity_time'] = segment_result
    print segment_result
    description = active_time_description(segment_result)
    activity_result['description'] = description
    return activity_result

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

#use to search user_portrait to show the attribute saved in es_user_portrait
def search_attribute_portrait(uid):
    results = dict()
    index_name = 'user_portrait'
    index_type = 'user'
    try:
        results = es_user_portrait.get(index=index_name, doc_type=index_type, id=uid)['_source']
    except:
        results = None
    keyword_list = []
    if results and results['keywords']:
        keywords_dict = json.loads(results['keywords'])
        sort_word_list = sorted(keywords_dict.items(), key=lambda x:x[1], reverse=True)
        print 'sort_word_list:', sort_word_list
        results['keywords'] = sort_word_list[:20]
    #print 'keywords:', results
    geo_top = []
    if results and results['activity_geo_dict']:
        geo_dict = json.loads(results['activity_geo_dict'])
        sort_geo_dict = sorted(geo_dict.items(), key=lambda x:x[1], reverse=True)
        geo_top = sort_geo_dict[:5]
        results['activity_geo'] = geo_top
    if results and results['hashtag_dict']:
        hashtag_dict = json.loads(results['hashtag_dict'])
        sort_hashtag_dict = sorted(hashtag_dict.items(), key=lambda x:x[1], reverse=True)
        results['hashtag_dict'] = sort_hashtag_dict[:5]
    emotion_result = {}
    if results and results['emotion_words']:
        emotion_words_dict = json.loads(results['emotion_words'])
        for word_type in emotion_mark_dict:
            try:
                word_dict = emotion_words_dict[word_type]
                sort_word_dict = sorted(word_dict.items(), key=lambda x:x[1], reverse=True)
                print 'sort_word_dict:', sort_word_dict
                word_list = sort_word_dict[:5]
            except:
                word_list = []
            emotion_result[emotion_mark_dict[word_type]] = word_list
    print 'emotion_words:', type(emotion_result)
    results['emotion_words'] = emotion_result
    #topic
    if results and results['topic']:
        topic_dict = json.loads(results['topic'])
        sort_topic_dict = sorted(topic_dict.items(), key=lambda x:x[1], reverse=True)
        results['topic'] = sort_topic_dict[:5]
    #domain
    if results and results['domain']:
        domain_string = results['domain']
        domain_list = domain_string.split('_')
        results['domain'] = domain_list
    #emoticon
    if results and results['emoticon']:
        emoticon_dict = json.loads(results['emoticon'])
        sort_emoticon_dict = sorted(emoticon_dict.items(), key=lambda x:x[1], reverse=True)
        results['emoticon'] = sort_emoticon_dict[:5]
    #online_pattern
    if results and results['online_pattern']:
        online_pattern_dict = json.loads(results['online_pattern'])
        sort_online_pattern_dict = sorted(online_pattern_dict.items(), key=lambda x:x[1], reverse=True)
        results['online_pattern'] = sort_online_pattern_dict[:5]
    #psycho_status
    if results and results['psycho_status']:
        psycho_status_dict = json.loads(results['psycho_status'])
        sort_psycho_status_dict = sorted(psycho_status_dict.items(), key=lambda x:x[1], reverse=True)
        results['psycho_status'] = sort_psycho_status_dict[:5]
    #psycho_feature
    if results and results['psycho_feature']:
        psycho_feature_list = results['psycho_feature'].split('_')
        results['psycho_feature'] = psycho_feature_list
    return results

#use to search user_portrait by lots of condition 
def search_portrait(condition_num, query, sort, size):
    user_result = []
    index_name = 'user_portrait'
    index_type = 'user'
    if condition_num > 0:
        try:
            #print query
            result = es_user_portrait.search(index=index_name, doc_type=index_type, \
                    body={'query':{'bool':{'must':query}}, 'sort':sort, 'size':size})['hits']['hits']
            #print 'result:', result
        except Exception,e:
            raise e
    else:
        try:
            result = es_user_portrait.search(index=index_name, doc_type=index_type, \
                    body={'query':{'match_all':{}},'size':size})['hits']['hits']
        except Exception, e:
            raise e
    if result:
        #print 'result:', result
        for item in result:
            user_dict = item['_source']
            user_result.append([user_dict['uid'], user_dict['uname'], user_dict['gender'], user_dict['activeness'], user_dict['importance'], user_dict['influence']])

    return user_result

def delete_action(uid_list):
    index_name = 'user_portrait'
    index_type = 'user'
    for uid in uid_list:
        action = {'delete':{'_id': uid}}
        bulk_action.append(action)
    es.bulk(bulk_action, index=index_name, doc_type=index_type)
    time.sleep(1)
    return True


if __name__=='__main__':
    uid = '1798289842'
    now_ts = 1377964800 + 3600 * 24 * 4
    search_attribute_portrait(uid)
    '''
    results1 = search_attention(uid)
    print 'attention:', results1
    results2 = search_follower(uid)
    print 'follow:', results2
    results3 = search_mention(now_ts, uid)
    print 'at_user:', results3 
    results4 = search_location(now_ts, uid)
    print 'location:', results4
    results5 = search_activity(now_ts, uid)
    print 'activity:', results5
    '''
    
