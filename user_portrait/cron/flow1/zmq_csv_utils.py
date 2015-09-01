# -*- coding:utf-8 -*-

import os
import sys
import zmq
import time
import json
import struct
from datetime import datetime
from csv2json import itemLine2Dict, csv2bin

reload(sys)
sys.path.append('../../')
from global_config import ZMQ_VENT_PORT_FLOW1, ZMQ_CTRL_VENT_PORT_FLOW1,\
                          ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_HOST_FLOW1, BIN_FILE_PATH
sys.path.append('/home/ubuntu8/libsvm-3.17/python')
from sta_ad import start

def load_items_from_bin(bin_path):
    return open(bin_path, 'rb')

def filter_ad(item_list):
    results = start(item_list, 1234)
    filter_set = set()
    for item in results:
        filter_set.add(item[0])
    return filter_set

def send_filter(filter_set, weibo_send, count_send, sender):
    for item in weibo_send:
        if item['mid'] not in filter_set:
            sender.send_json(item)
            count_send += 1
    return count_send

def send_all(f, sender):
    count = 0
    count_send = 0
    tb = time.time()
    ts = tb
    weibo_list = []
    weibo_send = []

    try:
        for line in f:
            weibo_item = itemLine2Dict(line)
            if weibo_item:
                weibo_item_bin = csv2bin(weibo_item)
                if int(weibo_item_bin['sp_type']) != 1:
                    continue
                sender.send_json(weibo_item_bin)
                count += 1

            if count % 10000 == 0:
                te = time.time()
                print '[%s] read csv speed: %s sec/per %s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), te - ts, 10000)
                print '[%s] total send filter weibo %s, cost %s sec [avg %s per/sec]' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), count_send, te - tb, count / (te - tb))
                ts = te
    except:
        print "pass"
    total_cost = time.time() - tb
    return count, total_cost


def send_weibo(sender, total_count=0, total_cost=0):
    """
    send weibo data to zmq_work
    """

    if 1:
        file_list = set(os.listdir(BIN_FILE_PATH))
        print "total file is ", len(file_list)
        for each in file_list:
            if 'csv' in each:
                filename = each.split('.')[0]
                if '%s.csv' % filename in file_list and '%s_yes1.txt' % filename not in file_list:
                    bin_input = load_items_from_bin(os.path.join(BIN_FILE_PATH, each))
                    load_origin_data_func = bin_input
                    tmp_count, tmp_cost = send_all(load_origin_data_func, sender)
                    total_count += tmp_count
                    total_cost += tmp_cost

                    with open(os.path.join(BIN_FILE_PATH, '%s_yes1.txt' % filename), 'w') as fw:
                        fw.write('finish reading' + '\n')

        print 'this scan total deliver %s, cost %s sec' % (total_count, total_cost)
    #except Exception,e:
    #    print Exception, ":", e
   
    return total_count, total_cost
