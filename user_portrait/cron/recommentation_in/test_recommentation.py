# -*- coding: UTF-8 -*-
import sys
import csv
import json
import time
reload(sys)
sys.path.append('../../')
from global_utils import R_CLUSTER_FLOW2 as r_cluster
from global_utils import R_1 as r
from global_utils import R_DICT as r_dict
from global_utils import ES_DAILY_RANK
from global_utils import es_user_portrait
from time_utils import datetime2ts

'''
calculate the fans, followers, weibos of all, verified, top10000
'''

def cal_ave_fans():
    # test there should use r_dict
    scan_count = 0
    scan_cursor = 0
    all_count = 0
    while 1:
        if scan_count == 1000000:
            break
        results = r.scan(scan_cursor, count=1000)
        scan_cursor = results[0]
        scan_count += 1000
        for result in results[1]:
            if 'be_retweet_' == result[:11]:
                uid = result[11:]
                retweet_dict = r.hgetall(result)
                retweet_user_count = len(retweet_dict)
                all_count += retweet_user_count
    ave_count = float(all_count) / scan_count
    print 'ave_count:', ave_count

def cal_ave_weibo():
    date = '2013-09-07'
    timestamp = datetime2ts(date)
    scan_count = 0
    scan_cursor = 0
    all_count = 0
    while 1:
        if scan_count == 1000000:
            break
        results = r_cluster.hscan('activity_'+str(timestamp), scan_cursor, count=1000)
        scan_cursor = results[0]
        scan_count += 1000
        for uid in results[1]:
            for i in range(0,1):
                ts = timestamp - 24*3600*i
                activity_dict_string = r_cluster.hget('activity_'+str(ts), uid)
                if activity_dict_string:
                    activity_dict = json.loads(activity_dict_string)
                    weibo_count = 0
                    for time_seg in activity_dict:
                        weibo_count += int(activity_dict[time_seg])
                    all_count += weibo_count
    ave_count = float(all_count) / scan_count
    print 'ave_count:', ave_count
                 
# {'111':ratio1, '110':ratio}
def cal_class_ratio():
    ratio_results = {}
    date = '2013-09-07'
    ts = datetime2ts(date)
    scan_count = 0
    scan_cursor = 0
    all_count = 0
    while 1:
        if scan_count == 1000000:
            break
        results = r_cluster.hscan('activity_'+str(ts), scan_cursor, count=1000)
        scan_cursor = results[0]
        scan_count += 1000
        for uid in results[1]:
            activity_dict_string = r_cluster.hget('activity_'+str(ts), uid)
            activity_dict = json.loads(activity_dict_string)
            weibo_count = 0
            for time_seg in activity_dict:
                weibo_count += int(activity_dict[time_seg])
            if weibo_count >= 6:
                indic_3 = '1'
            else:
                indic_3 = '0'
            retweet_results = r.hgetall('retweet_'+str(uid))
            retweet_count = len(retweet_results)
            if retweet_count >= 8:
                indic_1 = '1'
            else:
                indic_1 = '0'
            be_retweet_results = r.hgetall('be_retweet_'+str(uid))
            be_retweet_count = len(be_retweet_results)
            #print 'be_retweet_count:', be_retweet_count
            if be_retweet_count >= 9:
                indic_2 = '1'
            else:
                indic_2 = '0'
            #print 'indic_2:', indic_2
            key = indic_1 + indic_2 + indic_3
            try:
                ratio_results[key] += 1
            except:
                ratio_results[key] = 1
            # write eight type users
            '''
            if key=='001':
                writer1.writerow([uid, retweet_count, be_retweet_count, weibo_count])
            elif key=='111':
                writer2.writerow([uid, retweet_count, be_retweet_count, weibo_count])
            elif key=='101':
                writer3.writerow([uid, retweet_count, be_retweet_count, weibo_count])
            elif key=='011':
                writer4.writerow([uid, retweet_count, be_retweet_count, weibo_count])
            elif key=='110':
                writer5.writerow([uid, retweet_count, be_retweet_count, weibo_count])
            if key=='010':
                writer6.writerow([uid, retweet_count, be_retweet_count, weibo_count])
            '''
    print 'ratio_results:', ratio_results

def cal_core_class():
    date = '2013-09-07'
    timestamp = datetime2ts(date)
    f_r = open('/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/recommentation_in/core_list.csv', 'rb')
    reader = csv.reader(f_r)
    f_w = open('/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/recommentation_in/core_class.csv', 'wb')
    writer = csv.writer(f_w)
    result_list = []
    count011 = 0
    for line in reader:
        uid = line[0]
        retweet_results = r.hgetall('retweet_'+str(uid))
        retweet_count = len(retweet_results)
        be_retweet_results = r.hgetall('be_retweet_'+str(uid))
        be_retweet_count = len(be_retweet_results)
        weibo_count = 0
        for i in range(0,7):
            ts = timestamp - 24*3600*i
            activity_string = r_cluster.hget('activity_'+str(ts), str(uid))
            if activity_string:
                activity_dict = json.loads(activity_string)
            else:
                activity_dict = {}
            for time_seg in activity_dict:
                count = activity_dict[time_seg]
                weibo_count += count
        ave_weibo_count = float(weibo_count) / 7
        if retweet_count >= 8:
            indic_1 = '1'
        else:
            indic_1 = '0'
        if be_retweet_count >= 9:
            indic_2 = '1'
        else:
            indic_2 = '0'
        if ave_weibo_count >= 6:
            indic_3 = '1'
        else:
            indic_3 = '0'
        key = indic_1 + indic_2 + indic_3
        if key=='011':
            count011 += 1
        result_list.append([uid, key, retweet_count, be_retweet_count, ave_weibo_count])
    f_r.close()
    sort_result = sorted(result_list, key=lambda x:x[3], reverse=True)
    for item in sort_result:
        writer.writerow(list(item))
    f_w.close()
    print 'count011:', count011

            
if __name__=='__main__':
    #cal_ave_fans()
    #cal_ave_weibo()
    '''
    f1 = open('/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/recommentation_in/user001.csv', 'wb')
    writer1 = csv.writer(f1)
    f2 = open('/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/recommentation_in/user111.csv', 'wb')
    writer2 = csv.writer(f2)
    f3 = open('/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/recommentation_in/user101.csv', 'wb')
    writer3 = csv.writer(f3)
    f4 = open('/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/recommentation_in/user011.csv', 'wb')
    writer4 = csv.writer(f4)
    f5 = open('/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/recommentation_in/user110.csv', 'wb') 
    writer5 = csv.writer(f5)
    f6 = open('/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/recommentation_in/user010.csv', 'wb')
    writer6 = csv.writer(f6)
    
    cal_class_ratio()
    f1.close()
    f2.close()
    f3.close()
    f4.close()
    f5.close()
    f6.close()
    '''
    cal_core_class()
