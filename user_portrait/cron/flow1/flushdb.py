from redis import StrictRedis
from rediscluster import RedisCluster

if __name__ == '__main__':
    for i in [91, 92, 93]:
        for j in [6379, 6380]:
            startup_nodes = [{"host": '219.224.135.%s'%i, "port": '%s'%j}]
            weibo_redis = RedisCluster(startup_nodes = startup_nodes)

            weibo_redis.flushall()
    print "finish flushing!"
    """
    r = StrictRedis(host="219.224.135.97", port="6380", db=1)
    r.set("1","1")
    """

