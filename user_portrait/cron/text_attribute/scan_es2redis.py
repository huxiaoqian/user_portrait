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
from global_utils import update_week_redis, UPDATE_WEEK_REDIS_KEY


#scan es to redis as a queue for update day
#write in version: 15-12-08
#order time task for every day
#data in redis: [{'uid':uid, 'activity_geo_dict':json.dumps([activity_geo_dict])}, {'uid':uid, 'activity_geo_dict':...}]
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


#scan es to redis as a queue for update_week
#write in version: 15-12-08
#order time task for every month
def scan_es2redis_month():
    count = 0
    s_re = scan(es_user_portrait, query={'query':{'match_all': {}}, 'size':1000}, index=portrait_index_name, doc_type=portrait_index_type)
    start_ts = time.time()
    user_list = []
    user_info = {}
    while True:
        try:
            scan_re = s_re.next()['_source']
            count += 1
            uid = scan_re['uid']
            #user_info[uid] = {'psycho_status': scan_re['psycho_status']}
            #test
            user_info[uid] = {'psycho_status':json.dumps({'first':{'posemo':1, 'negemo':2, 'middle':3}, 'second':{'anger':0, 'other':0, 'anx':0, 'sad':0.6}})}
            update_week_redis.lpush(UPDATE_WEEK_REDIS_KEY, json.dumps(user_info))
            user_info = {}
            if count % 1000 == 0 and count != 0:
                end_ts = time.time()
                print '%s sec count 1000' % (end_ts - start_ts)
                start_ts = end_ts
        except StopIteration:
            print 'all done'
            if user_info:
                update_week_redis.lpush(UPDATE_WEEK_REDIS_KEY, json.dumps(user_info))
                user_info = {}
            break
        except Exception, r:
            raise r
            break

    if user_info:
        update_week_redis.lpush(UPDATE_WEEK_REDIS_KEY, json.dumps(user_info))

    print 'count:', count

if __name__=='__main__':
    scan_es2redis()
