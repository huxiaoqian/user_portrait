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
from user_portrait.global_utils import es_user_profile
from user_portrait.search_user_profile import search_uid2uname
from user_portrait.filter_uid import all_delete_uid


emotion_mark_dict = {'126': 'positive', '127':'negative', '128':'anxiety', '129':'angry'}
link_ratio_threshold = [0, 0.5, 1]


def search_identify_uid(uid):
    result = 0
    try:
        user_dict = es_user_portrait.get(index='user_portrait', doc_type='user', id=uid)
        #print 'user_dict:', user_dict
        result = 1
    except:
        result = 0
    return result

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
                if ruid != uid:
                    try:
                        stat_results[ruid] += ruid_results[ruid]
                    except:
                        stat_results[ruid] = ruid_results[ruid]
    # print 'results:', stat_results
    if not results:
        return [None, 0]
    try:
        sort_state_results = sorted(stat_results.items(), key=lambda x:x[1], reverse=True)[:20]
    except:
        return [None, 0]
    print 'sort_state_results:', sort_state_results
    uid_list = [item[0] for item in sort_state_results]
    es_profile_results = es_user_profile.mget(index='weibo_user', doc_type='user', body={'ids':uid_list})['docs']
    es_portrait_results = es_user_portrait.mget(index='user_portrait', doc_type='user', body={'ids':uid_list})['docs']
    result_list = []
    for i in range(len(es_profile_results)):
        item = es_profile_results[i]
        uid = item['_id']
        try:
            source = item['_source']
            uname = source['nick_name']
        except:
            uname = u'未知'
        # identify uid is in the user_portrait
        portrait_item = es_portrait_results[i]
        try:
            source = portrait_item[i]
            in_status = 1
        except:
            in_status = 0

        result_list.append([uid,[uname, stat_results[uid], in_status]])
       
    return [result_list[:20], len(stat_results)]


#search:'be_retweet_' + str(uid) return followers {br_uid1:count1, br_uid2:count2}
#redis:{'be_retweet_'+uid:{br_uid:count}}
#return results:{br_uid:[uname, count]}
def search_follower(uid):
    results = dict()
    stat_results = dict()
    for db_num in R_DICT:
        r = R_DICT[db_num]
        br_uid_results = r.hgetall('be_retweet_'+str(uid))
        if br_uid_results:
            for br_uid in br_uid_results:
                if br_uid != uid:
                    try:
                        stat_results[br_uid] += br_uid_results[br_uid]
                    except:
                        stat_results[br_uid] = br_uid_results[br_uid]
    if not stat_results:
        return [None, 0]
    try:
        sort_stat_results = sorted(stat_results.items(), key=lambda x:x[1], reverse=True)[:20]
    except:
        return [None, 0]

    uid_list = [item[0] for item in sort_stat_results]
    es_profile_results = es_user_profile.mget(index='weibo_user', doc_type='user', body={'ids':uid_list})['docs']
    es_portrait_results = es_user_portrait.mget(index='user_portrait', doc_type='user', body={'ids':uid_list})['docs']
    result_list = []
    for i in range(len(es_profile_results)):
        item = es_profile_results[i]
        uid = item['_id']
        try:
            source = item['_source']
            uname = source['nick_name']
        except:
            uname = u'未知'

        portrait_item = es_portrait_results[i]
        try:
            source = portrait_item['_source']
            in_status = 1
        except:
            in_status = 0
        result_list.append([uid,[uname, stat_results[uid], in_status]])
    return [result_list[:20], len(stat_results)]

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
        uid = ''
        count = stat_results[at_uid]
        results[at_uid] = [uid, count]
    if results:
        sort_results = sorted(results.items(), key=lambda x:x[1][1], reverse=True)
        return [sort_results[:20], len(results)]
    else:
        return [None, 0]

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
    #print 'location results:', results
    return results

