# -*- coding=utf-8 -*-
'''
use to scan redis(retweet/be_retweet) to insert es
'''
import sys
import time
import json
import redis

reload(sys)
sys.path.append('../../')
from global_utils import es_user_portrait as es
from global_utils import retweet_redis_dict, comment_redis_dict
from global_config import R_BEGIN_TIME
from parameter import DAY
from time_utils import ts2datetime, datetime2ts
from retweet_mappings import retweet_es_mappings, be_retweet_es_mappings

begin_ts = datetime2ts(R_BEGIN_TIME)

#use to get db_number which is needed to es
def get_db_num(timestamp):
    date = ts2datetime(timestamp)
    date_ts = datetime2ts(date)
    db_number = 2 - (((date_ts - begin_ts) / (DAY * 7))) % 2
    #test
    db_number = 1
    return db_number


#use to get db retweet/be_retweet redis to es
def scan_retweet():
    count = 0
    scan_cursor = 0
    now_ts = time.time()
    now_date_ts = datetime2ts(ts2datetime(now_ts))
    #get redis db number
    db_number = get_db_num(now_date_ts)
    #retweet/be_retweet es mappings
    '''
    retweet_es_mappings(str(db_number))
    be_retweet_es_mappings(str(db_number))
    '''
    #get redis db
    retweet_redis = retweet_redis_dict[str(db_number)]
    retweet_bulk_action = []
    be_retweet_bulk_action = []
    start_ts = time.time()
    #retweet count/be_retweet count
    retweet_count = 0
    be_retweet_count = 0
    while True:
        re_scan = retweet_redis.scan(scan_cursor, count=1000)
        re_scan_cursor = re_scan[0]
        '''
        if re_scan_cursor == 0:
            print 'scan finish'
            if retweet_bulk_action != []:
                es.bulk(retweet_bulk_action, index='retweet_'+str(db_number), doc_type='user')
            if be_retweet_bulk_action != []:
                es.bulk(be_retweet_bulk_action, index='be_retweet_'+str(db_number), doc_type='user')
            break
        '''
        for item in re_scan[1]:
            count += 1
            item_list = item.split('_')
            save_dict = {}
            if len(item_list)==2:
                retweet_count += 1
                uid = item_list[1]
                item_result = retweet_redis.hgetall(item)
                save_dict['uid'] = uid
                save_dict['uid_retweet'] = json.dumps(item_result)
                retweet_bulk_action.extend([{'index':{'_id':uid}}, save_dict])
            elif len(item_list)==3:
                be_retweet_count += 1
                uid = item_list[2]
                item_result = retweet_redis.hgetall(item)
                save_dict['uid'] = uid
                save_dict['uid_be_retweet'] = json.dumps(item_result)
                be_retweet_bulk_action.extend([{'index':{'_id':uid}}, save_dict])
        es.bulk(retweet_bulk_action, index='retweet_'+str(db_number), doc_type='user')
        es.bulk(be_retweet_bulk_action, index='be_retweet_'+str(db_number), doc_type='user')
        retweet_bulk_action = []
        be_retweet_bulk_action = []
        end_ts = time.time()
        print '%s sec scan %s count user:', (end_ts - start_ts, count)
        start_ts = end_ts
        scan_cursor = re_scan[0]
        if scan_cursor==0:
            break
    print 'count:', count
    print 'end'


if __name__=='__main__':
    scan_retweet()
