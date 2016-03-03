# -*- coding: UTF-8 -*-
import sys
import time
import json
import math
from mid2weibolink import weiboinfo2url
from user_portrait.global_config import UPLOAD_FOLDER
from user_portrait.global_utils import R_GROUP as r
from user_portrait.global_utils import es_user_portrait as es
from user_portrait.global_utils import es_user_portrait, portrait_index_name, portrait_index_type,\
                        es_flow_text, flow_text_index_name_pre, flow_text_index_type,\
                        es_user_profile, profile_index_name, profile_index_type,\
                        es_group_result, group_index_name, group_index_type
from user_portrait.time_utils import ts2datetime, datetime2ts, ts2date
from user_portrait.parameter import MAX_VALUE, DAY, FOUR_HOUR, SENTIMENT_SECOND
from user_portrait.global_utils import group_analysis_queue_name
from user_portrait.parameter import RUN_TYPE, RUN_TEST_TIME

index_name = group_index_name
index_type = group_index_type

'''
#submit new task and identify the task name unique
def submit_task(input_data):
    status = 0
    result = r.lrange('group_task', 0, -1)
    #print 'result:',result
    for task in result:
        task_dict = json.loads(task)
        task_name = task['task_name']
        if input_data==task_name:
            status += 1
    result = es.get(index=index_name, doc_type=index_type, id=task_name)
    try:
        task_exist = result['_source']
    except:
        status += 1
    if status != 0:
        return False
    else:
        r.lpush('group_task', json.dumps(input_data))
    return True
'''

# read uid list from upload file
def read_uid_file(filename):
    uid_list = []
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    f = open(filepath+'.txt', 'r')
    for line in f:
        if len(line)==10:
            uid_list.append(line)
    return uid_list

# delete uid list after save to redis and es
def delete_uid_file(filename):
    status = 0
    filename += '.txt'
    filenames = os.listdir(UPLOAD_FOLDER)
    if filename in filenames:
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        os.remove(filepath)
    else:
        print 'there no this file'
    return status


#submit new task and identify the task name unique in es-group_result and save it to redis list
def submit_task(input_data):
    status = 0 # mark it can not submit
    task_name = input_data['task_name']
    try:
        result = es_group_result.get(index=group_index_name, doc_type=group_index_type, id=task_name)['_source']
    except:
        status = 1
    
    if status != 0 and 'uid_file' not in input_data:
        input_data['status'] = 0 # mark the task not compute
        count = len(input_data['uid_list'])
        input_data['count'] = count
        input_data['task_type'] = 'analysis'
        input_data['submit_user'] = 'admin'
        input_data['detect_type'] = ''
        input_data['detect_process'] = ''
        add_es_dict = {'task_information': input_data, 'query_condition':''}
        es_group_result.index(index=group_index_name, doc_type=group_index_type, id=task_name, body=input_data)
        r.lpush(group_analysis_queue_name, json.dumps(input_data))
    
    return status



#search task by some condition -whether add download
def search_task(task_name, submit_date, state, status):
    results = []
    query = []
    condition_num = 0
    if task_name:
        task_name_list = task_name.split(' ')
        for item in task_name_list:
            query.append({'wildcard':{'task_name': '*' + item + '*'}})
            condition_num += 1
    if submit_date:
        submit_date_ts = datetime2ts(submit_date)
        submit_date_start = submit_date_ts
        submit_date_end = submit_date_ts + DAY
        query.append({'range':{'submit_date': {'gte': submit_date_start, 'lt': submit_date_end}}})
        condition_num += 1
    if state:
        state_list = state.split(' ')
        for item in state_list:
            query.append({'wildcard':{'state': '*' + item + '*'}})
            condition_num += 1
    if status:
        query.append({'match':{'status': status}})
        condition_num += 1
    if condition_num > 0:
        query.append({'term':{'task_type': 'analysis'}})
        try:
            source = es_group_result.search(
                    index = group_index_name,
                    doc_type = group_index_type,
                    body = {
                        'query':{
                            'bool':{
                                'must':query
                                }
                            },
                        'sort': [{'count':{'order': 'desc'}}],
                        'size': MAX_VALUE
                        }
                    )
        except Exception as e:
            raise e
    else:
        query.append({'term':{'task_type': 'analysis'}})
        source = es.search(
                index = group_index_name,
                doc_type = group_index_type,
                body = {
                    'query':{'bool':{
                        'must':query
                        }
                        },
                    'sort': [{'count': {'order': 'desc'}}],
                    'size': MAX_VALUE
                    }
                )

    try:
        task_dict_list = source['hits']['hits']
    except:
        return None
    print 'step yes'
    result = []
    for task_dict in task_dict_list:
        try:
            state = task_dict['_source']['state']
        except:
            state = ''
        try:
            status = task_dict['_source']['status']
        except:
            status = 0
        result.append([task_dict['_source']['task_name'], task_dict['_source']['submit_date'], task_dict['_source']['count'], state, status])
    
    return result


