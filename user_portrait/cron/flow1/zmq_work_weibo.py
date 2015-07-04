# -*- coding=utf-8 -*-

import re
import zmq
import time
import json
import math
import sys
from datetime import datetime

reload(sys)
sys.path.append('../../')
from global_config import ZMQ_VENT_PORT_FLOW1, ZMQ_CTRL_VENT_PORT_FLOW1, ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_HOST_FLOW1 
from global_utils import  R_CLUSTER_FLOW1

"""
single_redis is nickname_to_uid

"""

def get_queue_index(timestamp):
    time_struc = time.gmtime(float(timestamp))
    hour = time_struc.tm_hour
    minute = time_struc.tm_min
    index = hour*4+math.ceil(minute/15.0) #every 15 minutes
    return int(index)

def cal_propage_work(item):
    cluster_redis = R_CLUSTER_FLOW1
    user = str(item['uid'])
    followers_count = item['user_fansnum']
    cluster_redis.hset(user, 'user_fansnum', followers_count)

    retweeted_uid = str(item['root_uid'])
    retweeted_mid = str(item['root_mid'])

    message_type = item['message_type']
    if message_type == 2:
        mid = str(item['mid'][2:])
    else:
        mid = str(item['mid'])

    timestamp = item['timestamp']
    text = item['text']
    if message_type == 1:
        cluster_redis.sadd('user_set', user)
        cluster_redis.hset(user, mid + '_origin_weibo_timestamp', timestamp)

    elif message_type == 2: # comment weibo
        if cluster_redis.sismember(user + '_comment_weibo', retweeted_mid):
            return 
        cluster_redis.sadd(user + '_comment_weibo', retweeted_mid)
        #RE = re.compile(u'//@([a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+):', re.UNICODE)
        #nicknames = RE.findall(text)
        queue_index = get_queue_index(timestamp)

        if 1:
        #if len(nicknames) == 0:
            cluster_redis.hincrby(retweeted_uid, retweeted_mid + '_origin_weibo_comment', 1) 
            cluster_redis.hincrby(retweeted_uid, 'origin_weibo_comment_timestamp_%s' % queue_index, 1)
            cluster_redis.hset(retweeted_uid, retweeted_mid + '_origin_weibo_comment_timestamp', timestamp)
	"""
        else:
            nick_id_ = nicknames[0]
            _id = single_redis.hget(NICK_UID_NAMESPACE, nick_id_)
            print _id
            single_redis.hset(ACTIVE_NICK_UID_NAMESPACE, nick_id_, _id)
            if _id:
                cluster_redis.hincrby(str(_id), retweeted_mid + '_retweeted_weibo_comment', 1) 
                cluster_redis.hincrby(str(_id), 'retweeted_weibo_comment_timestamp_%s' % queue_index, 1)
                cluster_redis.hset(str(_id), retweeted_mid + '_retweeted_weibo_comment_timestamp', timestamp)
	"""
    elif message_type == 3:
        cluster_redis.sadd('user_set', user)
        if cluster_redis.sismember(user + '_retweeted_weibo', retweeted_mid):
            return

        cluster_redis.sadd(user + '_retweeted_weibo', retweeted_mid)
        cluster_redis.hset(user, retweeted_mid + '_retweeted_weibo_timestamp', timestamp) 
        queue_index = get_queue_index(timestamp)
        cluster_redis.hincrby(retweeted_uid, 'origin_weibo_retweeted_timestamp_%s' % queue_index, 1)    
        cluster_redis.hincrby(retweeted_uid, retweeted_mid + '_origin_weibo_retweeted', 1) 
	"""    
        RE = re.compile(u'//@([a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+):', re.UNICODE)
        nicknames = RE.findall(text)
        if len(nicknames) != 0:
            for nick_id in nicknames:
                _id = single_redis.hget(NICK_UID_NAMESPACE, nick_id)
                print _id
                single_redis.hset(ACTIVE_NICK_UID_NAMESPACE, nick_id, _id)
                if _id:
                    cluster_redis.hincrby(str(_id), retweeted_mid+'_retweeted_weibo_retweeted', 1) 
                    cluster_redis.hset(str(_id), 'retweeted_weibo_retweeted_timestamp', timestamp)
                    cluster_redis.hincrby(str(_id), 'retweeted_weibo_retweeted_timestamp_%s' % queue_index, 1)
	"""

if __name__ == "__main__":
    """
     receive weibo
    """
    context = zmq.Context()

    receiver = context.socket(zmq.PULL)
    receiver.connect('tcp://%s:%s' %(ZMQ_VENT_HOST_FLOW1, ZMQ_VENT_PORT_FLOW1))

    controller = context.socket(zmq.SUB)
    controller.connect("tcp://%s:%s" %(ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_VENT_PORT_FLOW1))

    cluster_redis = R_CLUSTER_FLOW1
    

    count = 0
    tb = time.time()
    ts = tb
    while 1:
        try:
            item = receiver.recv_json()
        except Exception, e:
            print Exception, ":", e 
        if not item:
            continue 
        
        if item['sp_type'] == 1:
            try:
                cal_propage_work(item)
            except Exception, r:
                print Exception, r


        count += 1
        if count % 10000 == 0:
            te = time.time()
            print '[%s] cal speed: %s sec/per %s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), te - ts, 10000) 
            if count % 100000 == 0:
                print '[%s] total cal %s, cost %s sec [avg %s per/sec]' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), count, te - tb, count / (te - tb)) 
            ts = te
