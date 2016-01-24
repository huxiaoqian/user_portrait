# -*- coding: UTF-8 -*-
import IP
import sys
import json
import time
import math
import numpy as np
from save_utils import save_group_results
from config import activeness_weight_dict, importance_weight_dict,\
                   domain_weight_dict, topic_weight_dict, tightness_weight_dict
reload(sys)
sys.path.append('../../')
from global_utils import es_user_portrait as es
from global_utils import R_GROUP as r
from global_utils import group_analysis_queue_name
from global_utils import es_user_portrait, portrait_index_name, portrait_index_type ,\
                         es_group_result, group_index_name, group_index_type ,\
                         es_retweet, retweet_index_name_pre, retweet_index_type ,\
                         be_retweet_index_name, be_retweet_index_type ,\
                         es_comment, comment_index_name_pre, comment_index_type ,\
                         be_comment_index_name, be_comment_index_type ,\
                         es_flow_text, flow_text_index_name_pre, flow_text_index_type,\
                         es_copy_portrait, copy_portrait_index_name, copy_portrait_index_type

from global_utils import R_DICT as r_dict
from global_utils import R_CLUSTER_FLOW2 as r_cluster
from global_utils import ES_CLUSTER_FLOW1 as es_cluster
from global_config import R_BEGIN_TIME
from parameter import ACTIVITY_GEO_TOP, MAX_VALUE, DAY, HIS_BINS_COUNT, GROUP_ACTIVITY_TIME_THRESHOLD, \
        GROUP_ACTIVITY_TIME_DESCRIPTION_DICT
from time_utils import ts2datetime, datetime2ts


r_begin_ts = datetime2ts(R_BEGIN_TIME)


#use to merge dict list
#input: dict_list
#ouput: merge_dict
def union_dict_list(objs):
    _keys = set(sum([obj.keys() for obj in objs], []))
    _total = {}
    for _key in _keys:
        _total[_key] = sum([int(obj.get(_key, 0)) for obj in objs])

    return _total

# compute index rank like importance/activeness/influence rank
# input: index_value and index_type
# output: index_rank
def get_index_rank(index_value, index_name):
    result = 0
    query_body = {
            'query':{
                'range':{
                    index_name:{
                        'from':index_value,
                        'to': MAX_VALUE
                        }
                    }
                }
            }
    index_rank = es_user_portrait.count(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)
    if index_rank['_shards']['successful'] != 0:
       result = index_rank['count']
    else:
        print 'es index rank error'
        results = 0
    return result


#compute attr from es_user_portrait
#version: 16-01-22
#input: uid_list
#output: 
def get_attr_portrait(uid_list):
    result = {}
    #init some dict
    gender_ratio = dict()
    verified_ratio = dict()
    online_pattern_ratio = dict()
    domain_ratio = dict()
    topic_ratio = dict()
    keyword_ratio = dict()
    hashtag_ratio = dict()
    activity_geo_distribution_date = dict() # {'date1':{geo1:person_count, geo2:person_count}, 'date2':{geo1:person_count,..}, ..} # one month
    activity_geo_vary = dict() # {'geo2geo': count, ...}  geo2geo='activity_geo1&activity_geo2'
    importance_list = []
    influence_list = []
    activeness_list = []
    sentiment_dict_list = []
    #get now date to iter activity geo
    now_ts = int(time.time())
    now_date_ts = datetime2ts(ts2datetime(now_ts))
    #split uid_list to bulk action
    iter_count = 0
    all_user_count = len(uid_list)
    while iter_count < all_user_count:
        iter_uid_list = uid_list[iter_count: iter_count + DETECT_ITER_COUNT]
        try:
            iter_user_dict_list = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type, \
                body={'ids':iter_uid_list})['docs']
        except:
            iter_user_dict_list = []

        for user_dict in iter_user_dict_list:
            source = user_dict['_source']
            #attr1: gender ratio:
            gender = source['gender']
            try:
                gender_ratio[gender] += 1
            except:
                gender_ratio[gender] = 1
            #attr2: verified ratio
            verified = source['verified']
            try:
                verified_ratio[verified] += 1
            except:
                verified_ratio[verified] = 1
            #attr3: online pattern
            online_pattern = source['online_pattern']
            online_pattern = json.loads(online_pattern)
            for pattern in online_pattern:
                try:
                    online_pattern_ratio[pattern] += 1
                except:
                    online_pattern_ratio[pattern] = 1
            #attr4: domain
            domain = source['domain']
            try:
                domain_ratio[domain] += 1
            except:
                domain_ratio[domain] = 1
            #attr5: topic
            topic_string = source['topic_string']
            topic_list = topic_string.split('&')
            for topic in topic_list:
                try:
                    topic_ratio[topic] += 1
                except:
                    topic_ratio[topic] = 1
            #attr6: keywords_string
            keywords_string = source['keywords_string']
            keywords_list = keywords_string.split('&')
            for keyword in keywords_list:
                try:
                    keyword_ratio[keyword] += 1
                except:
                    keyword_ratio[keyword] = 1
            #attr7: hashtag
            hashtag_string = source['hashtag']
            hashtag_list = hashtag_string.split('&')
            for hashtag in hashtag_list:
                try:
                    hashtag_ratio[hashtag] += 1
                except:
                    hashtag_ratio[hashtag] = 1
            #attr8: activity_geo_dict---distribution by date
            user_activity_geo = {}
            activity_geo_dict_list = json.loads(source['activity_geo_dict'])
            activity_geo_date_count = len(activity_geo_dict_list)
            iter_ts = now_date_ts - activity_geo_date_count * DAY
            user_date_main_list = []
            for i in range(0, activity_geo_date_count):
                if iter_date in activity_geo_distribution_date:
                    activity_geo_distribution_date[iter_ts] = union_dict([activity_geo_distribution_date[iter_ts], date_item])
                else:
                    activity_geo_distribution_date[iter_ts] = date_item
                #use to get activity_geo vary
                sort_date_item = sorted(date_item.items(), key=lambda x:x[1], reverse=True)
                if date_item != {}:
                    main_date_city = sort_date_item[0][0]
                    try:
                        last_user_date_main_item = user_date_main_list[-1]
                    except:
                        lasr_user_date_main_item = ''
                    if main_date_city != main_date_city:
                        user_date_main_list.append(main_date_city)

                iter_ts += DAY
            #attr8: activity_geo_dict---location vary
            if len(user_date_main_list) > 1:
                for i in range(1, len(user_date_main_list)):
                    vary_item = '&'.join(user_date_main_list[i-1:i])
                    try:
                        activity_geo_vary[vary_item] += 1
                    except:
                        activity_geo_vary[vary_item] = 1
            
            #attr9: influence distribution
            influence = source['influence']
            influence_rank = get_index_rank(influence, 'influence')
            influence_list.append(influence_rank) 
            #attr10: importance distribution
            importance = source['importance']
            importance_rank = get_index_rank(importance, 'importance')
            importance_list.append(importance_rank)
            #attr11: activeness distribution
            activeness = source['activeness']
            activeness_rank = get_index_rank(activeness, 'activeness')
            activeness_list.append(activeness_rank)
            #attr12: tag
            for user_attribute_item in source:
                if user_attribute_item not in IDENTIFY_ATTRIBUTE_LIST:
                    tag_name = user_attribute_item
                    tag_value = source[user_attribute_item]
                    tag_key = tag_name + ':' + tag_value
                    try:
                        tag_dict[tag_key] += 1
                    except:
                        tag_dict[tag_key] = 1
            #attr13: psycho status
            #test
            user_sentiment = source['psycho_status']['first_dict']
            #user_sentiment = source['psycho_status']
            sentiment_dict_list.append(user_sentiment)

        iter_count += DETECT_ITER_COUNT
    #get all sentiment dict
    sentiment_dict = union_dict_list(sentiment_dict_list)
    # importance ditribution
    p, t = np.histogram(importance_list, bins=HIS_BINS_COUNT, normed=False)
    results['importance_his'] = [p.tolist(), t.tolist()]
    p, t = np.histogram(influence_list, bins=HIS_BINS_COUNT, normed=False)
    results['influence_his'] = [p.tolist(), t.tolist()]
    p, t = np.histogram(activeness_list, bins=HIS_BINS_COUNT ,normed=False)
    results['activeness_his'] = [p.tolist(), t.tolist()]
    # get result dict
    result['gender'] = json.dumps(gender_ratio)
    result['verified'] = json.dumps(verified_ratio)
    result['online_pattern'] = json.dumps(onlinr_pattern)
    result['domain'] = json.dumps(domain_ratio)
    result['topic'] = json.dumps(topic_rati)
    result['activity_geo_distribution'] = json.dumps(activity_geo_distribution_date)
    result['activity_geo_vary'] = json.dumps(activity_geo_vary)
    result['hashtag'] = json.dumps(hashtag_dict)
    result['keywords'] = json.dumps(keyword_ratio)
    
    return result