#search group analysis result
#input: task_name, module
#output: module_result
def search_group_results(task_name, module):
    result = {}
    #step1:identify the task_name exist
    try:
        source = es_group_result.get(index=group_index_name, doc_type=group_index_type, \
                id=task_name)['_source']
    except:
        return 'group task is not exist'
    #step2: identify the task status=1(analysis completed)
    status = source['status']
    if status != 1:
        return 'group task is not completed'
    #step3:get module result
    if module == 'overview':
        result['task_name'] = source['task_name']
        result['submit_date'] = ts2datetime(source['submit_date'])
        result['state'] = source['state']
        result['submit_user'] = source['submit_user']
        result['density_star'] = source['density_star']
        result['activeness_star'] = source['activeness_star']
        result['influence_star'] = source['influence_star']
        result['importance_star'] = source['importance_star']
        result['tag_vector'] = json.loads(source['tag_vector'])
    elif module == 'basic':
        result['gender'] = json.loads(source['gender'])
        result['verified'] = json.loads(source['verified'])
        result['user_tag'] = json.loads(source['user_tag'])
        result['count'] = source['count']
    elif module == 'activity':
        result['activity_trend'] = json.loads(source['activity_trend'])
        result['activity_time'] = json.loads(source['activity_time'])
        result['activity_geo_disribution'] = json.loads(source['activity_geo_distribution'])
        result['activiy_geo_vary'] = json.loads(source['activity_geo_vary'])
        result['activeness_trend'] = json.loads(source['activeness'])
        result['activeness_his'] = json.loads(source['activeness_his'])
        result['activeness_description'] = source['activeness_description']
        result['online_pattern'] = json.loads(source['online_pattern'])
    elif module == 'preference':
        result['keywords'] = json.loads(source['keywords'])
        result['hashtag'] = json.loads(source['hashtag'])
        result['sentiment_word'] = json.loads(source['sentiment_word'])
        result['domain'] = json.loads(source['domain'])
        result['topic'] = json.loads(source['topic'])
    elif module == 'influence':
        result['influence_his'] = json.loads(source['influence_his'])
        result['influence_trend'] = json.loads(source['influence'])
        result['influence_in_user'] = json.loads(source['influence_in_user'])
        result['influence_out_user'] = json.loads(source['influence_out_user'])
    elif module == 'social':
        result['in_density'] = source['in_density']
        result['in_inter_user_ratio'] = source['in_inter_user_ratio']
        result['in_inter_weibo_ratio'] = source['in_inter_weibo_ratio']
        result['social_in_record'] = json.loads(source['social_in_record'])
        result['out_inter_user_ratio'] = source['out_inter_user_ratio']
        result['out_inter_weibo_ratio'] = source['out_inter_weibo_ratio']
        result['social_out_record'] = json.loads(source['social_out_record'])
        result['density_description'] = source['density_description']
        result['mention'] = source['mention']
    elif module == 'think':
        result['sentiment_trend'] = json.loads(source['sentiment_trend'])
        result['sentiment_pie'] = json.loads(source['sentiment_pie'])
        result['character'] = json.loads(source['character'])
    return result