#search: now_ts, uid return 7day activity trend list {time_segment:weibo_count}
# redis:{'activity_'+Date:{str(uid): '{time_segment: weibo_count}'}}
# return :{time_segment:count}
def search_activity(now_ts, uid):
    date = ts2datetime(now_ts)
    print 'date:', date
    ts = datetime2ts(date)
    timestamp = ts
    print 'date-timestamp:', ts
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
        ts = timestamp - i*24*3600
        for j in range(0, 6):
            time_seg = ts + j*15*60*16
            if time_seg in results:
                trend_list.append((time_seg, results[time_seg]))
            else:
                trend_list.append((time_seg, 0))
    sort_trend_list = sorted(trend_list, key=lambda x:x[0], reverse=False)
    #print 'sort_trend_list:', sort_trend_list
    activity_result['activity_trend'] = sort_trend_list
    sort_segment_list = sorted(segment_result.items(), key=lambda x:x[1], reverse=True)
    activity_result['activity_time'] = sort_segment_list[:2]
    #print segment_result
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
        city_list = city.split('\t')
        if len(city_list)==4:
            city = '\t'.join(city_list[:3])
    except Exception,e:
        return None
    return city

# show user geo track
def get_geo_track(uid):
    date_results = [] # {'2013-09-01':[(geo1, count1),(geo2, count2)], '2013-09-02'...}
    now_ts = time.time()
    now_date = ts2datetime(now_ts)
    #test
    now_date = '2013-09-08'
    ts = datetime2ts(now_date)
    city_list = []
    city_set = set()
    for i in range(7, 0, -1):
        timestamp = ts - i*24*3600
        #print 'timestamp:', ts2datetime(timestamp)
        ip_dict = dict()
        results = r_cluster.hget('ip_'+str(timestamp), uid)
        ip_dict = dict()
        date = ts2datetime(timestamp)
        date_key = '-'.join(date.split('-')[1:])
        if results:
            ip_dict = json.loads(results)
            geo_dict = ip_dict2geo(ip_dict)
            city_list.extend(geo_dict.keys())
            sort_geo_dict = sorted(geo_dict.items(), key=lambda x:x[1], reverse=True)
            date_results.append([date_key, sort_geo_dict[:2]])
        else:
            date_results = [date_key, []]

    print 'results:', date_results
    city_set = set(city_list)
    geo_conclusion = get_geo_conclusion(uid, city_set)
    return [date_results, geo_conclusion]

def get_geo_conclusion(uid, city_set):
    conclusion = ''
    mark = 0
    user_portrait_result = es_user_portrait.get(index='user_portrait', doc_type='user', id=uid)
    try:
        source = user_portrait_result['_source']
        location = source['location']
        location_city_list = location.split('\t')
        #print 'location_city:', location_city_list
        for location_city in location_city_list:
            if location_city in city_set:
                mark += 1
        if mark==0:
            conclusion = u'该用户注册地与活跃地区不一致'
        else:
            conclusion = u'该用户注册地包括在活跃地区范围内'
    except:
        conclusion = ''
    #print 'conclusion:', conclusion
    return conclusion

def ip_dict2geo(ip_dict):
    city_set = set()
    geo_dict = dict()
    for ip in ip_dict:
        try:
            city = IP.find(str(ip))
            if city:
                city.encode('utf-8')
            else:
                city = ''
        except Exception, e:
            city = ''
        if city:
            len_city = len(city.split('\t'))
            if len_city==4:
                city = '\t'.join(city.split('\t')[:3])
            new_len_city = len(city.split('\t'))
            city = city.split('\t')[new_len_city-1]
            try:
                geo_dict[city] += ip_dict[ip]
            except:
                geo_dict[city] = ip_dict[ip]
    return geo_dict


