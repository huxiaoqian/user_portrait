#-*- coding:utf-8 -*-
import os
import sys
import json
import time
import leveldb

from user_portrait.time_utils import ts2datetime, datetime2ts
from user_portrait.global_config import DEFAULT_LEVELDBPATH
from user_portrait.global_utils import es_user_portrait as es
from user_portrait.global_utils import es_user_profile
'''
reload(sys)
sys.path.append('../')
from time_utils import ts2datetime, datetime2ts
from global_config import DEFAULT_LEVELDBPATH
'''

# get user weibo from leveldb
def get_user_weibo(uid):
    result = []
    #use to test
    datestr = '2013-09-02'
    end_ts = datetime2ts(datestr)
    #real way to get datestr and ts_segment
    '''
    now_ts = time.time()
    now_date = ts2datetime(now_ts)
    now_date_ts = datetime2ts(now_date)
    ts_segment = (int((now_ts - now_date_ts) / 3600)) % 24
    end_ts = now_date_ts + ts_segment * 3600
    '''
    file_list = set(os.listdir(DEFAULT_LEVELDBPATH))
    for i in range(24*7, 0, -1):
        ts = end_ts - i * 3600
        datestr = ts2datetime(ts)
        ts_segment = (int((ts - datetime2ts(datestr)) / 3600)) % 24 + 1
        leveldb_folder = datestr + str(ts_segment)
        
        if leveldb_folder in file_list:
            leveldb_bucket = dynamic_leveldb(leveldb_folder)
            try:
                user_weibo = leveldb_bucket.Get(uid)
                weibo_list = json.loads(user_weibo)
                result.extend(weibo_list)
            except:
                pass
            

    return result

# dynamic get leveldb by now ts
def dynamic_leveldb(leveldb_folder):
    leveldb_bucket = leveldb.LevelDB(os.path.join(DEFAULT_LEVELDBPATH+'/', leveldb_folder), block_cache_size=8*(2 << 25), write_buffer_size=8*(2 << 25))
    return leveldb_bucket

# get user weibo by date
def user_weibo_date(uid, date):
    result = []
    file_list = set(os.listdir(DEFAULT_LEVELDBPATH))
    for i in range(1, 25):
        leveldb_folder = date + str(i)
        if leveldb_folder in file_list:
            leveldb_bucket = dynamic_leveldb(leveldb_folder)
            try:
                user_weibo = leveldb_bucket.Get(uid)
                weibo_list = json.loads(user_weibo)
                result.extend(weibo_list)
            except:
                pass
    return result

# get user weibo by ts
def user_weibo_ts(uid, ts):
    result = []
    ts = int(ts)
    file_list = set(os.listdir(DEFAULT_LEVELDBPATH))
    datestr = ts2datetime(ts)
    date_ts = datetime2ts(datestr)
    ts_segment = ((ts - date_ts) / 3600) % 24 + 1
    for i in range(0, 4):
        segment = ts_segment + i
        leveldb_folder = datestr + str(segment)
        #print 'leveldb_folder:', leveldb_folder
        if leveldb_folder in file_list:
            leveldb_bucket = dynamic_leveldb(leveldb_folder)
            try:
                user_weibo = leveldb_bucket.Get(str(uid))
                weibo_list = json.loads(user_weibo)
                #print 'len weibo_list:', len(weibo_list)
                result.extend(weibo_list)
            except:
                pass
    return result

# get group weibo by date
def get_group_weibo(task_name, date):
    group_weibo = []
    #step1 : get group user list by task_name
    group_index_name = 'group_result'
    group_index_type = 'group'
    try:
        group_task = es.get(index=group_index_name, doc_type=group_index_type, id=task_name)['_source']
    except Exception ,e:
        raise e
    user_list = group_task['uid_list']
    #step2: get group user name
    profile_index_name = 'weibo_user'
    profile_index_type = 'user'
    try:
        user_name_result = es_user_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={'ids':user_list})['docs']
    except Exception, e:
        raise e
    #print 'user_name_result:', user_name_result
    #step3 : get group user weibo
    file_list = set(os.listdir(DEFAULT_LEVELDBPATH))
    count = 0
    for user in user_list:
        user_nick_name = user_name_result[count]['_source']['nick_name']
        for i in range(1, 25):
            leveldb_folder = date + str(i)
            if leveldb_folder in file_list:
                leveldb_bucket = dynamic_leveldb(leveldb_folder)
                try:
                    user_weibo = leveldb_bucket.Get(str(user))
                    weibo_list = json.loads(user_weibo)
                    for weibo in weibo_list:
                        weibo['uname'] = user_nick_name
                        group_weibo.append(weibo)
                except:
                    pass
    sort_group_weibo = sorted(group_weibo, key=lambda x:x['timestamp'])
    return sort_group_weibo


if __name__=='__main__':
    uid = '2816287692'
    ts = datetime2ts('2013-09-06')
    result = user_weibo_ts(uid, str(ts))
    print 'result:', len(result)