#abandon
'''
#show group results
def get_group_results(task_name, module):
    result = []
    try:
        es_result = es.get(index=index_name, doc_type=index_type, id=task_name)['_source']
        #print 'result:', result
    except:
        return None
    #basic module: gender, count, verified
    if module=='overview':
        task_name = es_result['task_name']
        submit_date = es_result['submit_date']
        state = es_result['state']
        tightness = es_result['tightness']
        activeness = es_result['activeness']
        importance = es_result['importance']
        influence = es_result['influence']
        result = [task_name, submit_date, state, tightness, activeness, importance, influence]
    if module=='basic':
        gender_dict = json.loads(es_result['gender'])
        count = es_result['count']
        verified = es_result['verified']
        if verified:
            verified_dict = json.loads(verified)
        result = [gender_dict, count, verified]
    if module=='activity':
        activity_geo_dict = json.loads(es_result['activity_geo'])
        sort_activity_geo = sorted(activity_geo_dict.items(), key=lambda x:x[1], reverse=True)
        activity_geo = sort_activity_geo[:50]
        activity_trend = json.loads(es_result['activity_trend'])
        online_pattern_dict = json.loads(es_result['online_pattern'])
        sort_online_pattern = sorted(online_pattern_dict.items(), key=lambda x:x[1], reverse=True)
        online_pattern = sort_online_pattern[:50]
        geo_track = json.loads(es_result['geo_track'])
        result = [activity_geo, activity_trend, online_pattern, geo_track]
    if module=='social':
        #degree_his = json.loads(es_result['degree_his'])
        density = es_result['density']
        retweet_weibo_count = es_result['retweet_weibo_count']
        retweet_user_count = es_result['retweet_user_count']
        retweet_relation = json.loads(es_result['retweet_relation'])
        uid_list = []
        for relation in retweet_relation:
            uid_list.append(relation[0])
            uid_list.append(relation[1])
        es_portrait_result = es.mget(index='user_portrait', doc_type='user', body={'ids':uid_list})['docs']
        es_count = 0
        new_retweet_relation = []
        for relation in retweet_relation:
            source_uid = relation[0]
            source_item = es_portrait_result[es_count]
            try:
                source = source_item['_source']
                source_uname = source['uname']
            except:
                source_uname = ''
            target_uid = relation[1]
            es_count += 1
            target_item = es_portrait_result[es_count]
            try:
                source = target_item['_source']
                target_uname = source['uname']
            except:
                target_uname = ''

            count = relation[2]
            new_retweet_relation.append([source_uid, source_uname, target_uid, target_uname, count])
        uid_list = []
        out_beretweet_relation = json.loads(es_result['out_beretweet_relation'])
        uid_list = []
        uid_list = [item[0] for item in out_beretweet_relation]
        es_portrait_result = es.mget(index='user_portrait', doc_type='user', body={'ids':uid_list})['docs']
        es_count = 0
        new_out_beretweet_relation = []
        for i in range(len(uid_list)):
            item = es_portrait_result[i]
            uid = item['_id']
            try:
                source = item['_source']
                uname = source['uname']
            except:
                uname = ''
            out_relation_item = out_beretweet_relation[i][1:]
            a = [uid, uname]
            a.extend(out_relation_item)
            #print 'add_item:', add_item
            new_out_beretweet_relation.append(a)
        result = [new_retweet_relation, density, retweet_weibo_count, retweet_user_count, new_out_beretweet_relation]
    if module=='think':
        domain_dict = json.loads(es_result['domain'])
        topic_dict = json.loads(es_result['topic'])
        psycho_status = json.loads(es_result['psycho_status'])
        psycho_feature = json.loads(es_result['psycho_feature'])
        result = [domain_dict, topic_dict, psycho_status, psycho_feature]
    if module=='text':
        hashtag_dict = json.loads(es_result['hashtag'])
        sort_hashtag = sorted(hashtag_dict.items(), key=lambda x:x[1], reverse=True)
        hashtag = sort_hashtag[:50]
        emoticon_dict = json.loads(es_result['emoticon'])
        sort_emoticon = sorted(emoticon_dict.items(), key=lambda x:x[1], reverse=True)
        emoticon = sort_emoticon[:5]
        keyword_dict = json.loads(es_result['keywords'])
        sort_keyword = sorted(keyword_dict.items(), key=lambda x:x[1], reverse=True)
        keyword = sort_keyword[:50]
        result = [hashtag, keyword, emoticon]
    if module=='influence':
        importance_dis = json.loads(es_result['importance_his'])
        activeness_his = json.loads(es_result['activeness_his'])
        influence_his = json.loads(es_result['influence_his'])
        user_influence_list = json.loads(es_result['user_influence_list'])
        user_influence_result = []
        for user_item in user_influence_list:
            uid = user_item[0]
            result_item = user_item[:5]
            for i in range(5,9):
                item = user_item[i]
                mid = item[1]
                number = item[0]
                if mid != 0 and uid:
                    weibolink = weiboinfo2url(uid, mid)
                else:
                    weibolink = None
                result_item.append((number, mid, weibolink))
            user_influence_result.append(result_item)
        
        result = [importance_dis, activeness_his, influence_his, user_influence_result]
    #print result
    return result
'''

