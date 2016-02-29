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
from global_utils import retweet_redis_dict, comment_redis_dict, redis_host_list
from global_config import R_BEGIN_TIME
from parameter import DAY
from time_utils import ts2datetime, datetime2ts
from retweet_mappings import retweet_es_mappings, be_retweet_es_mappings

begin_ts = datetime2ts(R_BEGIN_TIME)

error_f = open('/home/ubuntu8/huxiaoqian/user_portrait_151220/user_portrait/user_portrait/cron/flow3/error_file.txt', 'w')

#use to get db_number which is needed to es
def get_db_num(timestamp):
    date = ts2datetime(timestamp)
    date_ts = datetime2ts(date)
    db_number = 2 - (((date_ts - begin_ts) / (DAY * 7))) % 2
    #test
    db_number = 1
    return db_number


def scan_comment():
    count = 0
    scan_cursor = 0
    now_ts = time.time()
    now_date_ts = datetime2ts(ts2datetime(now_ts))
    #get redis db number
    db_number = get_db_num(now_date_ts)
    #comment/be_comment es mappings
    '''
    '''
    #get redis db
    comment_redis = comment_redis_dict[str(db_number)]

    # 1. 判断即将切换的db中是否有数据
    while 1:
        redis_host_list.pop(str(db_number))
        other_db_number = comment_redis_dict[redis_host_list[0]]
        current_dbsize = other_db_number.dbsize()
        if current_dbsize:
            break # 已经开始写入新的db，说明前一天的数据已经写完
        else:
            time.sleep(60)

    # 2. 删除之前的es
    comment_es_mappings(str(db_number))
    be_comment_es_mappings(str(db_number))

    # 3. scan
    comment_bulk_action = []
    be_comment_bulk_action = []
    start_ts = time.time()
    #comment count/be_comment count
    comment_count = 0
    be_comment_count = 0
    while True:
        re_scan = comment_redis.scan(scan_cursor, count=100)
        re_scan_cursor = re_scan[0]
        for item in re_scan[1]:
            count += 1
            item_list = item.split('_')
            save_dict = {}
            if len(item_list)==2:
                comment_count += 1
                uid = item_list[1]
                item_result = comment_redis.hgetall(item)
                save_dict['uid'] = uid
                save_dict['uid_comment'] = json.dumps(item_result)
                comment_bulk_action.extend([{'index':{'_id':uid}}, save_dict])
            '''
            elif len(item_list)==3:
                be_comment_count += 1
                uid = item_list[2]
                item_result = comment_redis.hgetall(item)
                save_dict['uid'] = uid
                save_dict['uid_be_comment'] = json.dumps(item_result)
                be_comment_bulk_action.extend([{'index':{'_id': uid}}, save_dict])
            '''
        try:
            es.bulk(comment_bulk_action, index='1225_comment_'+str(db_number), doc_type='user')
        except:
            index_name = '1225_comment_'+str(db_number)
            split_bulk_action(comment_bulk_action, index_name)
        '''
        try:
            es.bulk(be_comment_bulk_action, index='1225_be_comment_'+str(db_number), doc_type='user')
        except:
            index_name = '1225_be_comment_'+str(db_number)
            split_bulk_action(be_comment_bulk_action, index_name)
        '''
        comment_bulk_action = []
        #be_comment_bulk_action = []
        end_ts = time.time()
        print '%s sec scan %s count user' % (end_ts - start_ts, count)
        start_ts = end_ts
        scan_cursor = re_scan[0]
        if scan_cursor==0:
            break
    print 'count:', count
    print 'end'

    # 4. flush redis
    comment_redis.flushdb()


def split_bulk_action(bulk_action, index_name):
    new_bulk_action = []
    for i in range(0, len(bulk_action)):
        if i % 2 == 0:
            new_bulk_action = [bulk_action[i], bulk_action[i+1]]
            #print 'new_bulk_action:', new_bulk_action
            try:
                es.bulk(new_bulk_action, index=index_name, doc_type='user')
            except:
                error_f.writelines([new_bulk_action[0]['index']['_id'], '\n'])




if __name__=='__main__':
    #scan_retweet()
    scan_comment()
    '''
    bulk_action = [{'index':{'_id': '1234567890'}}, {'test':'test'}, {'index':{'_id':'7894561230'}}, {'test2':'test2'}]
    index_name = 'test_portrait_00'
    split_bulk_action(bulk_action, index_name)
    '''
    error_f.close()
