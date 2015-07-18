# -*- coding: UTF-8 -*-
'''
use to update the attribute of user portrait
update frequence: one day
update attribute: activeness, importance, influence
'''
import sys
import json
import time
from save_utils import update_day
from evaluate_index import get_evaluate_index
from save_utils import save_user_results
from elasticsearch.helpers import scan
reload(sys)
sys.path.append('../../')
from global_utils import es_user_portrait as es



def update_attribute_day():
    #scan the user_portrait and bulk action to update
    status = False
    results = {}
    count = 0
    index_name = 'user_portrait'
    index_type = 'user'
    s_re = scan(es, query={'query':{'match_all':{}}, 'size':1000}, index=index_name, doc_type=index_type)
    while True:
        bulk_action = []
        while True:
            try:
                scan_re = s_re.next()['_source']
                count += 1
            except StopIteration:
                print 'all done'
                if bulk_action:
                    print 'bulk_action:', bulk_action
                    status = save_user_results(bulk_action)
                    print 'status:', status
                sys.exit(0)
            except Exception, r:
                print Exception, r
                sys.exit(0)
            uid = scan_re['uid']
            user_info = {'uid':uid}
            evaluate_result = get_evaluate_index(user_info, status='update')
            results = {}
            results = dict(results, **evaluate_result)
            action = {'update':{'_id':str(uid)}}
            bulk_action.extend([action, results])
            #print 'bulk_action:', bulk_action
            if count%1000 == 0:
                break
        '''
        print 'bulk_action:', bulk_action
        if bulk_action:
            status = save_user_results(bulk_action)
        '''
    print 'status:', status
    return status


if __name__=='__main__':
    status = update_attribute_day()
    print 'update attribute week status:', status
