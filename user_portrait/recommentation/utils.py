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
from global_utils import R_RECOMMENTATION as r

def save_uid2compute(uid_list):
    test_date = '2013-09-01'
    hash_name = 'compute'
    status = 0
    for uid in uid_list:
        value_string = [test_date, status]
        r.hset(hash_name, uid, json.dumps(value_string))

if __name__=='__main__':
    #test
    test_uid_list = ['2101413011','1995786393','2132734472','2776631980','2128524603',\
                     '1792702427','2703153040','2787852095','1599102507','1726544024']
    save_uid2compute(test_uid_list)
