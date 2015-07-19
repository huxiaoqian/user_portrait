# -*- coding: UTF-8 -*-
'''
acquire the information from flow
input: uid_list
output: {uid:{attr:value}}
update: one day
'''
import IP
import sys
import time
import json
reload(sys)
sys.path.append('../../')
from global_utils import R_CLUSTER_FLOW2 as r_cluster
from time_utils import datetime2ts, ts2datetime

def get_flow_information(uid_list):
    results_dict = {}
    now_ts = time.time()
    now_date = ts2datetime(now_ts)
    ts = datetime2ts(now_date)
    #test
    hashtag_results = {}
    geo_results = {}
    ts = datetime2ts('2013-09-08')
    for i in range(1,8):
        ts = ts - 3600*24  
        results = r_cluster.hmget('hashtag_'+str(ts), uid_list)
        #print 'r_cluster hashtag:', results
        ip_results = r_cluster.hmget('ip_'+str(ts), uid_list)
        for j in range(0,len(uid_list)):
            if results[j]:
                hashtag_list = json.loads(results[j]).keys()
                try:
                    hashtag_results[uid_list[j]].extend(hashtag_list)
                except:
                    hashtag_results[uid_list[j]] = hashtag_list
            if ip_results[j]:
                ip_list = json.loads(ip_results[j]).keys()
                try:
                    geo_results[uid_list[j]].extend(ip_list)
                except:
                    geo_results[uid_list[j]] = ip_list
    
    for uid in uid_list:
        try:
             hashtag_list = set(hashtag_results[uid])
             hashtag_string = ' '.join(hashtag_list)
        except KeyError:
            hashtag_string = ''
        try:
            ip_list = set(geo_results[uid])
            geo_list = ip2geo(ip_list)
            geo_string = '&'.join(geo_list)
        except KeyError:
            geo_string = ''
        results_dict[uid] = {'hashtag':hashtag_string, 'activity_geo':geo_string}
    #print 'results_dict:', results_dict
    return results_dict

def ip2geo(ip_list):
    city_set = set()
    for ip in ip_list:
        try:
            city = IP.find(str(ip))
            if city:
                city.encode('utf-8')
            else:
                city = ''
        except Exception, e:
            city = ''
        if city:
            len_city = len(city.split('\t'))
            if len_city==4:
                city = '\t'.join(city.split('\t')[:2])
            city_set.add(city)
    return list(city_set)

if __name__=='__main__':
    test_uid = ['3308759641', '1815817877']
    get_flow_information(test_uid)
