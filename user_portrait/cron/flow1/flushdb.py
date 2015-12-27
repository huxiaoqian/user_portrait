from redis import StrictRedis
from rediscluster import RedisCluster

if __name__ == '__main__':

    startup_nodes = [{"host": '219.224.135.91', "port": "6379"}]
    weibo_redis = RedisCluster(startup_nodes = startup_nodes)
    weibo_redis.flushall()

    startup_nodes = [{"host": '219.224.135.91', "port": "6380"}]
    weibo_redis = RedisCluster(startup_nodes = startup_nodes)
    weibo_redis.flushall()

    startup_nodes = [{"host": '219.224.135.93', "port": "6380"}]
    weibo_redis = RedisCluster(startup_nodes = startup_nodes)
    weibo_redis.flushall()

    print "finish flushing!"
    """
    r = StrictRedis(host="219.224.135.97", port="6380", db=1)
    r.set("1","1")

    startup_nodes = [{"host": '219.224.135.94', "port": '6379'}]
    r =  RedisCluster(startup_nodes = startup_nodes)
    print r.hgetall('ip_1378224000')
    """