#use to search user_portrait to show the attribute saved in es_user_portrait
def search_attribute_portrait(uid):
    results = dict()
    index_name = 'user_portrait'
    index_type = 'user'
    try:
        results = es_user_portrait.get(index=index_name, doc_type=index_type, id=uid)['_source']
    except:
        results = None
        return None
    keyword_list = []
    if results['keywords']:
        keywords_dict = json.loads(results['keywords'])
        sort_word_list = sorted(keywords_dict.items(), key=lambda x:x[1], reverse=True)
        #print 'sort_word_list:', sort_word_list
        results['keywords'] = sort_word_list
    else:
        results['keywords'] = []
    #print 'keywords:', results
    geo_top = []
    if results['activity_geo_dict']:
        geo_dict = json.loads(results['activity_geo_dict'])
        sort_geo_dict = sorted(geo_dict.items(), key=lambda x:x[1], reverse=True)
        geo_top = sort_geo_dict
        results['activity_geo'] = geo_top
    else:
        results['activity_geo'] = []
    if results['hashtag_dict']:
        hashtag_dict = json.loads(results['hashtag_dict'])
        sort_hashtag_dict = sorted(hashtag_dict.items(), key=lambda x:x[1], reverse=True)
        results['hashtag_dict'] = sort_hashtag_dict[:5]
        descriptions = hashtag_description(hashtag_dict)
        results['hashtag_description'] = descriptions
    else:
        results['hashtag_dict'] = []
        results['hashtag_description'] = ''
    emotion_result = {}
    emotion_conclusion_dict = {}
    if results['emotion_words']:
        emotion_words_dict = json.loads(results['emotion_words'])
        for word_type in emotion_mark_dict:
            try:
                word_dict = emotion_words_dict[word_type]
                if word_type=='126' or word_type=='127':
                    emotion_conclusion_dict[word_type] = word_dict
                sort_word_dict = sorted(word_dict.items(), key=lambda x:x[1], reverse=True)
                #print 'sort_word_dict:', sort_word_dict
                word_list = sort_word_dict[:5]
            except:
                word_list = []
            emotion_result[emotion_mark_dict[word_type]] = word_list
    #print 'emotion_words:', type(emotion_result)
    results['emotion_words'] = emotion_result
    #emotion_conclusion
    results['emotion_conclusion'] = get_emotion_conclusion(emotion_conclusion_dict)
    #topic
    if results['topic']:
        topic_dict = json.loads(results['topic'])
        sort_topic_dict = sorted(topic_dict.items(), key=lambda x:x[1], reverse=True)
        results['topic'] = sort_topic_dict[:5]
    else:
        results['topic'] = []
    #domain
    if results['domain']:
        domain_string = results['domain']
        domain_list = domain_string.split('_')
        results['domain'] = domain_list
    else:
        results['domain'] = []
    #emoticon
    if results['emoticon']:
        emoticon_dict = json.loads(results['emoticon'])
        sort_emoticon_dict = sorted(emoticon_dict.items(), key=lambda x:x[1], reverse=True)
        results['emoticon'] = sort_emoticon_dict[:5]
    else:
        results['emoticon'] = []
    #online_pattern
    if results['online_pattern']:
        online_pattern_dict = json.loads(results['online_pattern'])
        sort_online_pattern_dict = sorted(online_pattern_dict.items(), key=lambda x:x[1], reverse=True)
        results['online_pattern'] = sort_online_pattern_dict[:5]
    else:
        results['online_pattern'] = []
    #psycho_status
    if results['psycho_status']:
        psycho_status_dict = json.loads(results['psycho_status'])
        sort_psycho_status_dict = sorted(psycho_status_dict.items(), key=lambda x:x[1], reverse=True)
        results['psycho_status'] = sort_psycho_status_dict[:5]
    else:
        results['psycho_status'] = []
    #psycho_feature
    if results['psycho_feature']:
        psycho_feature_list = results['psycho_feature'].split('_')
        results['psycho_feature'] = psycho_feature_list
    else:
        results['psycho_feature'] = []
    #state
    if results['uid']:
        uid = results['uid']
        try:
            profile_result = es_user_profile.get(index='weibo_user', doc_type='user', id=uid)
        except:
            profile_result = None
        try:
            user_state = profile_result['_source']['description']
            results['description'] = user_state
        except:
            results['description'] = ''
    else:
        results['uid'] = ''
        results['description'] = ''
    
    if results['importance']:
        #print results['importance']
        query_body = {
                'query':{
                    "range":{
                        "importance":{
                        "from": results['importance'],
                        "to": 1000000
                        }
                        }
                    }
                }
        importance_rank = es_user_portrait.count(index=index_name, doc_type=index_type, body=query_body)
        if importance_rank['_shards']['successful'] != 0:
            #print 'importance_rank:', importance_rank
            results['importance_rank'] = importance_rank['count']
        else:
            print 'es_importance_rank error'
            results['importance_rank'] = 0
    else:
        results['importance_rank'] = 0
    if results['activeness']:
        query_body = {
                'query':{
                    "range":{
                        "activeness":{
                            "from":results['activeness'],
                            "to": 1000000
                            }
                        }
                    }
                }
        activeness_rank = es_user_portrait.count(index=index_name, doc_type=index_type, body=query_body)
        if activeness_rank['_shards']['successful'] != 0:
            results['activeness_rank'] = activeness_rank['count']
        else:
            print 'es_activess_rank error'
            results['activeness_rank'] = 0
    if results['influence']:
        query_body = {
                'query':{
                    'range':{
                        'influence':{
                            'from':results['influence'],
                            'to': 1000000
                            }
                        }
                    }
                }
        influence_rank = es_user_portrait.count(index=index_name, doc_type=index_type, body=query_body)
        if influence_rank['_shards']['successful'] != 0:
            results['influence_rank'] = influence_rank['count']
        else:
            print 'es_influence_rank error'
            results['influence_rank'] = 0
    #total count in user_portrait
    query_body ={
            'query':{
                'match_all':{}
                }
            }
    all_count_results = es_user_portrait.count(index=index_name, doc_type=index_type, body=query_body)
    if all_count_results['_shards']['successful'] != 0:
        results['all_count'] = all_count_results['count']
    else:
        print 'es_user_portrait error'
        results['all_count'] = 0
    #link conclusion
    link_ratio = results['link']
    results['link_conclusion'] = get_link_conclusion(link_ratio)
    return results

