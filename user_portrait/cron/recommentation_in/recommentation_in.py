# -*- coding: UTF-8 -*-
import sys
import csv
import json
import time
from elasticsearch import Elasticsearch
from filter_rules import filter_activity, filter_ip, filter_retweet_count, filter_mention

reload(sys)
sys.path.append('../../')
from global_utils import R_CLUSTER_FLOW2,  R_DICT, ES_DAILY_RANK, es_user_portrait
from global_config import RECOMMENTATION_TOPK as k
from time_utils import datetime2ts, ts2datetime

def search_from_es(date):
    # test
    k = 10000
    index_time = ''.join(date.split('-'))
    print 'index_time:', index_time
    index_type = 'bci'
    query_body = {
        'query':{
            'match_all':{}
            },
        'size':k,
        'sort':[{'user_index':{'order':'desc'}}]
        }
    try:
        result = ES_DAILY_RANK.search(index=index_time, doc_type=index_type, body=query_body)['hits']['hits']
    except:
        print 'recommentation in: there is not %s es' % index_time
        return None, None
    user_set = []
    user_set = [user_dict['_id'] for user_dict in result]
    print 'len user_set:',len(user_set)
    return result, set(user_set)

def filter_in(top_user_set):
    results = []
    try:
        in_results = es_user_portrait.mget(index='user_portrait', doc_type='user', body={'ids':top_user_set})
        #print 'in_results:', in_results
    except Exception as e:
        raise e
    filter_list = [item['_id'] for item in in_results['docs'] if item['found'] is True]
    print 'len filter_list:', len(filter_list)
    results = set(top_user_set) - set(in_results)
    print 'filter in results:', len(results)
    return results

def filter_rules(candidate_results):
    results = []
    #rule1: activity count
    filter_result1 = filter_activity(candidate_results)
    #rule2: ip count
    filter_result2 = filter_ip(filter_result1)
    #rule3: retweet count & beretweeted count
    filter_result3 = filter_retweet_count(filter_result2)
    #rule4: mention count
    results = filter_mention(filter_result3)
    return results

def write_recommentation(date, re_user, results):
    f = open('/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/recommentation_in/recommentation_list.csv', 'wb')
    writer = csv.writer(f)
    status = False
    after_filter_results = [[user_dict['_id'], user_dict['_source']['user_index']] for user_dict in results if user_dict['_id'] in re_user]
    sort_results = sorted(after_filter_results, key=lambda x:x[1], reverse=True)
    for item in sort_results:
        writer.writerow(item)
    return True


def read_black_user():
    results = set()
    f = open('/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/recommentation_in/dzs_uid.txt', 'rb')
    for line in f:
        uid_list = line.split(',')
        for uid in uid_list:
            results.add(uid)

    return results

def main():
    now_ts = time.time()
    #test
    now_ts = datetime2ts('2013-09-08')
    date = ts2datetime(now_ts - 3600*24)
    #step1: read from top es_daily_rank
    top_results, top_user_set = search_from_es(date)
    
    # black_uid
    black_user_set = read_black_user()
    print 'black_user_set:', len(black_user_set)
    intersection = top_user_set & black_user_set
    print 'intersection:', len(intersection)

    '''
    #step2: filter users have been in
    candidate_results = filter_in(top_user_set)
    #step3: filter rules about ip count& reposts/bereposts count&activity count
    results = filter_rules(candidate_results)
    #step4: write to recommentation csv/redis
    status = write_recommentation(date, results, top_results)
    if status==True:
        print 'date:%s recommentation done' % date
    '''
if __name__=='__main__':
    main()
