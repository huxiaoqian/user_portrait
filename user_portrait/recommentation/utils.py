# -*- coding: UTF-8 -*-
'''
recommentation
save uid list should be in
'''
import sys
import json
import redis
#from user_portrait.global_utils import R_RECOMMENTATION as r
reload(sys)
sys.path.append('../')
from user_portrait.global_utils import R_RECOMMENTATION as r

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
    results = []
    # read from redis
    hash_name = 'recomment_'+str(date)
    results = r.hgetall(hashname)
    # search from user_profile to rich th show information
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
        value_string = []
        r.hset(in_hash_key, uid, status)
        in_date = ts2datetime(time.time())
        r.hset(compute_hash_name, uid, json.dumps([in_date, compute_status]))
    return True

# show uid who have in but not compute
def show_compute(date):
    results = {}
    hash_name = 'compute'
    results = r.hgetall(hashname)
    #search user profile to inrich information
    return results

# identify uid to start compute
def identify_compute(data):
    results = {}
    compute_status = 1
    hash_name = 'compute'
    uid2compute = r.hgetall(hash_name)
    for uid in data:
        result = r.hget(hash_name, uid)
        in_date = result[uid][0]
        r.hset(hash_name, uid, json.dumps([in_date, compute_status]))

    return results


if __name__=='__main__':
    #test
    test_uid_list = ['2101413011','1995786393','2132734472','2776631980','2128524603',\
                     '1792702427','2703153040','2787852095','1599102507','1726544024']
    #save_uid2compute(test_uid_list)

