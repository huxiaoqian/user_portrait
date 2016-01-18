#-*- coding:utf-8 -*-
import os
import sys
import time

reload(sys)
sys.path.append('../../')
from global_utils import R_GROUP as r_group # save detect and analysis queue
from global_utils import group_detect_queue_name
from global_utils import es_user_portrait, portrait_index_name, portrait_index_type
from global_utils import es_flow_text, flow_text_index_name_pre, flow_text_index_type
from global_utils import es_retweet, retweet_index_name_pre, retweet_index_type,\
                         be_retweet_index_name_pre, be_retweet_index_type
from global_utils import es_comment, comment_index_name_pre, comment_index_type,\
                         be_comment_index_name_pre, be_comment_index_type
from global_utils import R_BEGIN_TIME
from parameter import DETECT_QUERY_ATTRIBUTE_MULTI, MAX_DETECT_COUNT, DAY,\
                      DETECT_COUNT_EXPAND
from time_utils import ts2datetime, datetime2ts


r_beigin_ts = datetime2ts(R_BEGIN_TIME)

#use to identify the task is exist
#input: task_name
#output: status True/False
def identify_task_exist(task_name):
    status = False
    try:
        task_exist_result = es_group_result.get(index=group_index_name, doc_type=group_index_type, id=task_name)['_source']
    except:
        task_exist_result = {}
    if task_exist_result != {}:
        status = True
    return status

#use to get single user portrait attribute
#input: seed_user_dict
#output: user_portriat_dict
def get_single_user_portrait(seed_user_dict):
    if 'uid' in seed_user_dict:
        uid = seed_user_dict['uid']
        try:
            user_portrait_result = es_user_portrait.get(index=portrait_index_name, doc_type=portrait_index_type, id=uid)['_source']
        except:
            user_portrait_result = {}
    else:
        uname = seed_user_dict['uname']
        query = {'term':{'uname': uname}}
        try:
            user_portrait_result = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type ,\
                      body={'query' query})['_source']
        except:
            user_portrait_result = {}

    return user_portrait_result


#use to get retweet/be_retweet/comment/be_comment db_number
#input: timestamp
#output: db_number
def get_db_num(timestamp):
    date = ts2datetime(timestamp)
    date_ts = datetime2ts(date)
    db_number = ((date_ts - r_beigin_ts) / (DAY*7)) % 2 + 1
    #test
    db_number = 1
    return db_number


#use to merge dict
#input: dict1, dict2, dict3...
#output: merge dict
def union_dict(*objs):
    _keys = set(sum([obj.keys() for obj in objs], []))
    _total = {}
    for _key in _keys:
        _total[_key] = sum([int(obj.get(_key, 0)) for obj in objs])
    
    return _total



