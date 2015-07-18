# -*- coding: UTF-8 -*-
'''
update attribute of user portrait one week
update attr: text attribute
update freq: one week
'''
import sys
import time
import json
from save_utils import save_user_results
from weibo_api import read_user_weibo
from cron_text_attribute import compute2in
from elasticsearch.helpers import scan
reload(sys)
sys.path.append('../../')
from global_utils import es_user_portrait as es

def update_atttribute_week():
    # scan the user_portrait and bulk action to update
    status = False
    results = {}
    count = 0
    index_name = 'user_portriat'
    index_type = 'user'
    s_re = scan(es, query={'query':{'match_all':{}}, 'size':1000}, index=index_name, doc_type=index_type)
    while True:
        bulk_action = []
        uid_list = []
        while True:
            try:
                scan_re = s_re.next()['_source']
                count += 1
            except StopIteration:
                print 'all done'
                sys.exit(0)
            except Exception, r:
                print Exception, r
                sys.exit(0)
            uid = scan_re['uid']
            uid_list.append(uid)
            if count%1000==0:
                break
        if uid_list:
            # get user list weibo dict from weibo api
            user_weibo_dict = read_user_weibo(uid_list)
            status = compute2in(uid_list, user_weibo_dict, status='update')
            print 'status:', status
    return status


if __name__=='__main__':
    status = update_attribute_week()
    print 'update week status:', status
