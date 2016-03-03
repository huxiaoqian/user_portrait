# -*- coding:utf-8 -*-
# 删除7天前的过期的redis数据：ip/activity/@;hashtag/sensitive_words;

import sys
import os
import redis
import time
reload(sys)
sys.path.append("../")
from time_utils import ts2datetime, datetime2ts
from global_utils import R_CLUSTER_FLOW2 as r_cluster
from global_utils import R_RECOMMENTATION as r
from parameter import EXPIRE_TIME

def main():
    now_ts = time.time()
    delete_ts = datetime2ts(ts2datetime(now_ts-EXPIRE_TIME))  #待删除的时间戳
    delete_date = ts2datetime(now_ts-EXPIRE_TIME)

    #delete @
    r_cluster.delete("at_"+str(delete_ts))

    #delete ip
    r_cluster.delete('new_ip_'+str(delete_ts))

    #delete activity
    r_cluster.delete('activity_'+str(delete_ts))

    #delete hashtag
    r_cluster.delete('hashtag_'+str(delete_ts))

    #delete sensitive words
    r_cluster.delete('sensitive_'+str(delete_ts))

    #delete recommendation
    r.delete('recomment_'+str(delete_date))

if __name__ == "__main__":
    now_ts = time.time()
    current_path = os.getcwd()
    file_path_redis = os.path.join(current_path, 'delete_redis.py')
    print_log = "&".join([file_path_redis, "start", ts2datetime(now_ts)])
    print print_log

    now_datetime = datetime2ts(ts2datetime(now_ts))
    new_ip_number = r_cluster.hlen('new_ip_'+str(now_datetime))
    new_hashtag_number = r_cluster.hlen('hashtag_'+str(now_datetime))

    #if new_ip_number and new_hashtag_number: # flow2/flow4写入新数据,可以清楚8天前数据
    #    main()

    now_ts = time.time()
    print_log = "&".join([file_path_redis, "end", ts2datetime(now_ts)])
    print print_log


