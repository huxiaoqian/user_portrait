# -*- coding: UTF-8 -*-
'''
use to recommentation
'''
import csv
import json
import time
from time_utils import ts2datetime, datetime2ts
from elasticsearch import Elasticsearch
from config import r_cluster, r
import matplotlib.pyplot as plt

es = Elasticsearch('219.224.135.93', timeout = 60)
index_name = time.strftime('%Y%m%d', time.localtime())
index_type = 'bci'

csvfile = open('/home/ubuntu4/huxiaoqian/portrait/test_recommentation_ip20.csv', 'rb')
writer = csv.writer(csvfile)

'''
step1:read candidate from ES
step2:rules to select
'''

def search_from_es():
    #index_time_list = ['20130901', '20130902', '20130903', '20130904', '20130905', '20130906', '20130907']
    index_time_list = ['20130907']
    k = 10000
    date_userset_dict = dict()
    for index_time in index_time_list:
        query_body = {
            'query':{
                'match_all' : {}
                },
            'size': k,
            'sort': [{"user_index" :{ 'order' : 'desc'}}]
            }

        result = es.search(index=index_time, doc_type = index_type, body=query_body)['hits']['hits']
        #print 'result:', result
        user_set = []
        for user_dict in result:
            #print user_dict
            uid = user_dict['_id']
            user_set.append(uid)
        date_userset_dict[index_time] = user_set
    return date_userset_dict

def compute_es_overlap():
    date_userset_dict = search_from_es()
    user_union = set(date_userset_dict['20130901']) | set(date_userset_dict['20130902'])
    user_combine = set(date_userset_dict['20130901']) & set(date_userset_dict['20130902'])
    print '20130901: ' + str(len(date_userset_dict['20130901']))
    print '20130902: ' + str(len(date_userset_dict['20130602']))
    print 'union: ' + str(len(user_union))
    print 'combine:' + str(len(user_combine))           

def compute_user_ip():
    date_user_set_dict = search_from_es()
    user_set = date_user_set_dict['20130907']
    timestamp = datetime2ts('2013-09-07')
    uid_ip_results = dict()
    for user in user_set:
        for i in range(0, 7):
            ts = timestamp - 24 * 3600 * i
            result_string = r_cluster.hget('ip_'+str(ts), str(user))
            if result_string:
                result_dict = json.loads(result_string)
                #print 'yes user'
            else:
                result_dict = {}
            for ip in result_dict:
                try:
                    uid_ip_results[user].append(ip)
                except:
                    uid_ip_results[user] = [ip]
    ip_dis_dict = dict()
    for user in user_set:
        if user in uid_ip_results:
            ip_count = len(set(uid_ip_results[user]))
            # 查看使用ip数超过20的用户的具体排名是多少
            if ip_count>=20:
                deal_ip_count(user, ip_count)
            try:
                ip_dis_dict[str(ip_count)] += 1
            except:
                ip_dis_dict[str(ip_count)] = 1
    sort_ip_dis = sorted(ip_dis_dict.items(), key = lambda x:int(x[0]))
    print 'ip_dis_dict:', sort_ip_dis
    top20 = 0
    sum_count = 0
    for item in sort_ip_dis:
        ip_count = int(item[0])
        user_count = int(item[1])
        if ip_count<=20:
            print 'ip_count, user_count:', ip_count, user_count
            top20 += user_count
        sum_count += user_count
    print 'top20:', top20
    print 'sum_count:', sum_count
    print 'ratio:', float(top20) / sum_count

def deal_ip_count(user, ip_count):
    query_body = {
            'query':{
                'match_all' : {
                    '_id': user
                    }
                },
            }
    result = es.search(index=index_name, doc_type = index_type, body=query_body)['hits']['hits']
    for user_dict in result:
        user_index = user_dict['_source']['user_index']
        writer.writerow([user, ip_count, user_index])
    csvfile.close()

def compute_user_retweet():
    count = 0
    scan_cursor = 0
    retweet_result_dict = dict()
    while 1:
        if count == 100:
            break
        results = r.scan(scan_cursor, count=100)
        count += 100
        for result in results[1]:
            if 'retweet_' == result[:8]:
                uid = result[8:]
                retweet_dict = r.hgetall(result)
                retweet_user_count = len(retweet_dict)
                all_retweet_count = 0
                for ruid in retweet_dict:
                    all_retweet_count += int(retweet_dict[ruid])
                retweet_result_dict[uid] = [retweet_user_count, all_retweet_count]
    print 'retweet_result_dict:', retweet_result_dict
    user_dis_dict = dict()
    retweet_dis_dict = dict()
    for uid in retweet_result_dict:
        user_count, retweet_count = retweet_result_dict[uid]
        try:
            user_dis_dict[user_count] += 1
        except:
            user_dis_dict[user_count] = 1
        try:
            retweet_dis_dict[retweet_count] += 1
        except:
            retweet_dis_dict[retweet_count] = 1
    print 'retweet_dis_dict:', retweet_dis_dict
    print 'user_dis_dict:', user_dis_dict
    x = []
    y = []
    '''
    for user_count in user_dis_dict:
        count = user_dis_dict[user_count]
        x.append(user_count)
        y.append(count)
    '''
    for retweet_count in retweet_dis_dict:
        count = retweet_dis_dict[retweet_count]
        x.append(retweet_count)
        y.append(count)
    print 'x:', x
    print 'y:', y
    plt.figure()
    plt.scatter(x, y)
    plt.xlabel('retweet_count')
    plt.ylabel('count')
    plt.title('retweet_count distribution')
    plt.show()
        
    #print 'retweet_result_dict:', retweet_result_dict
                
def test():
    # test ES overlap of user who ranking before 100000
    #compute_es_overlap()
    # test top 10000 user from ES ip number to set ip  threshold
    compute_user_ip()
    # test retweet number distribution
    #compute_user_retweet()

if __name__=='__main__':
    # test 
    test()