#abandon in version: 160122
'''
# compute attr from es_user_portrait
def get_attr_portrait(uid_list):
    result = {}
    index_name = 'user_portrait'
    index_type = 'user'
    user_dict_list = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type, body={'ids':uid_list})['docs']
    gender_ratio = dict()
    verified_ratio = dict()
    online_pattern_ratio = dict()
    domain_ratio = dict()
    topic_ratio = dict()
    emoticon_ratio = dict()
    keyword_ratio = dict()
    importance_list = []
    activeness_list = []
    influence_list = []
    psycho_status_ratio  = dict()
    psycho_feature_ratio = dict()
    hashtag_ratio = dict()
    activity_geo_ratio = dict()
    for user_dict in user_dict_list:
        user_dict = user_dict['_source']
        #attr1 gender ratio
        gender = user_dict['gender']
        if gender:
            try:
                gender_ratio[gender] += 1
            except:
                gender_ratio[gender] = 1
        #attr2 verified ratio
        verified = user_dict['verified']
        if verified:
            try:
                verified_ratio[verified] += 1
            except:
                verified_ratio[verified] = 1
        #attr3 online pattern
        online_pattern = user_dict['online_pattern']
        if online_pattern:
            online_pattern = json.loads(online_pattern)
            for pattern in online_pattern:
                try:
                    online_pattern_ratio[pattern] += 1
                except:
                    online_pattern_ratio[pattern] = 1
        #attr4 domain
        domain_string = user_dict['domain']
        if domain_string:
            domain_list = domain_string.split('_')
            for domain in domain_list:
                try:
                    domain_ratio[domain] += 1
                except:
                    domain_ratio[domain] = 1
        #attr5 topic
        topic_string = user_dict['topic']
        if topic_string:
            topic_dict = json.loads(topic_string)
            for topic in topic_dict:
                try:
                    topic_ratio[topic] += 1
                except:
                    topic_ratio[topic] = 1
        #attr6 emoticon
        emoticon_string = user_dict['emoticon']
        if emoticon_string:
            emoticon_dict = json.loads(emoticon_string)
            for emoticon in emoticon_dict:
                try:
                    emoticon_ratio[emoticon] += 1
                except:
                    emoticon_ratio[emoticon] = 1
        #attr7 keywords
        keyword_string = user_dict['keywords']
        if keyword_string:
            keyword_dict = json.loads(keyword_string)
            for keyword in keyword_dict:
                try:
                    keyword_ratio[keyword] += keyword_dict[keyword]
                except:
                    keyword_ratio[keyword] = keyword_dict[keyword]
        #attr8 importance distribution
        importance = user_dict['importance']
        importance_rank = get_index_rank(importance, 'importance')
        importance_list.append(int(importance_rank))
        #attr9 activeness distribution
        activeness = user_dict['activeness']
        activeness_rank = get_index_rank(activeness, 'activeness')
        activeness_list.append(int(activeness_rank))
        #attr10 influence distribution
        influence = user_dict['influence']
        influence_rank = get_index_rank(influence, 'influence')
        influence_list.append(int(influence_rank))
        #attr11 psycho_status ratio
        psycho_status_string = user_dict['psycho_status']
        if psycho_status_string:
            psycho_status_dict = json.loads(psycho_status_string)
            for psycho_status in psycho_status_dict:
                try:
                    psycho_status_ratio[psycho_status] += psycho_status_dict[psycho_status]
                except:
                    psycho_status_ratio[psycho_status] = psycho_status_dict[psycho_status]
        #attr12 psycho_feature ratio
        psycho_feature_string = user_dict['psycho_feature']
        if psycho_feature_string:
            psycho_feature_list = psycho_feature_string.split('_')
            for psycho_feature in psycho_feature_list:
                try:
                    psycho_feature_ratio[psycho_feature] += 1
                except:
                    psycho_feature_ratio[psycho_feature] = 1
        #attr13 activity geo ratio
        activity_geo_string = user_dict['activity_geo_dict']
        if activity_geo_string:
            activity_geo_dict = json.loads(activity_geo_string)
            for activity_geo in activity_geo_dict:
                city_list = activity_geo.split('\t')
                city = city_list[len(city_list)-1]
                try:
                    activity_geo_ratio[city] += activity_geo_dict[activity_geo]
                except:
                    activity_geo_ratio[city] = activity_geo_dict[activity_geo]
        #attr14 hashtag
        hashtag_string = user_dict['hashtag_dict']
        if hashtag_string:
            hashtag_dict = json.loads(hashtag_string)
            for hashtag in hashtag_dict:
                try:
                    hashtag_ratio[hashtag] += hashtag_dict[hashtag]
                except:
                    hashtag_ratio[hashtag] = hashtag_dict[hashtag]
    #print 'importance_list:', importance_list
    p, t = np.histogram(importance_list, bins=5, normed=False)
    importance_his = [p.tolist(), t.tolist()]
    #print 'importance_his:', importance_his
    p, t = np.histogram(activeness_list, bins=5, normed=False)
    activeness_his = [p.tolist(), t.tolist()]
    p, t = np.histogram(influence_list, bins=5, normed=False)
    influence_his = [p.tolist(), t.tolist()]
    result['gender'] = json.dumps(gender_ratio)
    result['verified'] = json.dumps(verified_ratio)
    result['online_pattern'] = json.dumps(online_pattern_ratio)
    result['domain'] = json.dumps(domain_ratio)
    result['topic'] = json.dumps(topic_ratio)
    result['psycho_status'] = json.dumps(psycho_status_ratio)
    result['psycho_feature'] = json.dumps(psycho_feature_ratio)
    result['emoticon'] = json.dumps(emoticon_ratio)
    result['keywords'] = json.dumps(keyword_ratio)
    result['hashtag'] = json.dumps(hashtag_ratio)
    result['activity_geo'] = json.dumps(activity_geo_ratio)
    result['importance_his'] = json.dumps(importance_his)
    result['activeness_his'] = json.dumps(activeness_his)
    result['influence_his'] = json.dumps(influence_his)
    return result
'''


