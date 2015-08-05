# -*- coding: UTF-8 -*-
'''
recommentation
save uid list should be in
'''
import IP
import sys
import time
import datetime
import json
import redis
from elasticsearch import Elasticsearch
from update_activeness_record import update_record_index
#from user_portrait.global_utils import R_RECOMMENTATION as r
from user_portrait.global_utils import R_RECOMMENTATION as r
from user_portrait.global_utils import R_RECOMMENTATION_OUT as r_out
from user_portrait.global_utils import R_CLUSTER_FLOW2 as r_cluster
from user_portrait.global_utils import es_user_portrait as es
from user_portrait.global_utils import es_user_profile
from user_portrait.global_utils import ES_CLUSTER_FLOW1 as es_cluster
from user_portrait.filter_uid import all_delete_uid
from user_portrait.time_utils import ts2datetime, datetime2ts

#test
'''
def save_uid2compute(uid_list):
    test_date = '2013-09-01'
    hash_name = 'compute'
    status = 0
    for uid in uid_list:
        value_string = [test_date, status]
        r.hset(hash_name, uid, json.dumps(value_string))
'''

#get user detail
#output: uid, uname, location, fansnum, statusnum, influence
def get_user_detail(date, input_result, status):
    results = []
    if status=='show_in':
        uid_list = input_result
    if status=='show_compute':
        uid_list = input_result.keys()
    if status=='show_in_history':
        uid_list = input_result.keys()
    index_name = ''.join(date.split('-'))
    # test
    index_name = '20130907'
    index_type = 'bci'
    user_bci_result = es_cluster.mget(index=index_name, doc_type=index_type, body={'ids':uid_list}, _source=True)['docs']
    #print 'user_portrait_result:', user_bci_result[0]
    user_profile_result = es_user_profile.mget(index='weibo_user', doc_type='user', body={'ids':uid_list}, _source=True)['docs']
    #print 'user_profile_result:', user_profile_result
    for i in range(0, len(uid_list)):
        uid = uid_list[i]
        bci_dict = user_bci_result[i]
        profile_dict = user_profile_result[i]
        try:
            bci_source = bci_dict['_source']
        except:
            bci_source = None
        if bci_source:
            influence = bci_source['user_index']
        else:
            influence = ''
        try:
            profile_source = profile_dict['_source']
        except:
            profile_source = None
        if profile_source:
            uname = profile_source['nick_name'] 
            location = profile_source['user_location']
            fansnum = profile_source['fansnum']
            statusnum = profile_source['statusnum']
        else:
            uname = ''
            location = ''
            fansnum = ''
            statusnum = ''
        if status == 'show_in':
            results.append([uid, uname, location, fansnum, statusnum, influence])
        if status == 'show_compute':
            print 'input_result:', json.loads(input_result[uid])
            in_date = json.loads(input_result[uid])[0]
            compute_status = json.loads(input_result[uid])[1]
            if compute_status == '1':
                compute_status = '3'
            results.append([uid, uname, location, fansnum, statusnum, influence, in_date, compute_status])
        if status == 'show_in_history':
            in_status = input_result[uid]
            results.append([uid, uname, location, fansnum, statusnum, influence, in_status])

    return results


# show recommentation in uid
def recommentation_in(input_ts):
    date = ts2datetime(input_ts)
    recomment_results = []
    # read from redis
    results = []
    hash_name = 'recomment_'+str(date)
    results = r.hgetall(hash_name)
    if not results:
        return results
    # search from user_profile to rich th show information
    for item in results:
        status = results[item]
        if status=='0':
            recomment_results.append(item)
    if recomment_results:
        results = get_user_detail(date, recomment_results, 'show_in')
    else:
        results = []
    return results

# identify uid to in user_portrait
def identify_in(data):
    in_status = 1
    compute_status = 0
    in_hash_name = 'recomment_'
    compute_hash_name = 'compute'
    for item in data:
        date = item[0] # identify the date form '2013-09-01' with web
        in_hash_key = in_hash_name + str(date)
        uid = item[1]
        status = item[2]
        value_string = []
        r.hset(in_hash_key, uid, in_status)
        if status == '1':
            in_date = ts2datetime(time.time())
            compute_status = '1'
        elif status == '2':
            in_date = ts2datetime(time.time())
            compute_status = '2'
        r.hset(compute_hash_name, uid, json.dumps([in_date, compute_status]))
    return True