# get importance max & activeness max & influence max
def get_evaluate_max():
    max_result = {}
    evaluate_index = ['importance', 'influence']
    for evaluate in evaluate_index:
        query_body = {
            'query':{
                'match_all':{}
                },
            'size': 1,
            'sort': [{evaluate: {'order': 'desc'}}]
            }
        try:
            result = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)['hits']['hits']
        except Exception, e:
            raise e
        max_evaluate = result[0]['_source'][evaluate]
        max_result[evaluate] = max_evaluate
    return max_result

# get grouop user list
def get_group_list(task_name):
    results = []
    try:
        es_results = es_group_result.get(index=group_index_name, doc_type=group_index_type, id=task_name)['_source']
    except:
        return results
    uid_list = es_results['uid_list']
    user_portrait_attribute = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type, body={'ids':uid_list})['docs']
    evaluate_max = get_evaluate_max()
    for item in user_portrait_attribute:
        uid = item['_id']
        try:
            source = item['_source']
            uname = source['uname']
            gender = source['gender']
            location = source['location']
            importance = source['importance']
            normal_importance = math.log(importance / evaluate_max['importance'] * 9 + 1, 10) * 100
            influence = source['influence']
            normal_influence = math.log(influence / evaluate_max['influence'] * 9 + 1, 10) * 100
            results.append([uid, uname, gender, location, normal_importance, normal_influence])
        except:
            results.append([uid, '', '', '', '', ''])
    return results

#use to get group member uid_uname
#version: write in 2016-02-26
#input: task_name
#output: uid_uname dict
def get_group_member_name(task_name):
    results = {}
    try:
        group_result = es_group_result.get(index=group_index_name, doc_type=group_index_type,\
                id=task_name)['_source']
    except:
        return results
    uid_list = group_result['uid_list']
    try:
        user_portrait_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type ,\
                body={'ids':uid_list})['docs']
    except:
        return results
    for item in user_portrait_result:
        uid = item['_id']
        if item['found'] == True:
            source = item['_source']
            uname = source['uname']
        else:
            uname = 'unkown'
        results[uid] = uname

    return results



# delete group results from es_user_portrait 'group_analysis'
def delete_group_results(task_name):
    try:
        result = es.delete(index=index_name, doc_type=index_type, id=task_name)
    except:
        return False
    return True


#show group user geo track
#input: uid
#output: results [geo1,geo2,..]
def get_group_user_track(uid):
    results = []
    #step1:get user_portrait activity_geo_dict
    try:
        portrait_result = es_user_portrait.get(index=portrait_index_name, doc_type=portrait_index_type,\
                id=uid, _source=False, fields=['activity_geo_dict'])
    except:
        portrait_result = {}
    if portrait_result == {}:
        return 'uid is not in user_portrait'
    activity_geo_dict = json.loads(portrait_result['fields']['activity_geo_dict'][0])
    now_date_ts = datetime2ts(ts2datetime(int(time.time())))
    start_ts = now_date_ts - DAY * len(activity_geo_dict)
    #step2: iter date to get month track
    for geo_item in activity_geo_dict:
        iter_date = ts2datetime(start_ts)
        sort_day_dict = sorted(geo_item.items(), key=lambda x:x[1], reverse=True)
        if sort_day_dict:
            results.append([iter_date, sort_day_dict[0][0]])
        else:
            results.append([iter_date, ''])
        start_ts = start_ts + DAY

    return results



