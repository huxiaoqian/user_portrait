# -*- coding: utf-8 -*-

import zmq
import time 
import redis
import os
from config import ZMQ_VENT_PORT, ZMQ_CTRL_VENT_PORT, ZMQ_VENT_HOST, ZMQ_CTRL_HOST, REDIS_VENT_HOST, REDIS_VENT_PORT, REDIS_NICK_UID_HOST, REDIS_NICK_UID_PORT, _default_single_redis, _default_cluster_redis, NICK_UID_NAMESPACE,ACTIVE_NICK_UID_NAMESPACE, BIN_FILE_PATH

def delete_files():
    localtime = int(time.time())
    print "time to delete files ..."
    count = 0
    file_list = os.listdir('../weibo')
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

    while True:
        localtime = time.localtime()
        
        if localtime.tm_hour == 0 and localtime.tm_min == 0 and localtime.tm_sec <=30 and localtime.tm_sec >=0:
	        print "ok"
            for i in range(5):
                controller.send("PAUSE")
                delete_files()

        elif localtime.tm_hour == 8 and localtime.tm_min == 0 and localtime.tm_sec >= 0 and  localtime.tm_sec<= 30:
            cluster_redis.flushall()
            for i in range(5):
                controller.send("RESTART")

        elif localtime.tm_hour == 4 and localtime.tm_min == 0 and localtime.tm_sec >= 0 and localtime.tm_sec <= 30:
            count = 0
            scan_cursor = 0
            tb = time.time()
            number = cluster_redis.scard("user_set")
            print number

            while True:
                re_scan = cluster_redis.sscan('user_set',scan_cursor, count=10000)
                if re_scan[0] == 0:
                    cluster_redis.lpush("active_user_id", re_scan[1])
        	        print 'finish'
        	        break
                else:
        	        cluster_redis.lpush("active_user_id", re_scan[1])
        	        count += 10000
        	        scan_cursor = re_scan[0]
        	        if count % 100000 == 0:
            		    ts = time.time()
            		    print '%s : %s' %(count, ts - tb)
            		    tb = ts

        else:
            time.sleep(3)
	


