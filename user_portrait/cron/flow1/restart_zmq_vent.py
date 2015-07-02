# -*- coding: utf-8 -*-

import zmq
import time
import redis
import os
from config import ZMQ_VENT_PORT, ZMQ_CTRL_VENT_PORT, ZMQ_VENT_HOST, ZMQ_CTRL_HOST, REDIS_VENT_HOST, REDIS_VENT_PORT, REDIS_NICK_UID_HOST, REDIS_NICK_UID_PORT, _default_single_redis, _default_cluster_redis, BIN_FILE_PATH

if __name__ == "__main__":

    context = zmq.Context()
    cluster_redis = _default_cluster_redis(REDIS_VENT_HOST, REDIS_VENT_PORT)

    controller = context.socket(zmq.PUB)
    controller.bind("tcp://%s:%s" %(ZMQ_CTRL_HOST, ZMQ_CTRL_VENT_PORT))

    for node in range(91,96):
        for port in [6379, 6380]:
            startup_nodes = [{"host": '219.224.135.%s'%i, "port": '%s'%j}]
            weibo_redis = RedisCluster(startup_nodes = startup_nodes)
            weibo_redis.flushall()
    print "finish flushing"

    for i in range(5):
        controller.send("RESTART")