#use to get db number for retweet/be_retweet/comment/be_comment
#input: timestamp
#output: db_number
def get_db_num(timestamp):
    date = ts2datetime(timestamp)
    date_ts = datetime2ts(date)
    db_number = (((date_ts - r_begin_ts) / DAY) / 7) % 2 + 1
    
    return db_number



#use to get group social attribute
#write in version: 16-01-23
#input: uid_list
#output: group social attribute
def get_attr_social(uid_list):
    result = {}
    #step1: get db number
    timestamp = int(time.time())
    db_num = get_db_num(timestamp)
    #step2: split uid list to iter mget
    iter_count = 0
    all_user_count = len(uid_list)
    while iter_count < all_user_count:
        iter_uid_list = uid_list[iter_count:iter_count+DETECT_ITER_COUNT]
        try:
            retweet_result = es_retweet.mget(index=retweet_index_name, doc_type=retweet_index_type, body={'ids':iter_uid})['docs']
        except:
            retweet_result = []
        try:
            be_retweet_result = es_comment.mget(index=be_retweet_index_name, doc_type=be_retweet_index_type, body={'ids':iter_uid})['docs']
        except:
            be_retweet_result = []

    #step2: mget retweet
    #step3: mget be_retweet
    #step4: mget comment
    #step5: mget be_comment
    #step6: union four type social user list
    #step7: filter to identify who is in user_portrait or not
    #step8: compute in-portrait index, out_portrait index
    return result


#abandon in version:16-01-23
'''
def get_attr_social(uid_list):
    result = {}
    union_dict = {}
    union_edge_count = 0
    union_weibo_count = 0
    union_user_set = set()
    group_user_set = set(uid_list)
    be_retweeted_out = 0
    be_retweeted_count_out = 0
    retweet_relation = []
    out_beretweet_relation = []
    for uid in uid_list:
        in_stat_results = dict()
        out_stat_results = dict()
        for db_num in r_dict:
            r_db = r_dict[db_num]
            ruid_results = r_db.hgetall('retweet_'+str(uid))
            #print 'len ruid_result:', len(ruid_results)
            if ruid_results:
                for ruid in ruid_results:
                    try:
                        in_stat_results[ruid] += ruid_results[ruid]
                    except:
                        in_stat_results[ruid] = ruid_results[ruid]
            br_uid_results = r_db.hgetall('be_retweet_'+str(uid))
            #print 'len br_uid_results:', len(br_uid_results)
            if br_uid_results:
                for br_uid in br_uid_results:
                    try:
                        out_stat_results[br_uid] += br_uid_results[br_uid]
                    except:
                        out_stat_results[br_uid] = br_uid_results[br_uid]
        # record the retweet relation in group uid
        uid_retweet_relation = [[uid, user, int(in_stat_results[user])] for user in in_stat_results if user in uid_list and user != uid]
        retweet_relation.extend(uid_retweet_relation)
        
        # record the be_retweet relation out group uid but in user_portrait
        uid_beretweet_relation = []
        uid_beretweet = [user for user in out_stat_results if user not in uid_list]
        es_portrait_result = es.mget(index='user_portrait', doc_type='user', body={'ids':uid_beretweet})['docs']
        for be_retweet_item in es_portrait_result:
            br_uid = be_retweet_item['_id']
            beretweet_count = int(out_stat_results[br_uid])
            try:
                be_retweet_source = be_retweet_item['_source']
                if be_retweet_source['influence']>=900:
                    uid_beretweet_relation.append([uid, br_uid, be_retweet_source['uname'], beretweet_count, be_retweet_source['influence']])
            except:
                next
        out_beretweet_relation.extend(uid_beretweet_relation)

        retweet_user_set = set(in_stat_results.keys())
        union_set = retweet_user_set & (group_user_set - set([uid]))
        union_edge_count += len(union_set) # count the retweet edge number
        if union_set:
            for ruid in union_set:
                union_weibo_count += int(in_stat_results[ruid])
        union_user_set = union_user_set | union_set

        #use to count the beretweeted by user who is out of the group
        be_retweeted_user_set = set(out_stat_results.keys())
        subtract_set = be_retweeted_user_set - set(uid_list)
        be_retweeted_out += len(subtract_set)
        be_retweeted_count_out_list = [int(out_stat_results[br_uid]) for br_uid in subtract_set]
        #print 'be_retweeted_count_out_list:', be_retweeted_count_out_list
        be_retweeted_count_out += sum(be_retweeted_count_out_list)

    result['density'] = float(union_edge_count) / (len(uid_list) * (len(uid_list)-1))
    result['retweet_weibo_count'] = float(union_weibo_count) / len(uid_list)
    result['retweet_user_count'] = float(len(union_user_set)) / len(uid_list)
    result['be_retweeted_count_out'] = be_retweeted_count_out
    result['be_retweeted_out'] = be_retweeted_out
    if retweet_relation!=[]:
        sort_retweet_relation = sorted(retweet_relation, key=lambda x:x[2], reverse=True)
    else:
        sort_retweet_relation = []
    result['retweet_relation'] = json.dumps(sort_retweet_relation)
    
    if out_beretweet_relation!=[]:
        sort_out_beretweet_relation = sorted(out_beretweet_relation, key=lambda x:x[4], reverse=True)
    else:
        sort_out_beretweet_relation = []
    result['out_beretweet_relation'] = json.dumps(sort_out_beretweet_relation)
    #print 'be_retweeted_out, be_retweeted_count_out:', be_retweeted_out, be_retweeted_count_out
    #print 'result:', result
    #print 'out_beretweet_relation:', sort_out_beretweet_relation
    return result
'''



