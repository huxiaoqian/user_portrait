# -*- coding: UTF-8 -*-
import sys
import time
import json
from weibo_api import read_user_weibo
from cron_text_attribute import compute2in
reload(sys)
sys.path.append('../../')
from global_utils import R_RECOMMENTATION as r

def scan_compute_redis():
    hash_name = 'compute'
    results = r.hgetall('compute')
    user_list = []
    mapping_dict = dict()
    for uid in results:
        user_list = json.loads(results[uid])
        print 'user_list:', user_list
        in_date = user_list[0]
        status = user_list[1]
        if status == '1':
            user_list.append(uid)
            mapping_dict[uid] = json.dumps([in_date, '3']) # mark status:2 computing
    print 'mapping_dict:', mapping_dict
    r.hmset('compute', mapping_dict)
    #acquire bulk user weibo data
    #user_weibo_dict = read_user_weibo(user_list)
    #compute text attribute
    #compute_status = compute2in(user_list, user_weibo_dict, status='insert')
    compute_status = False
    if compute_status==True:
        change_status_computed(mapping_dict)

def change_status_computed(mapping_dict):
    hash_name = 'compute'
    status = 4
    new_mapping_dict = {}
    for uid in mapping_dict:
        user_list = mapping_dict[uid]
        user_list[1] = '4'
        new_mapping_dict[uid] = json.dumps(user_list)
    r.hmset(hash_name, new_mapping_dict)

if __name__=='__main__':
    scan_compute_redis()
