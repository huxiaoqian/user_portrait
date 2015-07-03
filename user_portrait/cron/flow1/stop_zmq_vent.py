# -*- coding: utf-8 -*-

import zmq
import time
import redis
import os
from config import ZMQ_VENT_PORT, ZMQ_CTRL_VENT_PORT, ZMQ_VENT_HOST, ZMQ_CTRL_HOST, REDIS_VENT_HOST, REDIS_VENT_PORT, REDIS_NICK_UID_HOST, REDIS_NICK_UID_PORT, _default_single_redis, _default_cluster_redis, BIN_FILE_PATH

def delete_files():
    localtime = int(time.time())
    print "time to delete files ..."
    count = 0
    file_list = os.listdir(BIN_FILE_PATH)
    for each in file_list:
        file_name = each.split('.')[0]
        file_timestamp = int(file_name.split('_')[0])
        if file_timestamp < localtime:
            os.remove(os.path.join(BIN_FILE_PATH, each))
            count += 1
    print 'we delete %s file at the time %s' %(count, localtime)


if __name__ == "__main__":

    context = zmq.Context()
    cluster_redis = _default_cluster_redis(REDIS_VENT_HOST, REDIS_VENT_PORT)

    controller = context.socket(zmq.PUB)
    controller.bind("tcp://%s:%s" %(ZMQ_CTRL_HOST, ZMQ_CTRL_VENT_PORT))
 
    for i in range(5):
        controller.send("PAUSE")
        # repeat to send to ensure 

    delete_files()
  