#use to get user activity trend
#input: uid_list
#output: results {'activity_trend':[], 'acitivity_time':[dict, description]}
def get_attr_trend(uid_list):
    result = {}
    now_ts = time.time()
    date = ts2datetime(now_ts - DAY)
    timestamp = datetime2ts(date)
    #test
    timestamp = datetime2ts('2013-09-08')
    time_result = dict()
    segment_result = dict()
    user_segment_result = dict() # user_segment_result = {uid1:{time_segment1:count1, time_segment2:count2}, uid2:...}
    for i in range(1, 8):
        ts = timestamp - i*DAY
        r_result = r_cluster.hmget('activity_'+str(ts), uid_list)
        for item in r_result:
            if item:
                item = json.loads(item)
                for segment in item:
                    #for all user activity trend
                    try:
                        time_result[int(segment)/16*15*60*16+ts] += item[segment]
                    except:
                        time_result[int(segment)/16*15*60*16+ts] = item[segment]
                    #for user activity time
                    if uid in user_segment_result:
                        try:
                           user_ segment_result[uid][int(segment)/16*15*60*16] += item[segment]
                        except:
                            user_segment_result[uid][int(segment)/16*15*60*16] = item[segment]
                    else:
                        time_key = int(segment)/16*15*60*16
                        user_segment_result[uid] = {time_key: item[segment]}
    trend_list = []
    for i in range(1, 8):
        ts = timestamp - i*DAY
        for j in range(0, 6):
            time_seg = ts + j*15*60*16
            if time_seg in time_result:
                trend_list.append((time_seg, time_result[time_seg]))
            else:
                trend_list.append((time_seg, 0))
    sort_trend_list = sorted(trend_list, key=lambda x:x[0], reverse=False)
    result['activity_trend'] = json.dumps(sort_trend_list)

    #for user activity time
    for uid in uid_list:
        try:
            user_dict = user_segment_result[uid]
        except:
            user_dict = {}
        if user_dict != {}:
            sort_user_dict = sorted(user_dict.items(), key=lambda x:x[1], reverse=True)
            user_main_time = sort_user_dict[0][0]
            try:
                segment_result[user_main_time] += 1
            except:
                segment_result[user_main_time] = 1
    
    sort_segment_result = sorted(segment_result.items(), key=lambda x:x[1], reverse=True)
    top_segment_user_count = sort_segment_result[0][1]
    top_user_ratio = float(top_segment_user_count) / len(uid_list)
    if top_user_ratio >= GROUP_ACTIVITY_TIME_THRESHOLD[-1]:
        activity_time_description = GROUP_ACTIVITY_TIME_DESCRIPTION_DICT['2']
    elif top_user_ratio <= GROUP_ACTVITY_TIME_THRESHOLD[0]:
        activity_time_description = GROUP_ACTIVITY_TIME_DESCRIPTION_DICT['0']
    else:
        activity_time_description = GROUP_ACTIVITY_TIME_DESCRIPTION_DICT['1']

    result['activity_time'] = json.dumps([segment_result, activity_time_description]) # [(time_segment,user_count), (), (),...]

    return result


#use to get user evaluate index trend
#input: uid_list
#output: evaluate_index_trend
def get_attr_evaluate_trend(uid_list):
    results = {}
    activeness_dict = {} # {ts1:{uid:index, uid:index}, ts2:{}, ts3:{},...}
    influence_dict = {} # {ts1:{uid:index, uid:index}, ts2:{}, ...}
    try:
        es_user_result = es_copy_portrait.mget(index=copy_portrait_index_name, doc_type=copy_portrait_index_type, \
                body={'ids':uid_list})['docs']
    except:
        es_user_result = []
  
    for user_dict in es_user_result:
        uid = user_dict['_id']
        for index_key in user_dict:
            index_key_list = index_key.split('_')
            #get user activeness index
            if index_key_list[0]=='activeness':
                date = index_key_list[1] # 2013-09-07
                ts = datetime2ts(date)
                if ts in activeness_dict:
                    activeness_dict[ts][uid] = user_dict[index_key]
                else:
                    activeness_dict[ts] = {uid: user_dict[index_key]}

            #get user influence index
            if len(index_key_list)==1 and index_key != 'uid':
                date = index_key # 20130907
                ts = datetimestr2ts(date)
                if ts in influence_dict:
                    influence_dict[ts][uid] = user_dict[index_key]
                else:
                    influence_dict[ts] = {uid: user_dict[index_key]}
    #get activeness trend--ave_value/min_value/max_value
    activeness_time_list = []
    ave_list = []
    max_list = []
    min_list = []
    #get uname by uid
    uid2uname_dict = {}
    try:
        user_portrait_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type, \
                body={'ids':uid_list}, _source=False, fields=['uname'])['hits']['hits']
    except:
        user_portrait_result = []
    for item in user_portrait_result:
        uid = item['_id']
        uname = item['_source']['uname']
        uid2uname[uid] = uname

    sort_activeness_dict = sorted(activeness_dict.items(), key=lambda x:x[1])
    main_max_activeness_dict = {}
    main_min_activeness_dict = {}
    for ts_item in sort_activeness_dict:
        timestamp = ts_item[0]
        ts_index_dict = ts_item[1]
        activeness_time_list.append(ts2date(timestamp))
        ave_value = sum(ts_index_dict.values())
        sort_ts_index = sorted(ts_index_dict.items(), key=lambda x:x[1], reverse=True)
        #get max/min uid-uname
        max_uname = uid2uname[sort_ts_index[0][1]]
        min_uname = uid2uname[sort_ts_index[-1][1]]
        max_list.append([sort_ts_index[0][0], sort_ts_index[0][1], uname])
        min_list.append([sort_ts_index[-1][0], sort_ts_index[-1][1], uname])
        #get main max uid-uname
        max_uid_uname = sort_ts_index[0][1] + '&' + max_uname
        try:
            main_max_activeness_dict[max_uid_uname] += 1
        except:
            main_max_activeness_dict[max_uid_uname] = 1
        #get main min uid-uname
        min_uid_uname = sort_ts_index[-1][1] + '&' + min_uname
        try:
            main_min_activeness_dict[min_uid_uname] += 1
        except:
            main_min_activeness_dict[min_uid_uname] = 1
    
    sort_main_max_activeness = sorted(main_max_activeness_dict.items(), key=lambda x:x[1], reverse=True)
    sort_main_min_activeness = sorted(main_min_activeness_dict.items(), key=lambda x:x[1], reverse=True)
    results['activeness'] = {'time_list':activeness_time_list, 'ave_list':ave_list, 'max_list':max_list,\
            'min_list':min_list, 'main_max':sort_main_max_activeness[:5], 'main_min':sort_main_min_activeness[:5]}
    #get influence trend--ave_value/min_value/max_value
    influence_time_list = []
    ave_list = []
    max_list = []
    min_list = []
    sort_influence_dict = sorted(influence_dict.items(), key=lambda x:x[1])
    main_max_influence_dict = {}
    main_min_influence_dict = {}
    for ts_item in sort_influence_dict:
        timestamp = ts_item[0]
        ts_index_dict = ts_item[1]
        influence_time_list.append(ts2date(timestamp))
        ave_value = sum(ts_index_dict.values())
        sort_ts_index = sorted(ts_index_dict.items(), key=lambda x:x[1], reverse=True)
        #get max/min uid-uname
        max_uname = uid2uname[sort_ts_index[0][1]]
        min_uname = uid2uanme[sort_ts_index[-1][1]]
        max_list.append([sort_ts_index[0][0], sort_ts_index[0][1], uname])
        min_list.append([sort_ts_index[-1][0], sort_ts_index[-1][1], uname])
        #get main max uid-uname
        max_uid_uname = sort_ts_index[0][1] + '&' + max_uname
        try:
            main_max_influence_dict[max_uid_uname] += 1
        except:
            main_max_influence_dict[max_uid_uname] = 1
        #get main min uid-uname
        min_uid_uname = sort_ts_index[-1][1] + '&' + min_uname
        try:
            main_min_influence_dict[min_uid_uname] += 1
        except:
            main_min_influence_dict[min_uid_uname] = 1
    
    sort_main_max_influence = sorted(main_max_influence_dict.items(), key=lambda x:x[1], reverse=True)
    sort_main_min_influence = sorted(main_min_influence_dict.items(), key=lambda x:x[1], reverse=True)
    results['influence'] = {'time_list':inflluence_time_list, 'ave_list':ave_list, 'max_list':max_list,\
            'min_list':min_list, 'main_max':sort_main_max_influence[:5], 'main_min':sort_main_min_influence[:5]}
    
    
    return results