#use to get structure user
#input: seed_uid_list
#output: in_portrait_result [uid1, uid2, uid3,...] ranked by iteraction count and meet the filter dict
def get_structure_user(seed_uid_list, structure_dict, filter_dict):
    structure_user_dict = {}
    retweet_mark = int(structure_dict['retweet'])
    comment_mark = int(structure_dict['comment'])
    hop = int(structure_dict['hop'])
    retweet_user_dict = {}
    comment_user_dict = {}
    #get retweet/comment es db_number
    now_ts = time.time()
    db_number = get_db_num(now_ts)
    #iter to find seed uid list retweet/be_retweet/comment/be_comment user set by hop
    iter_hop_user_list = seed_uid_list
    iter_count = 0
    all_union_result = dict()
    while iter_count < hop:   # hop number control
        iter_hop_count += 1
        search_user_count = len(iter_hop_user_list)
        hop_union_result = dict()
        while iter_search_count < search_user_count:
            iter_search_user_list = iter_hop_user_list[iter_search_count: iter_search_count + DETECT_ITER_COUNT]
            #step1: mget retweet and be_retweet
            if retweet_mark == 1:
                retweet_index_name = retweet_index_name_pre + str(db_number)
                be_retweet_index_name = be_retweet_index_name_pre + str(db_number)
                #mget retwet
                try:
                    retweet_result = es_retweet.mget(index=retweet_index_name, doc_type=retweet_index_type, \
                                                     body={'ids':iter_search_user_list}, _source=True)['docs']
                except:
                    retweet_result = []
                #mget be_retweet
                try:
                    be_retweet_result = es_retweet.mget(index=be_retweet_index_name, doc_type=be_retweet_type, \
                                                        body={'ids':iter_search_user_list, _source=True})['docs']
                except:
                    be_retweet_result = []
            #step2: mget comment and be_comment
            if comment_mark == '1':
                comment_index_name = comment_index_name_pre + str(db_number)
                be_comment_index_name = be_comment_index_name_pre + str(db_number)
                #mget comment
                try:
                    comment_result = es_comment.mget(index=comment_index_name, doc_type=comment_index_type, \
                                                     body={'ids':iter_search_user_list, _source=True})['docs']
                except:
                    comment_result = []
                #mget be_comment
                try:
                    be_comment_result = es_comment.mget(index=be_comment_index_name, doc_type=be_comment_index_type, \
                                                    body={'ids':iter_search_user_list, _source=True})['docs']
                except:
                    be_comment_result = []
            #step3: union retweet/be_retweet/comment/be_comment result
            union_count = 0
            
            for iter_search_uid in iter_search_user_list:
                try:
                    uid_retweet_dict = json.loads(retweet_result[union_count]['uid_retweet'])
                except:
                    uid_retweet_dict = {}
                try:
                    uid_be_retweet_dict = json.loads(be_retweet_result[union_count]['uid_be_retweet'])
                except:
                    uid_be_retweet_dict = {}
                try:
                    uid_comment_dict = json.loads(comment_result[union_count]['uid_comment'])
                except:
                    uid_comment_dict = {}
                try:
                    uid_be_comment_dict = json.loads(be_comment_result[union_count]['uid_be_comment'])
                except:
                    uid_be_comment_dict = {}
                #union four type user set
                union_result = union_dict(uid_retweet_dict, uid_be_retweet_dict, uid_comment_dict, uid_be_comment_dict)
                hop_union_result = union_dict(hop_union_result, union_result)
            #step4: add iter search count
            iter_search_count += DETECT_ITER_COUNT

        #pop seed uid self
        for iter_hop_user_item in iter_hop_user_list:
            hop_union_result.pop(iter_hop_user_item)
        #get new iter_hop_user_list
        iter_hop_user_list = hop_union_result.keys()
        #get all union result
        all_union_result = union_dict(all_union_result, hop_union_result)
    
    #step5: identify the who is in user_portrait
    sort_all_union_result = sorted(all_union_result.items(), key=lambda x:x[1], reverse=True)
    iter_count = 0
    all_count = len(sort_all_union_result)
    in_portrait_result = []
    filter_importance_from = filter_dict['importance']['from']
    filter_importance_to = filter_dict['importance']['to']
    filter_influence_from = filter_dict['influence']['from']
    filter_influence_to = filter_dict['influence']['to']
    while iter_count < all_count:
        iter_user_list = [item[0] for item in sort_all_union_result[iter_count:iter_count + DETECT_ITER_COUNT]]
        try:
            portrait_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type, \
                    body={'ids':iter_user_list}, _source=True)['docs']
        except:
            portrait_result = []
        for portrait_item in portrait_result:
            if portrait_item['found'] == True:
                if portrait_item['importance'] >= filter_importance_from and portrait_item['importance'] <= filter_importance_to:
                    if portrait_item['influence'] <= filter_influence_from and portrait_item['influence'] >= filter_influence_to:
                        uid = portrait_item['_id']
                        in_portrait_result.append(uid)
        if len(in_portrait_result) > (filter_dict['count'] * DETECT_COUNT_EXPAND)
            break

    return in_portrait_result


