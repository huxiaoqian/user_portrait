# -*- coding: UTF-8 -*-
'''
compute activeness, influence, importance
first:activeness
     input: uid, geo
second:influence
     input: uid
last: importance
     input: uid, domain, uid
'''
import IP
import sys
import json
import time
import math
import numpy as np
from config import activeness_weight_dict, importance_weight_dict,\
                   domain_weight_dict, topic_weight_dict
reload(sys)
sys.path.append('../../')
from global_utils import R_CLUSTER_FLOW2 as r_cluster
from global_utils import ES_CLUSTER_FLOW1 as es
from global_utils import es_user_portrait 
from time_utils import ts2datetime, datetime2ts

def get_activeness(uid, activity_geo):
    result = 0
    now_ts = time.time()
    now_date = ts2datetime(now_ts)
    timestamp = datetime2ts(now_date)
    #test
    timestamp = datetime2ts('2013-09-08')
    # deal activity_time fft and statusnum
    activity_list = []
    statusnum = 0
    for i in range(1,8):
        ts = timestamp - 24*3600*i
        r_result = r_cluster.hget('activity_'+str(ts), uid)
        if r_result:
            r_result = json.loads(r_result)
        #print 'r_result:', r_result
        for i in range(0,96):
            try:
                count = r_result[str(i)]
            except:
                count = 0
            activity_list.append(float(count))
    #print 'activity_list:', activity_list
    statusnum = sum(activity_list)
    signal = np.array(activity_list)
    fftResult = np.abs(np.fft.fft(signal)) ** 2
    n = signal.size
    freq = np.fft.fftfreq(n, d=1)
    i = 0
    max_val = 0
    max_freq = 0
    for val in fftResult:
        #print str(1/freq[i]) + ',' + str(val)
        if val>max_val and freq[i]>0:
            max_val = val
            max_freq = freq[i]
        i = i + 1
    print 'i:', i
    print 'max_freq, max_val:', max_freq, max_val
    # deal avtivity_geo input: 'geo&geo'
    activity_geo_count = len(activity_geo.split('&'))
    result = activeness_weight_dict['activity_time'] * math.log(max_freq  + 1) + \
             activeness_weight_dict['activity_geo'] * math.log(activity_geo_count + 1) +\
             activeness_weight_dict['statusnum'] * math.log(statusnum + 1)
    print 'activeness:', result
    return result

def get_influence(uid):
    result = 0
    now_ts = time.time()
    now_date = ts2datetime(now_ts - 3600*24)
    # test
    now_date = '2013-09-07'
    index_time = ''.join(now_date.split('-'))
    index_type = 'bci'
    result = es.get(index=index_time, id=uid, doc_type=index_type)['_source']['user_index']
    print 'result_dict:', result
    query_body = {
        'query':{
            'filtered':{
                'query':{
                    'match_all':{}
                    },
                'filter':{
                    'range':{
                        'user_index':{
                            'gte':result
                            }
                        }
                    }
            }
        }
    }
    rank = es.count(index=index_time, doc_type=index_type, body=query_body)['count']
    #print 'rank:', rank
    return result

def get_importance(uid, domain, topic):
    result = 0
    domain_result = 0
    domain_list = domain.split(' ')
    #print 'domain_list:', domain_list
    for domain in domain_list:
        try:
            domain_result += domain_weight_dict[domain]
        except:
            pass
    topic_result = 0
    topic_list = topic.split(' ')
    #print 'topic_list:', topic_list
    for topic in topic_list:
        try:
            topic_result += topic_weight_dict[topic]
        except:
            pass
    #get fansnum, origin_weibo_retweeted_total_number, retweeted_weibo_retweeted_total_number
    now_ts = time.time()
    date = ts2datetime(now_ts-3600*24)
    #test 
    date = '2013-09-07'
    index_time = ''.join(date.split('-'))
    index_type = 'bci'
    es_result = es.get(index=index_time, doc_type=index_type, id=uid)['_source']
    fansnum = es_result['user_fansnum']
    retweetednum = es_result['origin_weibo_retweeted_total_number'] + es_result['retweeted_weibo_retweeted_total_number']
    result = importance_weight_dict['fansnum']*fansnum + importance_weight_dict['retweeted_num']*retweetednum + \
             importance_weight_dict['domain']*domain_result + importance_weight_dict['topic']*topic_result
    #print 'importance result:', result
    return result

def ip2geo(ip_list):
    ip_list = list(ip_list)
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

#use to update
def get_activity_geo(uid):
    ip_result = []
    now_ts = time.time()
    now_date = ts2datetime(now_ts)
    ts = datetime2ts(now_date)
    geo_result = {}
    # test
    ts = datetime2ts('2013-09-08')
    for i in range(1,8):
        ts = ts - 24*3600
        r_result = r_cluster.hget('ip_'+str(ts), uid)
        if r_result:
            ip_list = json.loads(r_result).keys()
            ip_result.extend(ip_list)
    ip_list = set(ip_result)
    geo_string = '&'.join(ip2geo(ip_list))
    print 'geo_string:', geo_string
    return geo_string

#use to update
def get_domain_topic(uid):
    result = dict()
    index_time = 'user_portrait'
    index_type = 'user'
    result = es_user_portrait.get(index=index_time, doc_type=index_type, id=uid)['_source']
    if result:
        print 'domain, toic:', result['domain'], result['topic']
        return result['domain'], result['topic'] 
    else:
        return None, None



# status: insert or update
# if insert, input info include: uid, domain, topic, activity_geo
# if update, input info include: uid (other information to be got from es)
def get_evaluate_index(user_info, status='insert'):
    if 'uid' not in user_info:
        return None
    results = dict()
    uid = user_info['uid']
    if status=='insert':
        activity_geo = user_info['activity_geo']
        domain = user_info['domain']
        topic = user_info['topic']
    elif status=='update':
        activity_geo = get_activity_geo(uid)
        domain, topic = get_domain_topic(uid)
        print 'domain, topic:', domain, topic
    results['activeness'] = get_activeness(uid, activity_geo)
    results['influence'] = get_influence(uid)
    results['importance'] = get_importance(uid, domain, topic)
    return results


if __name__=='__main__':
    test_uid_info = {'uid':'2407339403','domain':'domain1 domain2', 'topic':'testtopic', 'activity_geo':'geo&geo'}
    #get_evaluate_index(test_uid_info, 'insert') # status: insert or update
    #get_influence(uid='1978622405')
    #get_activity_geo('1978622405')
    get_domain_topic('1721131891')