# get importance max & activeness max & influence max to normalize
def get_evaluate_max():
    max_result = {}
    index_name = 'user_portrait'
    index_type = 'user'
    evaluate_index = ['activeness', 'importance', 'influence']
    for evaluate in evaluate_index:
        query_body = {
            'query': {
                'match_all':{}
                },
            'size': 1,
            'sort': [{evaluate:{'order': 'desc'}}]
            }
        try:
            result = es.search(index=index_name, doc_type=index_type, body=query_body)['hits']['hits']
        except Exception, e:
            raise e
        max_evaluate = result[0]['_source'][evaluate]
        max_result[evaluate] = max_evaluate

    return max_result


def get_attr_bci(uid_list):
    results = []
    now_ts = time.time()
    now_date = ts2datetime(now_ts - 24*3600)
    ts = datetime2ts(now_date)
    #test
    ts = datetime2ts('2013-09-07')
    user_results = {} # {'uid':{'origin_max..':[], ''}}
    total_weibo_number = 0
    
    fans_number = 0
    origin_weibo_number = 0
    retweeted_weibo_number = 0
    origin_weibo_retweeted_total_number = 0
    origin_weibo_comment_total_number = 0
    retweeted_weibo_retweeted_total_number = 0
    retweeted_weibo_comment_total_number = 0

    origin_weibo_retweeted_top = 0
    origin_weibo_comment_top = 0
    retweeted_weibo_retweeted_top = 0
    retweeted_weibo_comment_top = 0
    influence_dict = {}

    for i in range(0, 7):
        timestamp = ts - i*24*3600
        date = ts2datetime(timestamp)
        hash_key = ''.join(date.split('-'))
        es_user_results = es_cluster.mget(index=hash_key, doc_type='bci', body={'ids':uid_list})['docs']
        for user_dict in es_user_results:
            try:
                user_item = user_dict['_source']
            except:
                next
            uid = user_item['user']
            total_weibo_number += user_item['origin_weibo_number']
            total_weibo_number += user_item['retweeted_weibo_number']
            
            # yuankun revise
            origin_weibo_number += user_item['origin_weibo_number']
            retweeted_weibo_number += user_item['retweeted_weibo_number']
            origin_weibo_retweeted_top += user_item['origin_weibo_retweeted_top_number']
            origin_weibo_comment_top += user_item['origin_weibo_comment_top_number']
            retweeted_weibo_retweeted_top += user_item['retweeted_weibo_retweeted_top_number']
            retweeted_weibo_comment_top += user_item['retweeted_weibo_comment_top_number']
            #print 'user_item:', user_item
            if uid in user_results:
                try:
                    user_results[uid]['origin_weibo_retweeted_top'].append([user_item['origin_weibo_retweeted_top_number'], user_item['origin_weibo_top_retweeted_id']])
                    user_results[uid]['origin_weibo_comment_top'].append([user_item['origin_weibo_comment_top_number'], user_item['origin_weibo_top_comment_id']])
                    user_results[uid]['retweeted_weibo_retweeted_top'].append([user_item['retweeted_weibo_retweeted_top_number'], user_item['retweeted_weibo_top_retweeted_id']])
                    user_results[uid]['retweeted_weibo_comment_top'].append([user_item['retweeted_weibo_comment_top_number'], user_item['retweeted_weibo_top_comment_id']])
                except:
                    user_results[uid]['origin_weibo_retweeted_top'] = [[user_item['origin_weibo_retweeted_top_number'], user_item['origin_weibo_top_retweeted_id']]]
                    user_results[uid]['origin_weibo_comment_top'] = [[user_item['origin_weibo_comment_top_number'], user_item['origin_weibo_top_comment_id']]]
                    user_results[uid]['retweeted_weibo_retweeted_top'] = [[user_item['retweeted_weibo_retweeted_top_number'], user_item['retweeted_weibo_top_retweeted_id']]]
                    user_results[uid]['retweeted_weibo_comment_top'] = [[user_item['retweeted_weibo_comment_top_number'], user_item['retweeted_weibo_top_comment_id']]]
            else:
                #print 'user_item:', [[user_item['origin_weibo_retweeted_top_number'], user_item['origin_weibo_top_retweeted_id']]]
                user_results[uid] = {'origin_weibo_retweeted_top':[[user_item['origin_weibo_retweeted_top_number'], user_item['origin_weibo_top_retweeted_id']]]}
                user_results[uid] = {'origin_weibo_comment_top': [[user_item['origin_weibo_comment_top_number'], user_item['origin_weibo_top_comment_id']]]}
                user_results[uid] = {'retweeted_weibo_retweeted_top': [[user_item['retweeted_weibo_retweeted_top_number'], user_item['retweeted_weibo_top_retweeted_id']]]}
                user_results[uid] = {'retweeted_weibo_comment_top': [[user_item['retweeted_weibo_comment_top_number'], user_item['retweeted_weibo_top_comment_id']]]}
            
            # yuankun need
            #print 'fan_num:', user_item['user_fansnum'], type(user_item['user_fansnum']), type(fans_number)
            fans_number += int(user_item['user_fansnum'])
            origin_weibo_retweeted_total_number += user_item['origin_weibo_retweeted_total_number']
            origin_weibo_comment_total_number += user_item['origin_weibo_comment_total_number']
            retweeted_weibo_retweeted_total_number += user_item['retweeted_weibo_retweeted_total_number']
            retweeted_weibo_comment_total_number += user_item['retweeted_weibo_comment_total_number']

    user_portrait_result = es.mget(index='user_portrait', doc_type='user', body={'ids':uid_list})['docs']
    #print 'user_portrait_result:', user_portrait_result[0]

    # get activeness max & importance max & influence max to normalize
    evaluate_max_result = get_evaluate_max()

    for user_portrait in user_portrait_result:
        #print 'user_portrait:', user_portrait
        try:
            user_portrait_dict = user_portrait['_source']
            #print 'user_portrait_dict:', user_portrait_dict
            uname = user_portrait_dict['uname']
            importance = user_portrait_dict['importance']
            normal_importance = math.log((importance / evaluate_max_result['importance']) * 9 + 1, 10) * 100
            activeness = user_portrait_dict['activeness']
            normal_activeness = math.log(activeness / evaluate_max_result['activeness'] * 9 + 1, 10) * 100
            influence = user_portrait_dict['influence']
            normal_influence = math.log(influence / evaluate_max_result['influence'] * 9 + 1, 10) * 100
        except:
            uname = ''
            normal_importance = ''
            normal_activeness = ''
            normal_influence = ''
        #print 'user_portrait_dict:', user_portrait_dict
        uid = user_portrait_dict['uid']
        user_item_dict = user_results[uid]
        origin_weibo_retweeted_top_item = sorted(user_item_dict['origin_weibo_retweeted_top'], key=lambda x:x[0], reverse=True)[0]
        origin_weibo_comment_top_item = sorted(user_item_dict['origin_weibo_comment_top'], key=lambda x:x[0], reverse=True)[0]
        retweeted_weibo_retweeted_top_item = sorted(user_item_dict['retweeted_weibo_retweeted_top'], key=lambda x:x[0], reverse=True)[0]
        retweeted_weibo_comment_top_item = sorted(user_item_dict['retweeted_weibo_comment_top'], key=lambda x:x[0], reverse=True)[0]
        
        results.append([uid, uname, normal_activeness, normal_importance, normal_influence, origin_weibo_retweeted_top_item ,\
                        origin_weibo_comment_top_item, retweeted_weibo_retweeted_top_item, \
                        retweeted_weibo_comment_top_item])

    #yuankun need
    influence_dict['origin_weibo_retweeted_average_number'] = origin_weibo_retweeted_total_number/origin_weibo_number/7
    influence_dict['origin_weibo_comment_average_number'] = origin_weibo_comment_total_number/origin_weibo_number/7
    influence_dict['retweeted_weibo_retweeted_average_number'] = retweeted_weibo_retweeted_total_number/retweeted_weibo_number/7
    influence_dict['retweeted_weibo_comment_average_number'] = retweeted_weibo_comment_total_number/retweeted_weibo_number/7
    influence_dict['origin_weibo_retweeted_top_number'] = origin_weibo_retweeted_top/len(uid_list)/7
    influence_dict['origin_weibo_comment_top_number'] = origin_weibo_comment_top/len(uid_list)/7
    influence_dict['retweeted_weibo_retweeted_top_number'] = retweeted_weibo_retweeted_top/len(uid_list)/7
    influence_dict['retweeted_weibo_comment_top_number'] = retweeted_weibo_comment_top/len(uid_list)/7
    influence_dict['fans_number'] = fans_number
    influence_dict['total_weibo_number'] = total_weibo_number
    #print 'results:', results
    return {'user_influence_list': json.dumps(results), 'total_weibo_number': total_weibo_number}, influence_dict
           