#use to union attribute result and structure result
#input:attribute_user_reslt [user_dict1, user_dict2,...] ranked by similarity
#input:structure result [uid1, uid2,....] ranked by interaction count
def union_attribute_structure(attribute_user_result, structure_result, attribute_weight, structure_weight):
    union_result = dict()
    #step1:trans structure result list to dict {uid1:rank1, uid2:rank2....}
    structure_user_result = dict()
    for item_rank in range(0, len(structrue_result)):
        uid = structure_result[item_rank]
        structure_user_result[uid] = item_rank
    #step2:use attribute weight and structure weight to score for user
    attribute_rank = 0
    attribute_normal_index = float(1) / len(attribute_user_result)
    structure_normal_index = float(1) / len(structure_user_result)
    attribute_count = len(attribute_user_result)
    structure_count = len(structure_count)
    for attribute_item in attribute_user_result:
        uid = attribute_item['_id']
        structure_rank = structure_user_result[uid]
        new_score = attribute_weight*((attribute_count - attribute_rank)*attribute_normal_index) + \
                    structure_weight*((structure_count - structure_rank)*structure_normal_index)
        union_result[uid] = new_score
    #step3:sort user by new score
    sort_union_result = sorted(union_result.items(), key=lambda x:x[1], reverse=True)

    return sort_union_result

#use to filter event for single or multi detect task
#input: all_union_user, event_condition_dict
#output: user_list (who meet the filter condition)
def filter_event(all_union_user, event_condition_list):
    user_result = []
    new_event_condition_list = []
    #step1: adjust the date condition for date
    for event_condition_item in event_condition_dict:
        if 'range' in event_condition_item:
            range_dict = event_condition_item['range']
            from_ts = range_dict['from']
            to_ts = range_dict['to']
            from_date_ts = datetime2ts(ts2datetime(from_ts))
            to_date_ts = datetime2ts(ts2datetime(to_ts))
            new_range_dict_list = []
            if from_date_ts != to_date_ts:
                iter_date_ts = from_date_ts
                while iter_date_ts <= to_date_ts:
                    iter_next_date_ts = iter_date_ts + DAY
                    new_range_dict_list.append('range':{'timestamp':{'from':iter_date_ts, 'to':iter_next_date_ts}})
                    iter_date_ts = iter_next_date_ts
            else:
                new_range_dict_list = [{'range':{}}]
    #step2: iter to search user who publish weibo use keywords_string
    return user_result


#use to detect group by single-person
#input: input_dict
#output: status True/False
def single_detect(input_dict):
    results = {}
    task_information_dict = input_dict['task_information']
    task_name = task_information_dict['task_name']
    task_exist_mark = identify_task_exist(task_name)
    seed_user_dict = input_dict['seed_user']
    query_condition_dict = input_dict['query_condition']
    filter_dict = input_dict['filter']
    structure_dict = input_dict['structure_dict']
    #step1: get seed user portrait result
    user_portrait = get_single_user_portrait(seed_user_dict)
    seed_uid = user_portrait['uid']
    #step2: search attribute user set
    #step2.1: get attribute query dict
    attribute_item = query_condition_dict['attribute']
    attribute_query_list = []
    for query_item in attribute_item:
        try:
            user_attribute_value = user_portrait[query_item]
        except:
            user_attribute_value = ''
        if user_attribute_value != '':
            if user_attribute_value in DETECT_QUERY_ATTRIBUTE_MULTI:
                nest_body_list = []
                user_attribute_value_list = user_attribute_value.split('&')
                for attribute_value_item in user_attribute_value_list:
                    nest_body_list.append({'wildcard': {query_item: '*'+attribute_value_item+'*'}})
                attribute_query_list.append({'bool':{'should': nest_body_list}})
            else:
                attribute_query_list.append({'wildcard': {query_item: '*'+attribute_value+'*'}})
    #step2.2: add filter query condition
    count = MAX_DETECT_COUNT
    for filter_item in filter_dict:
        if filter_item == 'count':
            count = filter_dict[filter_item] * DETECT_COUNT_EXPAND
        else:
            filter_value_from = filter_dict[filter_item]['from']
            filter_value_to = filter_dict[filter_item]['to']
            attribute_query_list.append({'range':{filter_item: {'from': filter_value_from, 'to':filter_value_to}}})
    
    attribute_user_result = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type, \
            body={'query':{'bool':{'must':attribute_query_list}}, 'size': count})['hits']['hits']

    #step3: search structure user set
    structure_user_result = get_structure_user([seed_uid], structure_dict, filter_dict)
    #step4: union attribtue and structure user set
    attribute_weight = query_condition_dict['attribute_weight']
    structure_weight = query_condition_dict['structure_weight']
    all_union_user = union_attribtue_structure(attribute_user_result, structure_user_result)
    #step5: filter user by event
    event_condition_list = query_condition['text']
    filter_user_list = filter_event(all_union_user, event_condition_list)
    #step6: filter by count
    return results

