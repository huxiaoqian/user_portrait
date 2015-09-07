# -*- coding=utf-8 -*-

import re
import sys
import zmq
import time
import json
import math
import leveldb
from datetime import datetime
from portrait2redis import read_portrait2ram
reload(sys)
sys.path.append('../../')
from time_utils import ts2datetime, datetime2ts
from global_config import ZMQ_VENT_PORT_FLOW5, ZMQ_CTRL_VENT_PORT_FLOW5,\
                          ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_HOST_FLOW1, DEFAULT_LEVELDBPATH


# init a new leveldb by hour
def init_leveldb(leveldb_folder):
    leveldb_bucket = leveldb.LevelDB(os.path.join(DEFAULT_LEVELDBPATH, leveldb_folder), block_cache_size=8*(2 << 25), write_buffer_size=8*(2 << 25))
    return leveldb_bucket


# delete leveldb to keep 7 day data
def delete_leveldb(date_timestamp, ts_segment):
    del_date_timestamp = date_timestamp - 7*3600*24
    del_date = ts2datetime(del_date_timestamp)
    del_ts_segment = ts_segment
    del_leveldb_folder = del_date + str(del_ts_segment)
    try:
        os.remove(os.path.join(DEFAULT_LEVELDBPATH, del_leveldb_folder))
    except:
        print 'not need delete'


# write weibo to leveldb
def write2leveldb(item, user_portrait_weibo_leveldb):
    uid = item['uid']
    try:
        key_result = user_portrait_weibo_leveldb.Get(str(uid))
    except:
        user_portrait_weibo_leveldb.Put(uid, json.dumps([item]))
    if key_result != '':
        weibo_list = json.loads(key_result)
        weibo_list.append(item)
        user_portrait_weibo_leveldb.Put(str(uid), json.dumps(weibo_list))

if __name__ == "__main__":
    """
     receive weibo
    """
    context = zmq.Context()

    receiver = context.socket(zmq.PULL)
    receiver.connect('tcp://%s:%s' %(ZMQ_VENT_HOST_FLOW1, ZMQ_VENT_PORT_FLOW5))

    controller = context.socket(zmq.SUB)
    controller.connect("tcp://%s:%s" %(ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_VENT_PORT_FLOW5))

    count = 0
    tb = time.time()
    ts = tb
    
    #scan the suer_portrait user list
    user_list = read_portrait2ram()
    
    #mark previous leveldb path
    pre_leveldb_folder = ''
    user_portrait_weibo_leveldb = leveldb.LevelDB(os.path.join(DEFAULT_LEVELDBPATH, 'default_db'), block_cache_size=8*(2 << 25), write_buffer_size=8*(2 << 25))

    while 1:
        try:
            item = receiver.recv_json()
        except Exception, e:
            print Exception, ":", e 
        if not item:
            continue 
        
        if item['sp_type'] == '1' and item['uid'] in user_list:
            weibo_timestamp = item['timestamp']
            weibo_date = ts2datetime(weibo_timestamp)
            date_timestamp = datetime2ts(weibo_date)
            ts_segment = ((weibo_timestamp - date_timestamp) / 3600) % 24 + 1
            leveldb_folder = weibo_date + str(ts_segment) # 201309011-2013090124
            if leveldb_folder != pre_leveldb_folder:
                user_portrait_weibo_leveldb = init_leveldb(leveldb_folder)
                delete_leveldb(date_timestamp, ts_segment)
                pre_leveldb_folder = leveldb_folder
            write2leveldb(item, user_portrait_weibo_leveldb)
        
        count += 1
        if count % 10000 == 0:
            te = time.time()
            print '[%s] cal speed: %s sec/per %s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), te - ts, 10000) 
            if count % 100000 == 0:
                print '[%s] total cal %s, cost %s sec [avg %s per/sec]' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), count, te - tb, count / (te - tb)) 
            ts = te