'''
def get_attr_bci(uid_list):
    result = dict()
    influence_dict = {}
    now_ts = time.time()
    now_date = ts2datetime(now_ts-24*3600)
    ts = datetime2ts(now_date)
    #test
    ts = datetime2ts('2013-09-07')
    total_weibo_number = 0
    origin_max_retweeted_number = 0
    origin_max_retweeted_id = ''
    origin_max_retweeted_user = ''
    origin_max_comment_number = 0
    origin_max_comment_id = ''
    origin_max_comment_user = ''
    retweet_max_retweeted_number = 0
    retweet_max_retweeted_id = ''
    retweet_max_retweeted_user = ''
    retweet_max_comment_number = 0
    retweet_max_comment_id = ''
    retweet_max_comment_user = ''


    fans_number = 0
    origin_weibo_number = 0
    retweeted_weibo_number = 0
    origin_weibo_retweeted_total_number = 0
    origin_weibo_comment_total_number = 0
    retweeted_weibo_retweeted_total_number = 0
    retweeted_weibo_comment_total_number = 0

    origin_weibo_retweeted_top = 0
    origin_weibo_comment_top = 0
    retweeted_weibo_retweeted_top = 0
    retweeted_weibo_comment_top = 0

    for i in range(0, 7):
        timestamp = ts - i*24*3600
        date = ts2datetime(timestamp)
        hash_key = ''.join(date.split('-'))
        user_results = es_cluster.mget(index=hash_key, doc_type='bci', body={'ids':uid_list})['docs']
        #print 'user_results:', user_results
        for user_dict in user_results:
        #try:
            try:
                user_item = user_dict['_source']
            except:
                next
            total_weibo_number += user_item['origin_weibo_number']
            total_weibo_number += user_item['retweeted_weibo_number']

            # yuankun revise
            origin_weibo_number += user_item['origin_weibo_number']
            retweeted_weibo_number += user_item['retweeted_weibo_number']
            origin_weibo_retweeted_top += user_item['origin_weibo_retweeted_top_number']
            origin_weibo_comment_top += user_item['origin_weibo_comment_top_number']
            retweeted_weibo_retweeted_top += user_item['retweeted_weibo_retweeted_top_number']
            retweeted_weibo_comment_top += user_item['retweeted_weibo_comment_top_number']

            origin_weibo_retweeted_top_number = user_item['origin_weibo_retweeted_top_number']
            if origin_weibo_retweeted_top_number >= origin_max_retweeted_number:
                origin_max_retweeted_number = origin_weibo_retweeted_top_number
                origin_max_retweeted_id = user_item['origin_weibo_top_retweeted_id']
                origin_max_retweeted_user = user_item['user']
            origin_weibo_comment_top_number = user_item['origin_weibo_comment_top_number']
            if origin_weibo_comment_top_number >= origin_max_comment_number:
                origin_max_comment_number = origin_weibo_comment_top_number
                origin_max_comment_id = user_item['origin_weibo_top_comment_id']
                origin_max_comment_user = user_item['user']
            retweeted_weibo_retweeted_top_number = user_item['retweeted_weibo_retweeted_top_number']
            if retweeted_weibo_retweeted_top_number >= retweet_max_retweeted_number:
                retweet_max_retweeted_number = retweeted_weibo_retweeted_top_number
                retweet_max_retweeted_id = user_item['retweeted_weibo_top_retweeted_id']
                retweet_max_retweeted_user = user_item['user']
            retweeted_weibo_comment_top_number = user_item['retweeted_weibo_comment_top_number']
            if retweeted_weibo_comment_top_number >= retweet_max_comment_number:
                retweet_max_comment_number = retweeted_weibo_comment_top_number
                retweet_max_comment_id = user_item['retweeted_weibo_top_comment_id']
                retweet_max_comment_user = user_item['user']


            # yuankun revise
            fans_number += user_item['user_fansnum']
            origin_weibo_retweeted_total_number += user_item['origin_weibo_retweeted_total_number']
            origin_weibo_comment_total_number += user_item['origin_weibo_comment_total_number']
            retweeted_weibo_retweeted_total_number += user_item['retweeted_weibo_retweeted_total_number']
            retweeted_weibo_comment_total_number += user_item['retweeted_weibo_comment_total_number']


        #except:
        #pass

    # yuankun revise

    influence_dict['origin_weibo_retweeted_average_number'] = origin_weibo_retweeted_total_number/origin_weibo_number/7
    influence_dict['origin_weibo_comment_average_number'] = origin_weibo_comment_total_number/origin_weibo_number/7
    influence_dict['retweeted_weibo_retweeted_average_number'] = retweeted_weibo_retweeted_total_number/retweeted_weibo_number/7
    influence_dict['retweeted_weibo_comment_average_number'] = retweeted_weibo_comment_total_number/retweeted_weibo_number/7
    influence_dict['origin_weibo_retweeted_top_number'] = origin_weibo_retweeted_top/len(uid_list)/7
    influence_dict['origin_weibo_comment_top_number'] = origin_weibo_comment_top/len(uid_list)/7
    influence_dict['retweeted_weibo_retweeted_top_number'] = retweeted_weibo_retweeted_top/len(uid_list)/7
    influence_dict['retweeted_weibo_comment_top_number'] = retweeted_weibo_comment_top/len(uid_list)/7
    influence_dict['fans_number'] = fans_number
    influence_dict['total_weibo_number'] = total_weibo_number

    result['origin_max_retweeted_number'] = origin_max_retweeted_number
    result['origin_max_retweeted_id'] = origin_max_retweeted_id
    result['origin_max_comment_number'] = origin_max_comment_number
    result['origin_max_comment_id'] = origin_max_comment_id
    result['retweet_max_retweeted_number'] = retweet_max_retweeted_number
    result['retweet_max_retweeted_id'] = retweet_max_retweeted_number
    result['retweet_max_comment_number'] = retweet_max_comment_number
    result['retweet_max_comment_id'] = retweet_max_comment_id
    result['total_weibo_number'] = total_weibo_number
    result['origin_max_retweeted_user'] = origin_max_retweeted_user
    result['origin_max_comment_user'] = origin_max_comment_user
    result['retweet_max_retweeted_user'] = retweet_max_retweeted_user
    result['retweet_max_comment_user'] = retweet_max_comment_user
    #print 'result:', result
    return result,influence_dict
'''