#show in history
def show_in_history(date):
    results = []
    hash_name = 'recomment_'+str(date)
    r_results = r.hgetall(hash_name)
    if r_results:
        results = get_user_detail(date, r_results, 'show_in_history')
    return results

# show uid who have in but not compute
def show_compute(date):
    results = []
    hash_name = 'compute'
    r_results = r.hgetall(hash_name)
    #search user profile to inrich information
    if r_results:
        results = get_user_detail(date, r_results, 'show_compute')
        return results
    else:
        return results

# identify uid to start compute
def identify_compute(data):
    results = False
    compute_status = 1
    hash_name = 'compute'
    uid2compute = r.hgetall(hash_name)
    for item in data:
        uid = item[1]
        result = r.hget(hash_name, uid)
        print 'result:', result
        in_date = json.loads(result)[0]
        r.hset(hash_name, uid, json.dumps([in_date, compute_status]))

    return True

def show_out_uid(fields):
    out_list = []
    recommend_dict = r_out.hgetall("recommend_delete_list")
    recommend_keys = recommend_dict.keys()
    for iter_key in recommend_keys:
        out_list.extend(json.loads(r_out.hget("recommend_delete_list",iter_key)))
    if not out_list:
        return out_list # no one is recommended to out

    return_list = []
    detail = es.mget(index="user_portrait", doc_type="user", body={"ids":out_list}, _source=True)['docs']
            # extract the return dict with the field '_source'
    filter_uid = all_delete_uid()
    for i in range(len(out_list)):
        if detail[i]['_source']['uid'] in filter_uid:
            continue
        detail_info = []
        for item in fields:
            detail_info.append(detail[i]['_source'][item])
        return_list.append(detail_info)

    return return_list

def decide_out_uid(date, data):
    uid_list = []
    now_date = time.strftime("%Y%m%d", time.localtime(time.time()))
    if data:
        uid_list = data.split(",") # decide to delete uids
        exist_data = r_out.hget("decide_delete_list", now_date)
        if exist_data and exist_data != []:
            uid_list.extend(json.loads(exist_data))
            uid_list = list(set(uid_list))
        r_out.hset("decide_delete_list", now_date, json.dumps(uid_list))

    """
    if uid_list and uid_list != []:
        update_record_index(not_out_list)
    """
    filter_uid = all_delete_uid()
    uid_list = data.split(",")
    current_date_list = json.loads(r_out.hget("recommend_delete_list", date))
    new_list =  list(set(current_date_list).difference(set(uid_list)))
    new_list = list(set(new_list).difference(filter_uid))
    r_out.hset("recommend_delete_list", date, json.dumps(new_list))

    """
    if uid_list:
        temp = r_out.hget("history_delete_list", now_date)
        if temp:
            exist_data = json.loads(r_out.hget("history_delete_list", now_date))
            uid_list.extend(exist_data)
        r_out.hset("history_delete_list", now_date, json.dumps(uid_list))

    """
    return 1


def search_history_delete(date):
    return_list = []
    if not date:
        now_date = time.strftime('%Y%m%d',time.localtime(time.time()))
    elif date:
        now_date = date
    else:
        pass

    fields = ['uid','uname','domain','topic','influence','importance','activeness']
    temp = r_out.hget("decide_delete_list", now_date)
    print temp
    if temp:
        history_uid_list = json.loads(r_out.hget("decide_delete_list", now_date))
        if history_uid_list != []:
            detail = es.mget(index="user_portrait", doc_type="user", body={"ids":history_uid_list}, _source=True)['docs']
            for i in range(len(history_uid_list)):
                detail_info = []
                for item in fields:
                    detail_info.append(detail[i]['_source'][item])
                return_list.append(detail_info)

    return json.dumps(return_list)


