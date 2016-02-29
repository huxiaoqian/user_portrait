# -*- coding:utf-8 -*-

import subprocess
import sys
import os
import time


def check_redis(p_name):
    cmd = 'ps -ef|grep %s|grep -v "grep"' % p_name
    restart_cmd = 'cd /home/ubuntu3/huxiaoqian/redis-2.8.13 && src/redis-server redis.conf'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    (stdoutput, erroutput) = p.communicate()
    val = stdoutput
    if p_name in val:
        print "ok - %s process is running" % p_name
    else:
        os.system(restart_cmd)

def check_elasticsearch(p_name):
    cmd = 'ps -ef|grep %s|grep -v "grep"' % p_name
    restart_cmd = 'cd /home/ubuntu3/yuankun/elasticsearch-1.6.0 && bin/elasticsearch -Xmx25g -Xms25g -Des.max-open-files=true -d'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    (stdoutput, erroutput) = p.communicate()
    if p_name in stdoutput:
        print "%s ok - %s process is running" % (time.ctime(), p_name)
    else:
        os.system(restart_cmd)

if __name__ == '__main__':

    # test procedure running
    # 8-24: zmq_vent_weibo.py
    # 8-4: zmq_work_weibo.py
    # 4-8: redis_to_es.py

    # test redis running
    check_redis("redis")

    # test elasticsearch running
    check_elasticsearch("elasticsearch")
