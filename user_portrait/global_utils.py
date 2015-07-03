# -*- coding: utf-8 -*-

import redis
from elasticsearch import Elasticsearch
from rediscluster import RedisCluster
from global_config import REDIS_CLUSTER_HOST_FLOW1, REDIS_CLUSTER_PORT_FLOW1, REDIS_HOST, REDIS_PORT
from global_config import ZMQ_VENT_PORT_FLOW1, ZMQ_CTRL_VENT_PORT_FLOW1, ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_HOST_FLOW1, BIN_FILE_PATH
from global_config import USER_ES_HOST, ES_CLUSTER_HOST_FLOW1

def _default_cluster_redis(host=REDIS_CLUSTER_HOST_FLOW1, port=REDIS_CLUSTER_PORT_FLOW1):
    startup_nodes = [{'host':host, 'port':port}]
    weibo_redis = RedisCluster(startup_nodes = startup_nodes)
    return weibo_redis

def _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=1):
    return redis.StrictRedis(host, port, db)

def _default_es(host=USER_ES_HOST):
    es = Elasticsearch(USER_ES_HOST, timeout = 60)
    return es

def _default_es_cluster_flow1(host=ES_CLUSTER_HOST_FLOW1):
    es = Elsticsearch(host, timeout=60, retry_on_timeout=TRUE, max_retries=6)


