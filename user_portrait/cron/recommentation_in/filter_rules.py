# -*- coding: UTF-8 -*-
import sys
import csv
import json
import time
reload(sys)
sys.path.append('../../')
from global_utils import R_CLUSTER_FLOW2 as r_cluster
from global_utils import R_DICT, es_retweet, retweet_index_name_pre, retweet_index_type
from time_utils import datetime2ts, ts2datetime
from parameter import DAY
from cron.detect.cron_detect import get_db_num

activity_threshold = 50
ip_threshold = 7
retweet_threshold = 20
mention_threshold = 15

csvfile = open('/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/recommentation_in/filter_uid_list.csv', 'wb')
writer = csv.writer(csvfile)



def filter_activity(user_set):
    results = []
    now_date = ts2datetime(time.time())
    # test
    now_date = '2013-09-08'
    ts = datetime2ts(now_date) - DAY
    date = ts2datetime(ts)
    #print 'date:', date
    timestamp = datetime2ts(date)
    for user in user_set:
        over_count = 0
        for i in range(0,7):
            ts = timestamp - DAY*i
            result = r_cluster.hget('activity_'+str(ts), str(user))
            if result:
                items_dict = json.loads(result)
                for item in items_dict:
                    weibo_count = items_dict[item]
                    if weibo_count > activity_threshold:
                        over_count += 1
        if over_count == 0:
            results.append(user)
        else:
            writer.writerow([user, 'activity'])
            
    print 'after filter activity:', len(results)    
    return results

def filter_ip(user_set):
    results = []
    now_date = ts2datetime(time.time())
    # test
    now_date = '2013-09-08'
    ts = datetime2ts(now_date) - DAY
    for user in user_set:
        ip_set = set()
        for i in range(0,7):
            timestamp = ts - DAY*i
            ip_result = r_cluster.hget('ip_'+str(ts), str(user))
            if ip_result:
                result_dict = json.loads(ip_result)
            else:
                result_dict = {}
            for ip in result_dict:
                ip_set.add(ip)
        if len(ip_set) < ip_threshold:
            results.append(user)
        else:
            writer.writerow([user, 'ip'])
    print 'after filter ip:', len(results)
    return results

def filter_retweet_count(user_set):
    FILTER_ITER_COUNT = 100;
    results = []
    now_ts = time.time()
    db_number = get_db_num(now_ts)
    retweet_index_name = retweet_index_name_pre + str(db_number)
    # test
    search_user_count = len(user_set);
    iter_search_count = 0
    while iter_search_count < search_user_count:
        iter_search_user_list = user_set[iter_search_count:iter_search_count + FILTER_ITER_COUNT]
        try:
            retweet_result = es_retweet.mget(index = retweet_index_name, doc_type = retweet_index_type,\
                    body = {'ids':iter_search_user_list}, _source=True)['docs']
        except:
            retweet_result = []
        if retweet_result:
            print 'retweet_result:', retweet_result
        for retweet_item in retweet_result:
            retweet_set = set()
            user = retweet_item['_id']
            per_retweet_result = json.loads(retweet_item['_source']['uid_retweet'])
            for retweet_user in per_retweet_result:
                retweet_set.add(retweet_user)
            if len(retweet_set) < retweet_threshold:
                results.append(user)
            else:
                writer.writerow([user, 'retweet'])
        iter_search_count += FILTER_ITER_COUNT
    print 'after filter retweet:', len(results)
    return results

def filter_mention(user_set):
    results = []
    now_date = ts2datetime(time.time())
    # test
    now_date = '2013-09-08'
    timestamp = datetime2ts(now_date) - DAY
    date = ts2datetime(timestamp)
    for user in user_set:
        mention_set = set()
        for i in range(0,7):
            ts = timestamp - DAY*i
            result = r_cluster.hget('at_'+str(ts), str(user))
            if result:
                item_dict = json.loads(result)
                for at_user in item_dict:
                    mention_set.add(at_user)
        at_count = len(mention_set)
        if at_count < mention_threshold:
            results.append(user)
        else:
            writer.writerow([user, 'mention'])
    print 'after filter mention:', len(results)
    return results
