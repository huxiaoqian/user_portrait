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
    user_hashtag_result = dict()
    user_ip_result = dict()
    for i in range(1,8):
        ts = ts - 3600*24  
        results = r_cluster.hmget('hashtag_'+str(ts), uid_list)
        #print 'r_cluster hashtag:', results
        ip_results = r_cluster.hmget('ip_'+str(ts), uid_list)
        for j in range(0,len(uid_list)):
            uid = uid_list[j]
            if results[j]:
                hashtag_dict = json.loads(results[j])
                for hashtag in hashtag_dict:
                    if uid in user_hashtag_result:
                        try:
                            user_hashtag_result[uid][hashtag] += hashtag_dict[hashtag]
                        except:
                            user_hashtag_result[uid][hashtag] = hashtag_dict[hashtag]
                    else:
                        user_hashtag_result[uid] = {hashtag: hashtag_dict[hashtag]}

            if ip_results[j]:
                ip_dict = json.loads(ip_results[j])
                for ip in ip_dict:
                    if uid in user_ip_result:
                        try:
                            user_ip_result[uid][ip] += ip_dict[ip]
                        except:
                            user_ip_result[uid][ip] = ip_dict[ip]
                    else:
                        user_ip_result[uid] = {ip: ip_dict[ip]}

            '''
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
            '''
    
    for uid in uid_list:
        try:
             hashtag_dict = user_hashtag_result[uid]
             hashtag_string = json.dumps(hashtag_dict)
             hashtag_list = '&'.join(hashtag_dict.keys())
        except KeyError:
            hashtag_string = ''
            hashtag_list = ''
        try:
            ip_dict = user_ip_result[uid]
            geo_dict = ip2geo(ip_dict)
            geo_string = json.dumps(geo_dict)
            #geo_list = '&'.join(geo_dict.keys())
            geo_dict_keys = geo_dict.keys()
            geo_one_list = []
            for key in geo_dict_keys:
                key_list = key.split('\t')
                n = len(key_list)
                geo_one_list.append(key_list[n-1])
            geo_list = '&'.join(geo_one_list)
        except KeyError:
            geo_string = ''
            geo_list = ''
        results_dict[uid] = {'hashtag_dict':hashtag_string, 'activity_geo_dict':geo_string, \
                             'hashtag':hashtag_list, 'activity_geo':geo_list}
    #print 'results_dict:', results_dict
    return results_dict

def ip2geo(ip_dict):
    city_set = set()
    geo_dict = dict()
    for ip in ip_dict:
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
                city = '\t'.join(city.split('\t')[:3])
            try:
                geo_dict[city] += ip_dict[ip]
            except:
                geo_dict[city] = ip_dict[ip]
    return geo_dict

if __name__=='__main__':
    test_uid = ['3308759641', '1815817877']
    result_dict = get_flow_information(test_uid)
    print 'result_dict:', result_dict