#get emotion conclusion
def get_emotion_conclusion(emotion_dict):
    positive_key = '126'
    negative_key = '127'
    emotion_conclusion = ''
    if positive_key in emotion_dict:
        positive_word_count = sum(emotion_dict[positive_key].values())
    else:
        positive_word_count = 0
    if negative_key in emotion_dict:
        negative_word_count = sum(emotion_dict[negative_key].values())
    else:
        negative_word_count = 0
    if positive_word_count > negative_word_count:
        emotion_conclusion = u'该用户发布微博中偏好使用正向情感词'
    elif positive_word_count < negative_word_count:
        emotion_conclusion = u'该用户发布微博中偏好使用负向情感词'
    else:
        emotion_conclusion = u'该用户发布微博中正向情感词和负向情感词使用均衡'
    return emotion_conclusion

#get link conclusion
def get_link_conclusion(link_ratio):
    conclusion = ''
    if link_ratio >= link_ratio_threshold[2]: 
        conclusion = u'该用户极易于将外部信息引入微博平台'
    elif link_ratio < link_ratio_threshold[2] and link_ratio >= link_ratio_threshold[1]:
        conclusion = u'该用户一般易于将外部信息引入微博平台'
    elif link_ratio < link_ratio_threshold[1]:
        conclusion = u'该用户不易于将外部信息引入微博平台'
    return conclusion


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
                    body={'query':{'match_all':{}}, 'sort':[{sort:{"order":"desc"}}], 'size':size})['hits']['hits']
        except Exception, e:
            raise e
    if result:
        #print 'result:', result
        filter_set = all_delete_uid() # filter_uids_set
        for item in result:
            user_dict = item['_source']
            score = item['_score']

            if not user_dict['uid'] in filter_set:
                user_result.append([user_dict['uid'], user_dict['uname'], user_dict['location'], user_dict['activeness'], user_dict['importance'], user_dict['influence'], score])

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
    