# show group members weibo for activity ---week
# input: task_name, start_ts
# output: weibo_list
def get_activity_weibo(task_name, start_ts):
    results = []
    #step1: get task_name uid
    try:
        group_result = es_group_result.get(index=group_index_name, doc_type=group_index_type ,\
                id=task_name, _source=False, fields=['uid_list'])
    except:
        group_result = {}
    if group_result == {}:
        return 'task name invalid'
    try:
        uid_list = group_result['fields']['uid_list']
    except:
        uid_list = []
    if uid_list == []:
        return 'task uid list null'
    #step2: get uid2uname
    uid2uname = {}
    try:
        user_portrait_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type, \
                body = {'ids':uid_list}, _source=False, fields=['uname'])['docs']
    except:
        user_portrait_result = []
    for item in user_portrait_result:
        uid = item['_id']
        if item['found']==True:
            uname = item['fields']['uname'][0]
        uid2uname[uid] = uname
    #step3: search time_segment weibo
    time_segment = FOUR_HOUR
    end_ts = start_ts + time_segment
    time_date = ts2datetime(start_ts)
    flow_text_index_name = flow_text_index_name_pre + time_date
    query = []
    query.append({'terms':{'uid': uid_list}})
    query.append({'range':{'timestamp':{'gte':start_ts, 'lt':end_ts}}})
    try:
        flow_text_es_result = es_flow_text.search(index=flow_text_index_name, doc_type=flow_text_index_type, \
                body={'query':{'bool':{'must':query}}, 'sort':'timestamp', 'size':MAX_VALUE})['hits']['hits']
    except:
        flow_text_es_result = []
    for item in flow_text_es_result:
        weibo = {}
        source = item['_source']
        weibo['timestamp'] = ts2date(source['timestamp'])
        weibo['ip'] = source['ip']
        weibo['text'] = source['text']
        weibo['geo'] = '\t'.join(source['geo'])
        results.append(weibo)

    return results

#show group members weibo for influence content
#input: uid, timestamp_from, timestamp_to
#output: weibo_list
def get_influence_content(uid, timestamp_from, timestamp_to):
    weibo_list = []
    #split timestamp range to new_range_dict_list
    from_date_ts = datetime2ts(ts2datetime(timestamp_from))
    to_date_ts = datetime2ts(ts2datetime(timestamp_to))
    new_range_dict_list = []
    if from_date_ts != to_date_ts:
        iter_date_ts = from_date_ts
        while iter_date_ts < to_date_ts:
            iter_next_date_ts = iter_date_ts + DAY
            new_range_dict_list.append({'range':{'timestamp':{'gte':iter_date_ts, 'lt':iter_next_date_ts}}})
            iter_date_ts = iter_next_date_ts
        if new_range_dict_list[0]['range']['timestamp']['gte'] < timestamp_from:
            new_range_dict_list[0]['range']['timestamp']['gte'] = timestamp_from
        if new_range_dict_list[-1]['range']['timestamp']['lt'] > timestamp_to:
            new_range_dict_list[-1]['range']['timestamp']['lt'] = timestamp_to
    else:
        new_range_dict_list = [{'range':{'timestamp':{'gte':timestamp_from, 'lt':timestamp_to}}}]
    #iter date to search flow_text
    iter_result = []
    for range_item in new_range_dict_list:
        range_from_ts = range_item['range']['timestamp']['gte']
        range_from_date = ts2datetime(range_from_ts)
        flow_text_index_name = flow_text_index_name_pre + range_from_date
        query = []
        query.append({'term':{'uid':uid}})
        query.append(range_item)
        try:
            flow_text_exist = es_flow_text.search(index=flow_text_index_name, doc_type=flow_text_index_type,\
                    body={'query':{'bool':{'must': query}}, 'sort':[{'timestamp':'asc'}]})['hits']['hits']
        except:
            flow_text_exist = []
        iter_result.extend(flow_text_exist)
    # get weibo list
    for item in flow_text_exist:
        source = item['_source']
        weibo = {}
        weibo['timestamp'] = ts2date(source['timestamp'])
        weibo['ip'] = source['ip']
        weibo['text'] = source['text']
        weibo['geo'] = '\t'.join(source['geo'].split('&'))
        weibo_list.append(weibo)
        
    return weibo_list

