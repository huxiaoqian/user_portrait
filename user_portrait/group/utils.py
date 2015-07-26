# -*- coding: UTF-8 -*-
import sys
import time
import json
#test
'''
reload(sys)
sys.path.append('../')
from global_utils import R_GROUP as r
from global_utils import es_user_portrait as es
from time_utils import ts2datetime, datetime2ts
'''
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

#submit new task and identify the task name unique in es-group_result and save it to redis list
def submit_task(input_data):
    status = 0 # mark it can not submit
    task_name = input_data['task_name']
    try:
        result = es.get(index=index_name, doc_type=index_type, id=task_name)
    except:
        status = 1
    if status != 0:
        r.lpush('group_task', json.dumps(input_data))
        input_data['status'] = 0 # mark the task not compute
        count = len(input_data['uid_list'].split(','))
        input_data['count'] = count
        es.index(index='group_result', doc_type='group', id=task_name, body=input_data)
    return status



#search task by some condition -whether add download
def search_task(task_name, submit_date, state, status):
    results = []
    query = []
    condition_num = 0
    if task_name:
        query.append({'wildcard':{'task_name': '*' + task_name + '*'}})
        condition_num += 1
    if submit_date:
        query.append({'match':{'submit_date': submit_date}})
        condition_num += 1
    if state:
        query.append({'wildcard':{'state': '*' + state + '*'}})
        condition_num += 1
    if status:
        query.addpend({'match':{'status': status}})
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
                        'sort': [{'count':{'order': 'desc'}}]
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
                    'sort': [{'count': {'order': 'desc'}}]
                    }
                )

    try:
        task_dict_list = source['hits']['hits']
    except:
        return None
    result = []
    
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
        result = [task_name, submit_date, state, tightness, activeness, importance]
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
        activity_geo = sort_activity_geo[:5]
        activity_trend = json.loads(es_result['activity_trend'])
        online_pattern_dict = json.loads(es_result['online_pattern'])
        sort_online_pattern = sorted(online_pattern_dict.items(), key=lambda x:x[1], reverse=True)
        online_pattern = sort_online_pattern[:5]
        result = [activity_geo, activity_trend, online_pattern]
    if module=='social':
        degree_his = json.loads(es_result['degree_his'])
        density = es_result['density']
        retweet_weibo_count = es_result['retweet_weibo_count']
        retweet_user_count = es_result['retweet_user_count']
        result = [degree_his, density, retweet_weibo_count, retweet_user_count]
    if module=='think':
        domain_dict = json.loads(es_result['domain'])
        topic_dict = json.loads(es_result['topic'])
        psycho_status = json.loads(es_result['psycho_status'])
        psycho_feature = json.loads(es_result['psycho_feature'])
        result = [domain_dict, topic_dict, psycho_status, psycho_feature]
    if module=='text':
        hashtag_dict = json.loads(es_result['hashtag'])
        sort_hashtag = sorted(hashtag_dict.items(), key=lambda x:x[1], reverse=True)
        hashtag = sort_hashtag[:5]
        emoticon_dict = json.loads(es_result['emoticon'])
        sort_emoticon = sorted(emoticon_dict.items(), key=lambda x:x[1], reverse=True)
        emoticon = sort_emoticon[:5]
        keyword_dict = json.loads(es_result['keywords'])
        sort_keyword = sorted(keyword_dict.items(), key=lambda x:x[1], reverse=True)
        keyword = sort_keyword[:20]
        result = [hashtag, keyword, emoticon]
    if module=='influence':
        importance_dis = json.loads(es_result['importance_his'])
        activeness_his = json.loads(es_result['activeness_his'])
        influence_his = json.loads(es_result['influence_his'])
        origin_max_retweeted_number =es_result['origin_max_retweeted_number']
        origin_max_retweeted_id = es_result['origin_max_retweeted_id']
        origin_max_retweeted_user = es_result['origin_max_retweeted_user']
        origin_max_comment_number = es_result['origin_max_comment_number']
        origin_max_comment_id = es_result['origin_max_comment_id']
        origin_max_comment_user = es_result['origin_max_comment_user']
        retweet_max_retweeted_number = es_result['retweet_max_retweeted_number']
        retweet_max_retweeted_id = es_result['retweet_max_retweeted_id']
        retweet_max_retweeted_user = es_result['retweet_max_retweeted_user']
        retweet_max_comment_number = es_result['retweet_max_comment_number']
        retweet_max_comment_id = es_result['retweet_max_comment_id']
        retweet_max_comment_user = es_result['retweet_max_comment_user']
        result = [importance_dis, activeness_his, influence_his, \
                  origin_max_retweeted_number, origin_max_retweeted_id, origin_max_retweeted_user ,\
                  origin_max_comment_number, origin_max_comment_id, origin_max_comment_user ,\
                  retweet_max_retweeted_number, retweet_max_retweeted_id, retweet_max_retweeted_user ,\
                  retweet_max_comment_number, retweet_max_comment_id, retweet_max_retweeted_user]
    #print result
    return result

# delete group results from es_user_portrait 'group_analysis'
def delete_group_results(task_name):
    query_body = {
        'query':{
            'term':{
                'task_name': task_name
                }
            }
        }
    result = es.delete_by_query(index=index_name, doc_type=index_type, body=query_body)
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
    input_data['task_name'] = 'test_task'
    input_data['uid_list'] = ['2010832710', '3482838791', '3697357313', '2496434537',\
                '1642591402', '2074370833', '1640601392', '1773489534',\
                '2722498861', '2803301701']
    input_data['submit_date'] = '2013-09-08'
    input_data['state'] = 'it is a test'
    #submit_task(input_data)
    test_task_name = 'test name'
    status = delete_group_results(test_task_name)
    #print 'status:', status
