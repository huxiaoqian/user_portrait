# -*- coding=utf-8 -*-

import re
import zmq
import time
import json
import math
import sys
from datetime import datetime
from DFA_filter import readInputText, createWordTree, searchWord

reload(sys)
sys.path.append('../../')
from global_config import ZMQ_VENT_PORT_FLOW1, ZMQ_CTRL_VENT_PORT_FLOW1, ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_HOST_FLOW1 
from global_utils import  R_CLUSTER_FLOW1

reload(sys)
sys.path.append('../../../../../libsvm-3.17/python/')
from sta_ad import load_scws

sw = load_scws()
cx_list = ['a', 'n', 'nr', 'nz', 'v', '@', 'd']

# deal with sensitive word
def sensitive_word():
    f1 = open('zz.txt', 'rb')
    sensitive_words = set()
    for line in f1:
        line_list = line.split('=')
        word = line_list[0]
        #print 'word:', word, type(word.decode('utf-8'))
        sensitive_words.add(word.decode('utf-8', 'ignore'))
    f1.close()
    return sensitive_words

def deal_text_word(text):
    cut_text = sw.participle(text.encode('utf-8'))
    #cut_text = sw.participle(text)
    text_set = set()
    for item in cut_text:
        text_set.add((item[0]).decode('utf-8', 'ignore'))
    return text_set

def sensitive_test(text):
    cut_text_set = deal_text_word(text)
    sensitive_words = sensitive_word()
    overlap_set = cut_text_set & sensitive_words
    if len(overlap_set) == 0:
        return 0
    else:
        return 1



def get_queue_index(timestamp):
    time_struc = time.gmtime(float(timestamp))
    hour = time_struc.tm_hour
    minute = time_struc.tm_min
    index = hour*4+math.ceil(minute/15.0) #every 15 minutes
    return int(index)

def cal_propage_work(item, sensitive_words):
    cluster_redis = R_CLUSTER_FLOW1
    user = str(item['uid'])
    followers_count = item['user_fansnum']
    friends_count = item.get("user_friendsnum", 0)
    cluster_redis.hset(user, 'user_fansnum', followers_count)
    cluster_redis.hset(user, 'user_friendsnum', friends_count)

    retweeted_uid = str(item['root_uid'])
    retweeted_mid = str(item['root_mid'])

    message_type = int(item['message_type'])
    mid = str(item['mid'])
    timestamp = item['timestamp']
    text = item['text']

    ##sensitive_result = sensitive_test(text)
    sensitive_result = len(searchWord(text.encode('utf-8')))
    #print  sensitive_result
    #sensitive_result = 0
    if message_type == 1:
        cluster_redis.sadd('user_set', user)
        if sensitive_result:
            cluster_redis.hset('s_'+user, mid + '_origin_weibo_timestamp', timestamp)
        else:
            cluster_redis.hset(user, mid + '_origin_weibo_timestamp', timestamp)

    elif message_type == 2: # comment weibo
        cluster_redis.sadd('user_set', user)
        if cluster_redis.sismember(user + '_comment_weibo', retweeted_mid) or cluster_redis.sismember('s_' + user + '_comment_weibo', retweeted_mid):
            return

        #RE = re.compile(u'//@([a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+):', re.UNICODE)
        #nicknames = RE.findall(text)

        if not sensitive_result:
            cluster_redis.sadd(user + '_comment_weibo', retweeted_mid)
            queue_index = get_queue_index(timestamp)
            cluster_redis.hincrby(user, 'comment_weibo', 1)

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
        else:
            cluster_redis.sadd('s_' + user + '_comment_weibo', retweeted_mid)
            queue_index = get_queue_index(timestamp)
            cluster_redis.hincrby('s_'+user, 'comment_weibo', 1)

            if 1:
            #if len(nicknames) == 0:
                cluster_redis.hincrby('s_' + retweeted_uid, retweeted_mid + '_origin_weibo_comment', 1) 
                cluster_redis.hincrby('s_' + retweeted_uid, 'origin_weibo_comment_timestamp_%s' % queue_index, 1)
                cluster_redis.hset('s_' + retweeted_uid, retweeted_mid + '_origin_weibo_comment_timestamp', timestamp)
            """
            else:
                nick_id_ = nicknames[0]
                _id = single_redis.hget(NICK_UID_NAMESPACE, nick_id_)
                print _id
                single_redis.hset(ACTIVE_NICK_UID_NAMESPACE, nick_id_, _id)
                if _id:
                    cluster_redis.hincrby('s_' + str(_id), retweeted_mid + '_retweeted_weibo_comment', 1) 
                    cluster_redis.hincrby('s_' + str(_id), 'retweeted_weibo_comment_timestamp_%s' % queue_index, 1)
                    cluster_redis.hset('s_' + str(_id), retweeted_mid + '_retweeted_weibo_comment_timestamp', timestamp)
            """

    elif message_type == 3:
        cluster_redis.sadd('user_set', user)
        if cluster_redis.sismember(user + '_retweeted_weibo', retweeted_mid) or cluster_redis.sismember('s_' + user + '_retweeted_weibo', retweeted_mid):
            return
        """
        RE = re.compile(u'//@([a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+):', re.UNICODE)
        nicknames = RE.findall(text)
        """
        if not sensitive_result:
            cluster_redis.sadd(user + '_retweeted_weibo', retweeted_mid)
            cluster_redis.hset(user, retweeted_mid + '_retweeted_weibo_timestamp', timestamp) 
            queue_index = get_queue_index(timestamp)
            cluster_redis.hincrby(retweeted_uid, 'origin_weibo_retweeted_timestamp_%s' % queue_index, 1)    
            cluster_redis.hincrby(retweeted_uid, retweeted_mid + '_origin_weibo_retweeted', 1) 
            """
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
        else:
            cluster_redis.sadd('s_' + user + '_retweeted_weibo', retweeted_mid)
            cluster_redis.hset('s_' + user, retweeted_mid + '_retweeted_weibo_timestamp', timestamp)
            queue_index = get_queue_index(timestamp)
            cluster_redis.hincrby('s_' +retweeted_uid, 'origin_weibo_retweeted_timestamp_%s' %queue_index, 1)
            cluster_redis.hincrby('s_' +retweeted_uid, retweeted_mid + '_origin_weibo_retweeted', 1)
            """
            if len(nicknames) != 0:
                for nick_id in nicknames:
                    _id = single_redis.hget(NICK_UID_NAMESPACE, nick_id)
                    print _id
                    single_redis.hset(ACTIVE_NICK_UID_NAMESPACE, nick_id, _id)
                    if _id:
                        cluster_redis.hincrby('s_' + str(_id), retweeted_mid+'_retweeted_weibo_retweeted', 1) 
                        cluster_redis.hset('s_' + str(_id), 'retweeted_weibo_retweeted_timestamp', timestamp)
                        cluster_redis.hincrby('s_' + str(_id), 'retweeted_weibo_retweeted_timestamp_%s' % queue_index, 1)
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

    sensitive_words = createWordTree()

    count = 0
    tb = time.time()
    ts = tb
    while 1:
        item = receiver.recv_json()

        if not item:
            continue 

        if int(item['sp_type']) == 1:
            cal_propage_work(item, sensitive_words)

            count += 1
            if count % 10000 == 0:
                te = time.time()
                print '[%s] cal speed: %s sec/per %s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), te - ts, 10000)
                ts = te

            if count % 100000 == 0:
                print '[%s] total cal %s, cost %s sec [avg %s per/sec]' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), count, te - tb, count / (te - tb)) 
                ts = te
