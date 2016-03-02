# -*- coding:utf-8 -*-

"""
本程序用于实时监测redis和elasticsearch的状态，如果有数据库挂掉，应当在下个时间段内重启

"""
import subprocess
import sys
import os
import time
reload(sys)
sys.path.append('./../../')
from global_config import redis_path, es_path

def check_redis(p_name):
    cmd = 'ps -ef|grep %s|grep -v "grep"' % p_name
    restart_cmd = 'cd %s && src/redis-server redis.conf' % redis_path
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    (stdoutput, erroutput) = p.communicate()
    val = stdoutput
    if p_name in val:
        print "%s %s running" % (time.ctime(),p_name)
    else:
        os.system(restart_cmd)
        print "%s %s restart" % (time.ctime(), p_name)

def check_elasticsearch(p_name):
    cmd = 'ps -ef|grep %s|grep -v "grep"' % p_name
    restart_cmd = 'cd %s && bin/elasticsearch -Xmx25g -Xms25g -Des.max-open-files=true -d' % es_path
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    (stdoutput, erroutput) = p.communicate()
    if p_name in stdoutput:
        print "%s %s running" % (time.ctime(), p_name)
    else:
        os.system(restart_cmd)
        print "%s %s restart" % (time.ctime(), p_name)

if __name__ == '__main__':


    # test redis running
    check_redis("redis")

    # test elasticsearch running
    check_elasticsearch("elasticsearch")
