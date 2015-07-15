# -*- coding: UTF-8 -*-
import sys
import time
from weibo_api import compute2in
reload(sys)
sys.path.append('../../')
from global_utils import R_RECOMMENTATION as r

def scan_compute_redis():
    hash_name = 'compute'
    results = r.hgetall('compute')
    user_list = []
    mapping_dict = dict()
    for uid in results:
        status = results[uid]
        if status == '1':
            user_set.append(uid)
            mapping_dict[uid] = 2 # mark status:2 computing
    r.hmset('compute', mapping_dict)
    #acquire bulk user weibo data
    user_weibo_dict = read_user_weibo(user_list)
    #compute text attribute
    compute_status = compute2in(user_weibo_dict)
    if compute_status==True:
        delete_compute_redis(user_set)

def delete_compute_redis(user_set):
    hash_name = 'compute'
    for user in user_set:
        r.hdel(hash_name, user)

if __name__=='__main__':
    scan_compute_redis()