#show group members interaction weibo content
#input: uid1, uid2
#ouput: weibo_list
def get_social_inter_content(uid1, uid2, type_mark):
    weibo_list = []
    #get two type relation about uid1 and uid2
    #search weibo list
    now_ts = int(time.time())
    #run_type
    if RUN_TYPE == 1:
        now_date_ts = datetime2ts(ts2datetime(now_ts))
    else:
        now_date_ts = datetime2ts(RUN_TEST_TIME)
    #uid2uname
    uid2uname = {}
    try:
        portrait_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type ,\
                                body={'ids': [uid1, uid2]}, _source=False, fields=['uid', 'uname'])['docs']
    except:
        portrait_result = []
    
    for item in portrait_result:
        uid = item['_id']
        if item['found'] == True:
            uname = item['fields']['uname'][0]
            uid2uname[uid] = uname
        else:
            uid2uname[uid] = 'unknown'
    #iter date to search weibo list
    for i in range(7, 0, -1):
        iter_date_ts = now_date_ts - i*DAY
        iter_date = ts2datetime(iter_date_ts)
        flow_text_index_name = flow_text_index_name_pre + str(iter_date)
        query = []
        query.append({'bool':{'must':[{'term':{'uid':uid1}}, {'term':{'directed_uid': int(uid2)}}]}})
        if type_mark=='out':
            query.append({'bool':{'must':[{'term':{'uid':uid2}}, {'term':{'directed_uid': int(uid1)}}]}})
        try:
            flow_text_result = es_flow_text.search(index=flow_text_index_name, doc_type=flow_text_index_type,\
                    body={'query': {'bool':{'should': query}}, 'sort':[{'timestamp':{'order': 'asc'}}], 'size':MAX_VALUE})['hits']['hits']
        except:
            flow_text_result = []
        for flow_text in flow_text_result:
            source = flow_text['_source']
            weibo = {}
            weibo['timestamp'] = source['timestamp']
            weibo['ip'] = source['ip']
            weibo['geo'] = source['geo']
            weibo['text'] = '\t'.join(source['text'].split('&'))
            weibo['uid'] =  source['uid']
            weibo['uname'] = uid2uname[weibo['uid']]
            weibo['directed_uid'] = str(source['directed_uid'])
            weibo['directed_uname'] = uid2uname[str(source['directed_uid'])]
            weibo_list.append(weibo)

    return weibo_list

#show group members sentiment weibo
#input: task_name, start_ts ,sentiment_type
#output: weibo_list
def search_group_sentiment_weibo(task_name, start_ts, sentiment):
    weibo_list = []
    #step1:get task_name uid
    try:
        group_result = es_group_result.get(index=group_index_name, doc_type=group_index_type,\
                        id=task_name, _source=False, fields=['uid_list'])
    except:
        group_result = {}
    if group_result == {}:
        return 'task name invalid'
    try:
        uid_list = group_result['fields']['uid_list']
    except:
        uid_list = []
    if uid_list == []:
        return 'task uid list null'
    #step3: get ui2uname
    uid2uname = {}
    try:
        user_portrait_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type,\
                        body={'ids':uid_list}, _source=False, fields=['uname'])['docs']
    except:
        user_portrait_result = []
    for item in user_portrait_result:
        uid = item['_id']
        if item['found']==True:
            uname = item['fields']['uname'][0]
            uid2uname[uid] = uname
    #step4:iter date to search weibo
    weibo_list = []
    iter_date = ts2datetime(start_ts)
    flow_text_index_name = flow_text_index_name_pre + str(iter_date)
    #step4: get query_body
    if sentiment != '2':
        query_body = [{'terms': {'uid': uid_list}}, {'term':{'sentiment': sentiment}}, \
                {'range':{'timestamp':{'gte':start_ts, 'lt': start_ts+DAY}}}]
    else:
        query_body = [{'terms':{'uid':uid_list}}, {'terms':{'sentiment': SENTIMENT_SECOND}},\
                {'range':{'timestamp':{'gte':start_ts, 'lt':start_ts+DAY}}}]
    try:
        flow_text_result = es_flow_text.search(index=flow_text_index_name, doc_type=flow_text_index_type,\
                body={'query':{'bool':{'must': query_body}}, 'sort': [{'timestamp':{'order':'asc'}}], 'size': MAX_VALUE})['hits']['hits']
    except:
        flow_text_result = []
    for flow_text_item in flow_text_result:
        source = flow_text_item['_source']
        weibo = {}
        weibo['uid'] = source['uid']
        weibo['uname'] = uid2uname[weibo['uid']]
        weibo['ip'] = source['ip']
        try:
            weibo['geo'] = '\t'.join(source['geo'].split('&'))
        except:
            weibo['geo'] = ''
        weibo['text'] = source['text']
        weibo['timestamp'] = source['timestamp']
        weibo['sentiment'] = source['sentiment']
        weibo_list.append(weibo)

    return weibo_list


if __name__=='__main__':
    #test group task
    input_data = {}
    input_data['task_name'] = 'testtesttest'
    input_data['uid_list'] = json.dumps(['2010832710', '3482838791', '3697357313', '2496434537',\
                '1642591402', '2074370833', '1640601392', '1773489534',\
                '2722498861', '2803301701'])
    input_data['submit_date'] = '2013-09-08'
    input_data['state'] = 'it is a test'
    submit_task(input_data)
    test_task_name = 'testtesttest'
    #status = delete_group_results(test_task_name)
    #print 'status:', status
