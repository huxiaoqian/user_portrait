# -*- coding: UTF-8 -*-
import sys
import csv
import json
import time
from elasticsearch import Elasticsearch

reload(sys)
sys.path.append('../../')
from global_utils import R_CLUSTER_FLOW2,  R_DICT, ES_DAILY_RANK, es_user_portrait
from global_config import RECOMMENTATION_TOPK as k
from time_utils import datetime2ts, ts2datetime

def search_from_es(date):
    # test
    k = 1000
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
    user_set = set()
    for user_dict in result:
        user_set.add(user_dict['_id'])
    print 'len user_set:', len(user_set) 
    return result, user_set

def filter_in(top_results):
    results = []
    try:
        in_results = es_user_portrait.mget(index='weibo_user', doc_type='user', body={'ids':list(top_results)}, fields=['_id'])
        print 'in_results:', in_results
    except Exception as e:
        raise e
    results = (top_results) - set(in_results)
    print 'filter in results:', len(results)
    return results

def filter_rules(candidate_results):
    results = []
    #rule1: ip count
    #rule2: activity count
    #rule3: retweet count & beretweeted count
    #rule4: mention count
    return results

def write_recommentation(date, results):
    status = False
    return status


def main():
    now_ts = time.time()
    #test
    now_ts = datetime2ts('2013-09-08')
    date = ts2datetime(now_ts - 3600*24)
    #step1: read from top es_daily_rank
    top_user_set, top_results = search_from_es(date)
    #step2: filter users have been in
    candidate_results = filter_in(top_user_set)
    #step3: filter rules about ip count& reposts/bereposts count&activity count
    '''
    results = filter_rules(candidate_results)
    #step4: write to recommentation csv/redis
    status = write_recommentation(date, results)
    if status==True:
        print 'Ddate:%s recommentation done' % date
    '''    
if __name__=='__main__':
    main()
