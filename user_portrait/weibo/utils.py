#-*- coding:utf-8 -*-
import os
import sys
import json
import time
import leveldb

#from user_portrait.time_utils import ts2datetime, datetime2ts
#from user_portrait.global_config import DEFAULT_LEVELDBPATH

reload(sys)
sys.path.append('../')
from time_utils import ts2datetime, datetime2ts
from global_config import DEFAULT_LEVELDBPATH


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
        print 'leveldb_folder:', leveldb_folder
        if leveldb_folder in file_list:
            leveldb_bucket = dynamic_leveldb(leveldb_folder)
            try:
                user_weibo = leveldb_bucket.Get(str(uid))
                weibo_list = json.loads(user_weibo)
                print 'len weibo_list:', len(weibo_list)
                result.extend(weibo_list)
            except:
                pass
    return result


if __name__=='__main__':
    uid = '2816287692'
    ts = datetime2ts('2013-09-06')
    result = user_weibo_ts(uid, str(ts))
    print 'result:', len(result)