# yuankun revise
def get_attr_influence(uid_list, bci_dict):
    result = {}
    weight = [0.3, 0.4, 0.2, 0.1]
    influence = weight[0]*(0.3*math.log(1+bci_dict['origin_weibo_retweeted_top_number'])+0.3*math.log(1+bci_dict['origin_weibo_comment_top_number'])+\
                0.2*math.log(1+bci_dict['retweeted_weibo_retweeted_top_number'])+0.2*math.log(1+bci_dict['retweeted_weibo_comment_top_number'])) + \
                weight[1]*(0.3*math.log(1+bci_dict['origin_weibo_retweeted_average_number'])+0.3*math.log(1+bci_dict['origin_weibo_comment_average_number']) + \
                0.2*math.log(1+bci_dict['retweeted_weibo_retweeted_average_number'])+0.2*math.log(1+bci_dict['retweeted_weibo_comment_average_number'])) + \
                weight[2]*math.log(1+bci_dict['fans_number']) + weight[3]*math.log(1+bci_dict['total_weibo_number'])
    influence = 300 * influence

    result['influence'] = influence
    return result # result = {'influence': count}


def get_attr_activeness(activity_trend, total_number, activity_geo):
    result = dict()
    #print 'activity_trend:', activity_trend
    sort_activity_trend = sorted(activity_trend, key=lambda x:x[0], reverse=False)
    #print 'sort_activity_trend:', sort_activity_trend
    activity_list = [item[1] for item in sort_activity_trend]
    #print 'activity_list:', activity_list
    signal = np.array(activity_list)
    fftResult = np.abs(np.fft.fft(signal)) ** 2
    n = signal.size
    freq = np.fft.fftfreq(n, d=1)
    i = 0
    max_val = 0
    max_freq = 0
    for val in fftResult:
        if val>max_val and freq[i]>0:
            max_val = val
            max_freq = freq[i]
        i = i + 1
    #print 'max_freq:', max_freq
    result['activeness'] = activeness_weight_dict['activity_time'] * math.log(max_freq + 1) +\
             activeness_weight_dict['activity_geo'] * math.log(len(activity_geo) + 1) +\
             activeness_weight_dict['statusnum'] * math.log(total_number + 1)
    #print 'result:', result
    return result


def get_attr_importance(domain_dict, topic_dict, count, be_retweeted_count, be_retweeted_weibo_count):
    result = dict()
    sort_domain = sorted(domain_dict.items(), key=lambda x:x[1], reverse=True)
    sort_topic = sorted(topic_dict.items(), key=lambda x:x[1], reverse=True)
    #print 'sort_domain:', sort_domain
    #print 'sort_topic:', sort_topic
    domain_list = sort_domain[:5]
    topic_list = sort_topic[:5]
    domain_result = 0
    for domain in domain_list:
        try:
            domain_result = domain_weight_dict[domain] * domain_dict[domain]
        except:
            pass
    topic_result = 0
    for topic in topic_list:
        try:
            topic_result = topic_weight_dict[topic] * topic_dict[topic]
        except:
            pass
    #print 'topic_result, domain_result:', topic_result, domain_result
    result['importance'] = importance_weight_dict['count'] * math.log(count + 1) + \
                           importance_weight_dict['topic'] * math.log(topic_result + 1) + \
                           importance_weight_dict['domain'] * math.log(domain_result + 1) +\
                           importance_weight_dict['be_retweeted_out'] * math.log(be_retweeted_count + 1) +\
                           importance_weight_dict['be_retweeted_count_out'] * math.log(be_retweeted_weibo_count + 1)

    #print 'result:', result
    return result

def get_attr_tightness(density, retweet_weibo_count, retweet_user_count):
    result = dict()
    result['tightness'] = tightness_weight_dict['density'] * math.log(density + 1) +\
                          tightness_weight_dict['retweet_weibo_count'] * math.log(retweet_weibo_count + 1) +\
                          tightness_weight_dict['retweet_user_count'] * math.log(retweet_user_count + 1)
    #print 'tightness:', result
    return result

