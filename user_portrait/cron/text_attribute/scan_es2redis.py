# -*- coding: UTF-8 -*-
'''
use to scan the user_portrait uid, activeness_history and influence_history to redis
for 
'''
import sys
import time
import json
from elasticsearch.helpers import scan

reload(sys)
sys.path.append('../../')
from global_utils import es_user_portrait, portrait_index_name, portrait_index_type
from global_utils import update_day_redis, UPDATE_DAY_REDIS_KEY

def scan_es2redis():
    count = 0
    s_re = scan(es_user_portrait, query={'query':{'match_all':{}}, 'size':1000}, index=portrait_index_name, doc_type=portrait_index_type)
    start_ts = time.time()
    user_list = []
    user_info = {}
    while True:
        try:
            scan_re = s_re.next()['_source']
            count += 1
            uid = scan_re['uid']
            #user_info[uid] = {'activity_geo_dict':scan_re['activity_geo_dict']}
            #test
            user_info[uid] = {'activity_geo_dict':json.dumps([{u'中国\t北京\t北京':1}])}
            update_day_redis.lpush(UPDATE_DAY_REDIS_KEY, json.dumps(user_info))
            user_info = {}
            if count % 1000==0 and count!=0:
                end_ts = time.time()
                print '%s sec count 1000' % (end_ts - start_ts)
                start_ts = end_ts
        except StopIteration:
            print 'all done'
            if user_info:
                update_day_redis.lpush(UPDATE_DAY_REDIS_KEY, json.dumps(user_info))
                user_info = {}
            break
        except Exception, r:
            raise r
            break
    
    if user_info:
        update_day_redis.lpush(UPDATE_DAY_REDIS_KEY, json.dumps(user_info))

    print 'count:', count

if __name__=='__main__':
    scan_es2redis()
