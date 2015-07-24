# -*- coding: UTF-8 -*-
import sys
import time
import json
reload(sys)
sys.path.append('../../')
from global_utils import es_user_portrait as es

index_name = 'group_result'
index_type = 'group'


def save_group_results(results):
    status = False
    flag = es.indices.exists(index=index_name)
    if not flag:
        es.indices.create(index=index_name, ignore=400)
    
    es.index(index_name, doc_type=index_type, body=results, id=results['task_name'])
    return status


if __name__=='__main__':
    #test results
    uid_list = ['2010832710', '3482838791', '3697357313', '2496434537',\
                '1642591402', '2074370833', '1640601392', '1773489534',\
                '2722498861', '2803301701']
    results = {
        'task_name': 'test name',
        'submit_date': '2013-09-07',
        'state': 'it is a test',
        'uid_list': json.dumps(uid_list),
        'count': 10,
        'gender': json.dumps({'1':8, '2':2}),
        'verified': json.dumps({'yes':1, 'no':9}),
        'online_pattern': json.dumps({'weibo.com':5, 'iphone':5}),
        'domain': json.dumps({'education':3, 'art':4}),
        'topic': json.dumps({'topic1':1, 'topic2':2}),
        'psycho_status': json.dumps({'status1':1, 'status':2}),
        'psycho_feature': json.dumps({'feature1':1, 'feature':3}),
        'emoticon': 'testtest', 
        'keywords': json.dumps({'word1':5, 'word2':5}),
        'hashtag': json.dumps({'hashtag':1, 'hashtag2':9}),
        'activity_geo': json.dumps({'geo1':5, 'geo2':5}), 
        'importance_his': json.dumps([1,2,3,4,5,6]),
        'activeness_his': json.dumps([0,1,2,3,4,5]),
        'influence_his': json.dumps([4,5,6,7,8,9]),
        'degree_his': json.dumps([7,8,9,4,5,6]),
        'density': 0.5,
        'retweet_weibo_count': 5.6, 
        'retweet_user_count': 8,
        'be_retweeted_count_out': 4,
        'be_retweeted_out': 9,
        'activity_trend': json.dumps([1,2,3,4,5,6,7,8,9]),
        'activity_time': json.dumps({'seg1':1, 'seg2':2}),
        'origin_max_retweeted_number': 10,
        'origin_max_retweeted_id': '123456789', 
        'origin_max_comment_number': 5,
        'origin_max_comment_id': '789456123',
        'retweet_max_retweeted_number': 8,
        'retweet_max_retweeted_id': '456123789',
        'retweet_max_comment_number': 741,
        'retweet_max_comment_id': '963852741',
        'total_weibo_number': 753,
        'origin_max_retweeted_user': '951627843',
        'origin_max_comment_user': '753429861',
        'retweet_max_retweeted_user': '784951623',
        'retweet_max_comment_user': '159267483',
        'activeness': 0.789,
        'importance': 0.753,
        'tightness': 0.267,
        'influence': 0.78235,
        'status': 1
    }
    save_group_results(results)