#abandon in version: 16-01-24
'''
def get_attr_geo_track(uid_list):
    date_results = [] # results = {'2013-09-01':[(geo1, count1), (geo2, track2)], '2013-09-02'...} 7day
    now_ts = time.time()
    now_date = ts2datetime(now_ts)
    #test
    now_date = '2013-09-08'
    ts = datetime2ts(now_date)
    for i in range(7, 0, -1):
        timestamp = ts - i*24*3600
        #print 'timestamp:', ts2datetime(timestamp)
        ip_dict = dict()
        results = r_cluster.hmget('ip_'+str(timestamp), uid_list)
        #print 'results:',results
        for item in results:
            if item:
                item_dict = json.loads(item)
                #print 'item_dict:', item_dict
                for ip_item in item_dict:
                    try:
                        ip_dict[ip_item] += item_dict[ip_item]
                    except:
                        ip_dict[ip_item] = item_dict[ip_item]
        geo_dict = ip2geo(ip_dict)
        sort_geo_dict = sorted(geo_dict.items(), key=lambda x:x[1], reverse=True)
        date_key = ts2datetime(timestamp)
        date_results.append([date_key, sort_geo_dict[:2]])
    #print 'results:', date_results
    return {'geo_track': json.dumps(date_results)}
'''

def ip2geo(ip_dict):
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
            city_list = city.split('\t')
            city = city_list[len(city_list)-1]
            try:
                geo_dict[city] += ip_dict[ip]
            except:
                geo_dict[city] = ip_dict[ip]
    return geo_dict

'''
def compute_group_task():
    results = dict()
    while True:
        task = r.rpop(group_analysis_queue_name)
        if not task:
            break
        else:
            task = json.loads(task)
            #uid_list should be keep list type to save in es
            uid_list = task['uid_list']
            task_name = task['task_name']
            submit_date = task['submit_date']
            submit_state = task['state']
            # attr1 member count
            results['count'] = len(uid_list)
            # get attr from es_user_portrait
            attr_in_portrait = get_attr_portrait(uid_list)
            results['task_name'] = task_name
            results['uid_list'] = uid_list
            results['submit_date'] = submit_date
            results['state'] = task['state']
            results = dict(results, **attr_in_portrait)
            attr_in_social = get_attr_social(uid_list)
            results = dict(results, **attr_in_social)
            attr_weibo_trend = get_attr_trend(uid_list)
            results = dict(results, **attr_weibo_trend)
            attr_user_bci = get_attr_bci(uid_list)
            results = dict(results, **attr_user_bci)
            attr_group_activeness = get_attr_activeness(json.loads(results['activity_trend']), results['total_weibo_number'], json.loads(results['activity_geo']))
            results = dict(results, **attr_group_activeness)
            attr_group_importance = get_attr_importance(json.loads(results['domain']), json.loads(results['topic']), results['count'], results['be_retweeted_out'],results['be_retweeted_count_out'])
            results = dict(results , **attr_group_importance)
            attr_group_tightness = get_attr_tightness(results['density'], results['retweet_weibo_count'], results['retweet_user_count'])
            results = dict(results, **attr_group_tightness)
            attr_group_influence = get_attr_influence(uid_list)
            results = dict(results, **attr_group_influence)
            save_group_results(results)
    return results
'''

#test compute group task
#input: NULL
#output: 
def compute_group_task():
    results = dict()
    task = json.loads(TASK)
    task_name = task['task_name']
    uid_list = task['uid_list']
    submit_date = task['submit_date']  #submit_date = timestamp
    results['count'] = len(uid_list)
    #step1: get attr from es_user_portrait--basic/activity_geo/online_pattern/evaluate_index_his/preference/psycho_ratio
    #yes
    attr_in_portrait = get_attr_portrait(uid_list)
    results['task_name'] = task_name
    results['uid_list'] = uid_list
    results['submit_date'] = submit_date
    results['state'] = task['state']
    results = dict(results, **attr_in_portrait)
    #step2: get attr from social es----es_retweet&es_comment
    attr_in_social = get_attr_social(uid_list)
    results = dict(results, **attr_in_social)
    #step3: get attr activity trend and activity_time----redis for activity time
    #yes
    attr_weibo_trend = get_attr_trend(uid_list) # {'activity_trend':[], 'activity_time':{}}
    results = dict(results, **attr_weibo_trend)
    #step4: get evaluate index trend----copy_user_portrait
    evaluate_index_trend_dict = get_attr_evaluate_trend(uid_list) # {'importance_trend':[], 'influence_trend':[], 'importance_trend':[]}
    results = dict(results, **evaluate_index_trend_dict)
    #step5: get sentiment trend----flow_text_es
    sentiment_trend = get_attr_sentiment_trend(uid_list)
    results = dict(results, **sentiment_trend)
    #step6: get general evaluate index---activeness/influence/importance/tightness
    attr_user_bci, influence_dict = get_attr_bci(uid_list)
    results = dict(results, **attr_user_bci)
    attr_group_activeness = get_attr_activeness(json.loads(results['activity_trend']), results['total_weibo_number'], json.loads(results['activity_geo']))
    results = dict(results, **attr_group_activeness)
    attr_group_importance = get_attr_importance(json.loads(results['domain']), json.loads(results['topic']), results['count'], results['be_retweeted_out'], results['be_retweeted_count_out'])
    results = dict(results , **attr_group_importance)
    attr_group_tightness = get_attr_tightness(results['density'], results['retweet_weibo_count'], results['retweet_user_count'])
    results = dict(results, **attr_group_tightness)
    attr_group_influence = get_attr_influence(uid_list, influence_dict)
    results = dict(results, **attr_group_influence)
    #step7: update compute status to completed
    results['status'] = 1
    #step8: save results
    save_group_results(results)

    return results


if __name__=='__main__':
    #test
    input_data = {}
    input_data['task_name'] = u'媒体'
    
    input_data['uid_list'] = ['2803301701', '1292808363', '2656274875', '2062994093', '1663937380', \
                              '2651176564', '1999472465', '1855514017', '2127460165', '1887790981', '1639498782', \
                              '1402977920', '1414148492', '3114175427', '2105426467']
    '''
    input_data['uid_list'] = ['1182391231', '1759168351', '1670071920', '1689618340', '1494850741', \
                              '1582488432', '1708942053', '1647678107']
    input_data['task_name'] = u'商业人士'
    '''
    input_data['submit_date'] = '2013-09-08'
    input_data['state'] = u'关注的媒体'
    #input_data['state'] = u'关注的媒体'
    TASK = json.dumps(input_data)
    compute_group_task()
        
    #get_attr_portrait(input_data['uid_list'])
    #get_attr_trend(input_data['uid_list'])
    #get_attr_bci(input_data['uid_list'])
    #test retweet and beretweeted
    uid_list = ['1514608170', '2729648295', '3288875501', '1660612723', '1785934112',\
                '2397686502', '1748065927', '2699434042', '1886419032', '1830325932']
    #get_attr_social(uid_list)
    #get_attr_geo_track(uid_list)

