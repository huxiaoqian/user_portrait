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
#from user_portrait.global_utils import R_RECOMMENTATION as r
reload(sys)
sys.path.append('../')
from user_portrait.global_utils import R_RECOMMENTATION as r
from user_portrait.global_utils import R_RECOMMENTATION_OUT as r_out
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
# show recommentation in uid
def recommentation_in(input_ts):
    date = ts2datetime(input_ts)
    recomment_results = []
    # read from redis
    hash_name = 'recomment_'+str(date)
    results = r.hgetall(hash_name)
    # search from user_profile to rich th show information
    for item in results:
        status = results[item]
        if status=='0':
            recomment_results.append(item)

    return recomment_results

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
    date = ts2datetime(date)
    results = []
    hash_name = 'recomment_'+str(date)
    results = r.hgetall(hash_name)
    return results

# show uid who have in but not compute
def show_compute(date):
    results = {}
    hash_name = 'compute'
    results = r.hgetall(hash_name)
    #search user profile to inrich information
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

def show_out_uid(date):
    out_dict = {}
    data = str(date).replace("-","")
    uid_dict = r_out.hgetall("recommend_delete_list")
    if not uid_dict:
        return out_dict # no one is recommended to out

    keys = r_out.hkeys("recommend_delete_list")

    """
    if data in set(keys):
        out_dict[data] = json.dumps(r_out.hget("recommend_delete_list", data))

    """
    for iter_key in keys:
        out_dict[iter_key] = json.dumps(r_out.hget("recommend_delete_list",iter_key))

    return out_dict

def decide_out_uid(data):
    uid_list = []
    date = time.strftime("%Y%m%d", time.localtime(time.time()))
    if data:
        uid_list = data.split(",") # decide to delete uids
        r_out.hset("decide_delete_list", date, json.dumps(uid_list))
    r_out.delete("recommend_delete_list")
    r_out.hset("history_delete_list", date, json.dumps(uid_list))

    return 1

def genereat_date(former_date, later_date="21000101"):
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

def search_history_delete(date):
    history_uid_dict = {}
    if not date:
        now_date = time.strftime('%Y%m%d',time.localtime(time.time()))
        date_list = genereat_date(now_date)

    else:
        query_date = date.split(",")
        date_list = generate_date(query_date[0], query_date[1])

    for key in date_list:
        history_uid_dict[key] = json.loads(r_out.hget("history_delete_list", key))

    return json.dumps(history_uid_dict)

if __name__=='__main__':
    #test
    test_uid_list = ['2101413011','1995786393','2132734472','2776631980','2128524603',\
                     '1792702427','2703153040','2787852095','1599102507','1726544024']
    #save_uid2compute(test_uid_list)

