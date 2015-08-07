# -*- coding=utf-8 -*-

import re
import sys
import zmq
import time
import json
import math
from datetime import datetime

reload(sys)
sys.path.append('../../')
from time_utils import ts2datetime, datetime2ts
from global_utils import R_CLUSTER_FLOW2 as r_cluster
from global_config import ZMQ_VENT_PORT_FLOW2, ZMQ_CTRL_VENT_PORT_FLOW2,\
                          ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_HOST_FLOW1
from global_config import SENSITIVE_WORDS_PATH

def cal_text_work(item):
    uid = item['uid']
    timestamp = item['timestamp']
    date = ts2datetime(timestamp)
    ts = datetime2ts(date)
    text = item['text']


if __name__ == "__main__":
    """
     receive weibo
    """
    context = zmq.Context()

    receiver = context.socket(zmq.PULL)
    receiver.connect('tcp://%s:%s' %(ZMQ_VENT_HOST_FLOW1, ZMQ_VENT_PORT_FLOW2))

    controller = context.socket(zmq.SUB)
    controller.connect("tcp://%s:%s" %(ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_VENT_PORT_FLOW2))

    count = 0
    tb = time.time()
    ts = tb
    comment_count = 0
    while 1:
        try:
            item = receiver.recv_json()
        except Exception, e:
            print Exception, ":", e 
        if not item:
            continue 
        if item['sp_type'] == '1':
            try:
                if item and (item['message_type']==2):
                    #print 'item:', item
                    #print 'item_text:', item['text'], item['root_uid'], item['root_mid']
                    comment_count += 1
                    cal_text_work(item)
            except:
                pass
        if comment_count>=100:
            break
        count += 1
        if count % 10000 == 0:
            te = time.time()
            print '[%s] cal speed: %s sec/per %s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), te - ts, 10000) 
            #if count % 100000 == 0:
            #    print '[%s] total cal %s, cost %s sec [avg %s per/sec]' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), count, te - tb, count / (te - tb)) 
            ts = te
