# -*- coding = utf-8 -*-

import redis
import sys
import time
from rediscluster import RedisCluster

reload(sys)
sys.path.append('../../')
from global_utils import _default_cluster_redis

#weibo_redis = redis.StrictRedis(host='219.224.135.47', port='6379')

weibo_redis = _default_cluster_redis

count = 0
scan_cursor = 0
tb = time.time()
number = weibo_redis.scard("user_set")
print number
"""
re_scan = weibo_redis.sscan('user_set',scan_cursor, count=1000)
ts = time.time()
for item in re_scan[1]:
    weibo_redis.hgetall(item)
te = time.time()
print te-ts

"""
while 1:
    re_scan = weibo_redis.sscan('user_set',scan_cursor, count=10000)
    if re_scan[0] == 0:
        weibo_redis.lpush("user_id", re_scan[1])
        print 'finish'
        break
    else:
        weibo_redis.lpush("user_id", re_scan[1])
        count += 10000
        scan_cursor = re_scan[0]
        if count % 100000 == 0:
            ts = time.time()
            print '%s : %s' %(count, ts - tb)
            tb = ts




