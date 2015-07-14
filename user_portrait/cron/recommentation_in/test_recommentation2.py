# -*- coding: UTF-8 -*-
import sys
import csv
import json
import time
reload(sys)
sys.path.append('../../')
from global_utils import R_CLUSTER_FLOW2 as r_cluster
from global_utils import R_1 as r
from time_utils import datetime2ts


def main():
    f = open('/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/recommentation_in/core_list.csv', 'wb')
    writer = csv.writer(f)
    scan_count = 0
    scan_cursor = 0
    all_count = 0
    dis_dict = dict()
    fw_dict = dict()
    n_dict = dict()
    save_list = []
    range_list = [100000,10000,1000,100,0]
    while 1:
        if scan_count == 1000000:
            break
        results = r.scan(scan_cursor, count=1000)
        scan_cursor = results[0]
        scan_count += 1000
        for result in results[1]:
            if 'be_retweet_' == result[:11]:
                uid = result[11:]
                be_retweet_dict = r.hgetall(result)
                be_retweet_user_count = len(be_retweet_dict)
                all_count += be_retweet_user_count
                try:
                    dis_dict[str(be_retweet_user_count)] += 1
                except:
                    dis_dict[str(be_retweet_user_count)] = 1
                if be_retweet_user_count >= 1000:
                    save_list.append((uid, be_retweet_user_count))
    sort_save_list = sorted(save_list, key=lambda x:x[1], reverse=True)
    for item in sort_save_list:
        uid = item[0]
        count = item[1]
        writer.writerow([uid, item])
    
    for rf in dis_dict:
        dis_count = dis_dict[rf]
        for range_up in range_list:
            if int(rf) > range_up:
                try:
                    fw_dict[str(range_up)] += int(rf)
                except:
                    fw_dict[str(range_up)] = int(rf)
                try:
                    n_dict[str(range_up)] += dis_count
                except:
                    n_dict[str(range_up)] = dis_count
    print 'Rf, N, Fw:'
    for range_up in range_list:
        try:
            n = n_dict[str(range_up)]
            fw = fw_dict[str(range_up)]
        except:
            n = 0
            fw = 0
        print range_up, n, fw
    
    f.close()

if __name__=='__main__':
    main()
