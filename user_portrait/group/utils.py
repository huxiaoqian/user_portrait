# -*- coding: UTF-8 -*-
import sys
import time
import json
import math
from mid2weibolink import weiboinfo2url
#test
'''
reload(sys)
sys.path.append('../')
from global_utils import R_GROUP as r
from global_utils import es_user_portrait as es
from time_utils import ts2datetime, datetime2ts
'''
from user_portrait.global_config import UPLOAD_FOLDER
from user_portrait.global_utils import R_GROUP as r
from user_portrait.global_utils import es_user_portrait as es
from user_portrait.time_utils import ts2datetime, datetime2ts


index_name = 'group_result'
index_type = 'group'

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
        result = es.get(index=index_name, doc_type=index_type, id=task_name)
    except:
        status = 1
    
    if status != 0 and 'uid_file' not in input_data:
        r.lpush('group_task', json.dumps(input_data))
        input_data['status'] = 0 # mark the task not compute
        count = len(input_data['uid_list'])
        input_data['count'] = count
        uid_list_string = json.dumps(input_data['uid_list'])
        es.index(index='group_result', doc_type='group', id=task_name, body=input_data)
    elif status != 0 and 'uid_file' in input_data:
        input_data['status'] = 0 # mark the task not compute
        uid_file = input_data['uid_file']
        uid_list = read_uid_file(uid_file)
        input_data['count'] = len(uid_list)
        input_data['uid_list'] = json.dumps(uid_list)
        r.lpush('group_task', json.dumps(input_data))
        es.index(index='group_result', doc_type='group', id=task_name, body=input_data)
        delete_status = delete_uid_file(uid_file)
        if delete_status == 0:
            print 'fail delete uid file'
        elif delete_status == 1:
            print 'success delete uid file'
    return status



#search task by some condition -whether add download
def search_task(task_name, submit_date, state, status):
    results = []
    query = []
    condition_num = 0
    if task_name:
        task_name_list = task_name.split(' ')
        for item in task_name_list:
            #print 'item:', item
            query.append({'wildcard':{'task_name': '*' + item + '*'}})
            condition_num += 1
    if submit_date:
        query.append({'match':{'submit_date': submit_date}})
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
        try:
            source = es.search(
                    index = 'group_result',
                    doc_type = 'group',
                    body = {
                        'query':{
                            'bool':{
                                'must':query
                                }
                            },
                        'sort': [{'count':{'order': 'desc'}}],
                        'size': 10000
                        }
                    )
        except Exception as e:
            raise e
    else:
        source = es.search(
                index = 'group_result',
                doc_type = 'group',
                body = {
                    'query':{'match_all':{}
                        },
                    'sort': [{'count': {'order': 'desc'}}],
                    'size': 10000
                    }
                )

    try:
        task_dict_list = source['hits']['hits']
    except:
        return None
    result = []
    #print 'len task_dict_list:', len(task_dict_list)
    for task_dict in task_dict_list:
        result.append([task_dict['_source']['task_name'], task_dict['_source']['submit_date'], task_dict['_source']['count'], task_dict['_source']['state'], task_dict['_source']['status']])
    
    return result

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
        '''
        origin_max_retweeted_number =es_result['origin_max_retweeted_number']
        origin_max_retweeted_id = es_result['origin_max_retweeted_id']
        origin_max_retweeted_user = es_result['origin_max_retweeted_user']
        if origin_max_retweeted_id != 0 and origin_max_retweeted_user != 0:
            origin_max_retweeted_weibolink = weiboinfo2url(origin_max_retweeted_user, origin_max_retweeted_id)
        else:
            origin_max_retweeted_weibolink = None

        origin_max_comment_number = es_result['origin_max_comment_number']
        origin_max_comment_id = es_result['origin_max_comment_id']
        origin_max_comment_user = es_result['origin_max_comment_user']
        if origin_max_comment_id !=0 and origin_max_comment_user != 0:
            origin_max_comment_weibolink = weiboinfo2url(origin_max_comment_user, origin_max_comment_id)
        else:
            origin_max_comment_weibolink = None
        
        retweet_max_retweeted_number = es_result['retweet_max_retweeted_number']
        retweet_max_retweeted_id = es_result['retweet_max_retweeted_id']
        retweet_max_retweeted_user = es_result['retweet_max_retweeted_user']
        if retweet_max_retweeted_id != 0 and retweet_max_retweeted_user != 0:
            retweet_max_retweeted_weibolink = weiboinfo2url(retweet_max_retweeted_user, retweet_max_retweeted_id)
        else:
            retweet_max_retweeted_weibolink = None

        retweet_max_comment_number = es_result['retweet_max_comment_number']
        retweet_max_comment_id = es_result['retweet_max_comment_id']
        retweet_max_comment_user = es_result['retweet_max_comment_user']
        if retweet_max_comment_id != 0 and retweet_max_comment_user != 0:
            retweet_max_comment_weibolink = weiboinfo2url(retweet_max_comment_user, retweet_max_comment_id)
        else:
            retweet_max_comment_weibolink = None
        '''
        result = [importance_dis, activeness_his, influence_his, user_influence_result]
    #print result
    return result


# get importance max & activeness max & influence max
def get_evaluate_max():
    max_result = {}
    index_name = 'user_portrait'
    index_type = 'user'
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
            result = es.search(index=index_name, doc_type=index_type, body=query_body)['hits']['hits']
        except Exception, e:
            raise e
        max_evaluate = result[0]['_source'][evaluate]
        max_result[evaluate] = max_evaluate
    return max_result

# get grouop user list
def get_group_list(task_name):
    results = []
    try:
        es_results = es.get(index=index_name, doc_type=index_type, id=task_name)['_source']
    except:
        return results
    #print 'es_result:', es_results['uid_list'], type(es_results['uid_list'])
    uid_list = es_results['uid_list']
    user_portrait_attribute = es.mget(index='user_portrait', doc_type='user', body={'ids':uid_list})['docs']
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
            results.append([uid])
    return results


# delete group results from es_user_portrait 'group_analysis'
def delete_group_results(task_name):
    '''
    query_body = {
        'query':{
            'term':{
                'task_name': task_name
                }
            }
        }
    '''
    #result = es.delete_by_query(index=index_name, doc_type=index_type, body=query_body)
    result = es.delete(index=index_name, doc_type=index_type, id=task_name)
    #print 'result:', result
    '''
    if result['_indices']['twitter']['_shards']['failed'] == 0:
        return True
    else:
        return False
    '''
    return True


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
