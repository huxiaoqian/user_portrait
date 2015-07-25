# -*- coding: UTF-8 -*-
'''
recommentation
save uid list should be in
'''
import sys
import time
import datetime
import json
import redis
from elasticsearch import Elasticsearch
from update_activeness_record import update_record_index
#from user_portrait.global_utils import R_RECOMMENTATION as r
reload(sys)
sys.path.append('../')
from user_portrait.global_utils import R_RECOMMENTATION as r
from user_portrait.global_utils import R_RECOMMENTATION_OUT as r_out
from user_portrait.global_utils import es_user_portrait as es
from user_portrait.global_utils import es_user_profile
from user_portrait.global_utils import ES_CLUSTER_FLOW1 as es_cluster
from user_portrait.time_utils import ts2datetime
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
    #print 'user_portrait_result:', user_portrait_result[0]
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
            in_date = json.loads(input_result[uid])[0]
            compute_status = json.loads(input_result[uid])[1]
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
        value_string = []
        r.hset(in_hash_key, uid, in_status)
        in_date = ts2datetime(time.time())
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

def show_out_uid(date, fields):
    out_list = []
    date = str(date).replace("-","")
    uid_list = r_out.hget("recommend_delete_list", date)
    if not uid_list:
        return out_list # no one is recommended to out

    return_list = []
    date_out_list = json.loads(r_out.hget("recommend_delete_list",date))
    detail = es.mget(index="user_portrait", doc_type="user", body={"ids":date_out_list}, _source=True)['docs']
            # extract the return dict with the field '_source'
    print detail
    for i in range(len(date_out_list)):
        detail_info = []
        detail_info.append(date_out_list[i])
        for item in fields:
            detail_info.append(detail[i]['_source'][item])
        return_list.append(detail_info)

    return return_list

def decide_out_uid(data):
    uid_list = []
    date = time.strftime("%Y%m%d", time.localtime(time.time()))
    if data:
        uid_list = data.split(",") # decide to delete uids
        exist_data = r_out.hget("decide_delete_list", date)
        if exist_data:
            uid_list.extend(json.loads(exist_data))
        r_out.hset("decide_delete_list", date, json.dumps(uid_list))

    recommend_keys = r_out.hkeys("recommend_delete_list")
    recommend_uid_list = []
    for iter_key in recommend_keys:
        recommend_uid_list.extend(json.loads(r_out.hget("recommend_delete_list",iter_key)))
    not_out_list = list(set(recommend_uid_list).difference(set(uid_list))) # update user info in user_index_profile

    """
    update user states
    if not_out_list:
        update_record_index(not_out_list)
    """
    r_out.delete("recommend_delete_list")
    if uid_list:
        r_out.hset("history_delete_list", date, json.dumps(uid_list))

    return 1

"""
def generate_date(former_date, later_date="21000101"):
    date_list = []
    date_list.append(former_date)
    former_struct = datetime.date(int(former_date[0:4]), int(former_date[4:6]), int(former_date[6:]))
    later_struct = datetime.date(int(later_date[0:4]), int(later_date[4:6]), int(later_date[6:]))
    former_timestamp = time.mktime(former_struct.timetuple())
    later_timestamp = time.mktime(later_struct.timetuple())
    i = 0

    next_timestamp = former_timestamp
    while 1:
        next_timestamp += 86400
        if next_timestamp <= later_timestamp:
            date_list.append(time.strftime('%Y%m%d',time.localtime(next_timestamp)))
            i += 1
            if i == 7:
                break
        else:
            break

    return date_list
"""

def search_history_delete(date):
    history_uid_list = []
    if not date:
        now_date = time.strftime('%Y%m%d',time.localtime(time.time()))
    elif date:
        now_date = date
    else:
        pass

    temp = r_out.hget("history_delete_list", now_date)
    if temp:
        history_uid_list = json.loads(r_out.hget("history_delete_list", now_date))

    return json.dumps(history_uid_list)

if __name__=='__main__':
    #test
    test_uid_list = ['2101413011','1995786393','2132734472','2776631980','2128524603',\
                     '1792702427','2703153040','2787852095','1599102507','1726544024']
    #save_uid2compute(test_uid_list)

