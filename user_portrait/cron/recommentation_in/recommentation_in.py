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
from global_utils import R_RECOMMENTATION as r
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
    return set(user_set), result

def filter_in(top_user_set):
    results = []
    try:
        in_results = es_user_portrait.mget(index='user_portrait', doc_type='user', body={'ids':list(top_user_set)})
    except Exception as e:
        raise e
    filter_list = [item['_id'] for item in in_results['docs'] if item['found'] is True]
    print 'before filter in:', len(top_user_set)
    print 'filter_list:', len(filter_list)
    results = set(top_user_set) - set(filter_list)
    print 'after filter in:', len(results)
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


def write_recommentation(date, results, user_dict):
    f = open('/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/recommentation_in/recommentation_list_'+date+'.csv', 'wb')
    writer = csv.writer(f)
    status = False
    for item in results:
        writer.writerow([item])
    return True

def save_recommentation2redis(date, user_set):
    hash_name = 'recomment_'+str(date)
    status = 0
    for uid in user_set:
        r.hset(hash_name, uid, status)
    return True


def read_black_user():
    results = set()
    f = open('/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/recommentation_in/blacklist_2.csv', 'rb')
    reader = csv.reader(f)
    for line in reader:
        uid = line[0]
        results.add(uid)
    f.close()
    return results

# get sensitive user and filt in
def get_sensitive_user(date):
    results = set()
    r_cluster = R_CLUSTER_FLOW2
    ts = datetime2ts(date)
    results = r_cluster.hgetall('sensitive_'+str(ts))
    if results:
        user_list = results.keys()
    else:
        user_list = []
    results = filter_in(user_list)
    return results

def main():
    now_ts = time.time()
    #test
    now_ts = datetime2ts('2013-09-07')
    date = ts2datetime(now_ts - 3600*24)
    #step1: read from top es_daily_rank
    top_user_set, user_dict = search_from_es(date)
    #step2: filter black_uid
    black_user_set = read_black_user()
    print 'black_user_set:', len(black_user_set)
    intersection = top_user_set & black_user_set
    print 'intersection:', len(intersection)
    subtract_user_set = top_user_set - black_user_set
    print 'after filter blacklist:', len(subtract_user_set)
    #step3: filter users have been in
    candidate_results = filter_in(subtract_user_set)
    #step4: filter rules about ip count& reposts/bereposts count&activity count
    results = filter_rules(candidate_results)
    print 'after filter:', len(results)
    #step5: get sensitive user
    sensitive_user = list(get_sensitive_user(date))
    print 'sensitive_user:', len(sensitive_user)
    print 'sensitive_user_2:', sensitive_user[2]
    print 'before extend results:', len(results), type(results)
    results.extend(sensitive_user)
    print 'after list extend:', len(results), type(results)
    results = set(results)
    print 'end:', len(results)
    #step6: write to recommentation csv/redis
    '''
    status = save_recommentation2redis(date, results)
    status = True
    write_recommentation(date, results, user_dict)
    if status==True:
        print 'date:%s recommentation done' % date
    '''


def write_sensitive_user(results):
    csvfile = open('/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/recommentation_in/sensitive_user.csv', 'wb')
    writer = csv.writer(csvfile)
    for user in results:
        writer.writerow([user])
    return True

if __name__=='__main__':
    #main()
    results = get_sensitive_user('2013-09-07')
    print 'sensitive_user:', len(results)
    write_sensitive_user(results)
