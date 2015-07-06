# -*- coding: utf-8 -*-

import redis
from elasticsearch import Elasticsearch
from rediscluster import RedisCluster
from global_config import ZMQ_VENT_PORT_FLOW1, ZMQ_CTRL_VENT_PORT_FLOW1, ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_HOST_FLOW1, BIN_FILE_PATH
from global_config import REDIS_CLUSTER_HOST_FLOW1, REDIS_CLUSTER_PORT_FLOW1,\
                          REDIS_CLUSTER_HOST_FLOW2, REDIS_CLUSTER_PORT_FLOW2,\
                          REDIS_HOST, REDIS_PORT
from global_config import WEIBO_API_HOST, WEIBO_API_PORT
from global_config import USER_PROFILE_ES_HOST, USER_PROFILE_ES_PORT, ES_CLUSTER_HOST_FLOW1, USER_PORTRAIT_ES_HOST, USER_PORTRAIT_ES_PORT

def _default_cluster_redis(host=REDIS_CLUSTER_HOST_FLOW1, port=REDIS_CLUSTER_PORT_FLOW1):
    startup_nodes = [{'host':host, 'port':port}]
    weibo_redis = RedisCluster(startup_nodes = startup_nodes)
    return weibo_redis

R_CLUSTER_FLOW1 = _default_cluster_redis(host=REDIS_CLUSTER_HOST_FLOW1, port=REDIS_CLUSTER_PORT_FLOW1)
R_CLUSTER_FLOW2 = _default_cluster_redis(host=REDIS_CLUSTER_HOST_FLOW2, port=REDIS_CLUSTER_PORT_FLOW2)

def _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=1):
    return redis.StrictRedis(host, port, db)

R_0 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
R_1 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=1)
R_2 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=2)
R_3 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=3)
R_4 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=4)
R_5 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=5)
R_6 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=6)
R_7 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=7)
R_8 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=8)
R_9 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=9)
R_10 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=10)
R_11 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=11)
R_12 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=12)
R_13 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=13)
R_14 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=14)
R_15 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=15)

R_DICT = {'0':R_0, '1':R_1, '2':R_2, '3':R_3, '4':R_4, '5':R_5, '6':R_6, '7':R_7,\
          '8':R_8, '9':R_9, '10':R_10, '11':R_11, '12':R_12, '13':R_13,\
          '14':R_14, '15':R_15}

es_user_profile = Elasticsearch(USER_PROFILE_ES_HOST, timeout = 60)
es_user_portrait = Elasticsearch('%s:%s' % (USER_PORTRAIT_ES_HOST, USER_PORTRAIT_ES_PORT), timeout = 60)


def _default_es_cluster_flow1(host=ES_CLUSTER_HOST_FLOW1):
    es = Elasticsearch(host, timeout=60, retry_on_timeout=True, max_retries=6)
    return es

ES_CLUSTER_FLOW1 = _default_es_cluster_flow1(host=ES_CLUSTER_HOST_FLOW1)

def get_client(api_host=WEIBO_API_HOST, api_port=WEIBO_API_PORT):
    return Client(api_host, api_port)