#use to detect group by multi-person
#input: {}
#output: {}
def multi_detect():
    results = {}
    #step1: get seed users attribute
    #step2: search attribute user set
    #step3: search structure user set
    #step4: union search and structure user set
    #step5: filter user by event
    #step6: filter by count and evaluation index
    return results

#use to detect group by attribute or pattern
#input: {}
#output: {}
def attribute_pattern_detect():
    results = {}
    #step1: search text user set(who is in user_portrait)
    #step2: search attribute user
    #step3: filter by count and evaluation index
    return results

#use to detect group by event
#input: {}
#output: {}
def event_detect():
    results = {}
    #step1: search text user set
    #step2: filter user by domain or topic
    #step3: filter by count and evaluation index
    return results

#use to save detect results to es
#input: uid list (detect results)
#output: status (True/False)
def save_detect_results(detect_results):
    mark = False
    try:
        task_exist_result = es_group_result.get(index=group_index_name, doc_type=group_index_type, id=task_name)['_source']
    except:
        task_exist_result = {}
    if task_exist_result != {}:
        task_exist_result['uid_list'] = json.dumps(detect_results)
        es_group_result.index(index=group_index_name, doc_type=group_index_type, id=task_name, body=task_exist_result)
        mark = True

    return mark

#use to change detect task process proportion
#input: task_name, proportion
#output: status (True/False)
def change_process_proportion(task_name, proportion):
    mark = False
    try:
        task_exist_result = es_group_result.get(index=group_index_name, doc_type=group_index_type, id=task_name)['_source']
    except:
        task_exist_result = {}
        print 'task is not exist'
    if task_exist_result != {}:
        task_exist_result['process'] = proportion
        es_group_result.index(index=group_index_name, doc_type=group_index_type, id=task_name, body=task_exist_result)
        mark = True

    return mark


#use to add task to redis queue when the task  detect process fail
#input: input_dict
#output: status
def add_task2queue(input_dict):
    status = True
    try:
        r_group.lpush(group_detect_queue_name, json.dumps(input_dict))
    except:
        status = False

    return status


#use to get detect information from redis queue
#input: NULL
#output: task_information_dict (from redis queue---gruop_detect_task)
def get_detect_information():
    task_information_dict = {}
    task_information_string = r_group.rpop(group_detect_queue_name)
    if task_information_string:
        task_information_dict = json.loads(task_information_string)
    else:
        task_information_dict = {}

    return task_information_dict

#main function to group detect
def compute_group_detect():
    results = {}
    while True:
        #step1:read detect task information from redis queue
        detect_task_information = get_detect_information()
        if detect_task_information != {}:
            start_ts = time.time()
            task_information_dict = detect_task_information['task_information']
            task_name = task_information_dict['task_name']
            #step2:according task type to do group detect
            detect_task_type = task_information_dict['detect_type']
            if detect_task_type == 'single':
                detect_results = single_detect(detect_task_information)
            elif detect_task_type == 'multi':
                detect_results == multi_detect(detect_task_information)
            elif detect_task_type == 'attribute':
                detect_results =  attribute_pattern_detect(detect_task_information)
            elif detect_task_type == 'event':
                detect_results = event_detect(detect_task_information)
            #step3:save detect results to es (status=1 and process=100 and add uid_list)
            mark = save_detect_results(detect_results)
            #step4:add task_information_dict to redis queue when detect process fail
            if mark == False:
                status = add_task2queue(detect_task_information)
            else:
                end_ts = time.time()
                print 'success detect task:' + task_name
                print 'time cost %s sec' % (end_ts - start_ts)


if __name__=='__main__':
    compute_group_detect()
