# -*- coding: UTF-8 -*-
import sys
import json
import time
reload(sys)
sys.path.append('../../')
from global_utils import es_user_portrait as es
from time_utils import datetime2ts, ts2datetime
from global_utils import portrait_index_name, portrait_index_type

#test
#portrait_index_type = 'user'
#portrait_index_name = 'user_portrait_0303'

'''
def attr_hash(uid):
    hashtag_results = {}
    now_ts = time.time()
    # test
    now_ts = datetime2ts('2013-09-08')
    date = ts2datetime(now_ts)
    ts = datetime2ts(date)
    for i in range(1,8):
        ts = ts - 24*3600
        result_string = r_cluster.hget('hashtag_'+str(ts), str(uid))
        if result_string:
            result_dict = json.loads(result_string)
            for hashtag in result_dict:
                count = result_dict[hashtag]
                try:
                    hashtag_results[hashtag] += count
                except:
                    hashtag_results[hashtag] = count
    return hashtag_results
'''            

def save_user_results(bulk_action):
    #print 'save utils bulk action len:', len(bulk_action)
    #test
    #print 'bulk_action:', bulk_action
    #portrait_index_name = 'user_portrait_0303'
    #portrait_index_type = 'user'
    es.bulk(bulk_action, index=portrait_index_name, doc_type=portrait_index_type, timeout=600)
    return True    

if __name__=='__main__':
    save_user_results([])