def show_all_out():
    delete_dict = r_out.hgetall('decide_delete_list')
    delete_keys_list = delete_dict.keys()

    return_list = []
    fields = ['uid','uname','domain','topic','influence','importance','activeness']
    for iter_key in delete_keys_list:
        temp_list = []
        temp = json.loads(r_out.hget('decide_delete_list', iter_key))
        if temp and temp != []:
            temp_list.append(iter_key) # decide  delete date
            detail = es.mget(index="user_portrait", doc_type="user", body={"ids":temp}, _source=True)['docs']
            for i in range(len(temp)):
                detail_info = []
                for item in fields:
                    print detail
                    detail_info.append(detail[i]['_source'][item])
                temp_list.append(detail_info)

            return_list.append(temp_list)

    return json.dumps(return_list)



# get user time trend (7 day)
def get_user_trend(uid):
    activity_result = dict()
    now_ts = time.time()
    date = ts2datetime(now_ts-24*3600)
    ts = datetime2ts(date)
    #test
    ts = datetime2ts('2013-09-08')
    timestamp = ts
    results = dict()
    for i in range(1, 8):
        ts = timestamp - 24*3600*i
        try:
            result_string = r_cluster.hget('activity_'+str(ts), str(uid))
        except:
            result_string = ''
        if not result_string:
            continue
        result_dict = json.loads(result_string)
        for time_segment in result_dict:
            try:
                results[int(time_segment)/16*15*60*16+ts] += result_dict[time_segment]
            except:
                results[int(time_segment)/16*15*60*16+ts] = result_dict[time_segment]
    
    trend_list = []
    for i in range(1, 8):
        ts = timestamp - i*24*3600
        for j in range(0, 6):
            time_seg = ts + j*15*60*16
            if time_seg in results:
                trend_list.append((time_seg, results[time_seg]))
            else:
                trend_list.append((time_seg, 0))
    sort_trend_list = sorted(trend_list, key=lambda x:x[0], reverse=True)
    x_axis = [item[0] for item in sort_trend_list]
    y_axis = [item[1] for item in sort_trend_list]
    return [x_axis, y_axis]

# get user hashtag
def get_user_hashtag(uid):
    user_hashtag_result = {}
    now_ts = time.time()
    now_date = ts2datetime(now_ts)
    ts = datetime2ts(now_date)
    #test
    ts = datetime2ts('2013-09-08')
    for i in range(1, 8):
        ts = ts - 3600*24
        results = r_cluster.hget('hashtag_'+str(ts), uid)
        if results:
            hashtag_dict = json.loads(results)
            for hashtag in hashtag_dict:
                try:
                    user_hashtag_result[hashtag] += hashtag_dict[hashtag]
                except:
                    user_hashtag_result[hashtag] = hashtag_dict[hashtag]
    sort_hashtag_dict = sorted(user_hashtag_result.items(), key=lambda x:x[1], reverse=True)

    return sort_hashtag_dict

# get user geo
def get_user_geo(uid):
    result = []
    user_geo_result = {}
    user_ip_dict = {}
    user_ip_result = dict()
    now_ts = time.time()
    now_date = ts2datetime(now_ts)
    ts = datetime2ts(now_date)
    #test
    ts = datetime2ts('2013-09-08')
    for i in range(1, 8):
        ts = ts - 3600*24
        results = r_cluster.hget('ip_'+str(ts), uid)
        if results:
            ip_dict = json.loads(results)
            for ip in ip_dict:
                try:
                    user_ip_result[ip] += ip_dict[ip]
                except:
                    user_ip_result[ip] = ip_dict[ip]
    #print 'user_ip_result:', user_ip_result
    user_geo_dict = ip2geo(user_ip_result)
    user_geo_result = sorted(user_geo_dict.items(), key=lambda x:x[1], reverse=True)

    return user_geo_result

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
                city = '\t'.join(city.split('\t')[:2])
            try:
                geo_dict[city] += ip_dict[ip]
            except:
                geo_dict[city] = ip_dict[ip]
    return geo_dict


# show more information in recommentation
def recommentation_more_information(uid):
    result = {}
    result['time_trend'] = get_user_trend(uid)
    result['hashtag'] = get_user_hashtag(uid)
    result['activity_geo'] = get_user_geo(uid)
    #print 'result:', result
    return result


if __name__=='__main__':
    #test
    test_uid_list = ['2101413011','1995786393','2132734472','2776631980','2128524603',\
                     '1792702427','2703153040','2787852095','1599102507','1726544024']
    #save_uid2compute(test_uid_list)
    recommentation_more_information('2101413011')

