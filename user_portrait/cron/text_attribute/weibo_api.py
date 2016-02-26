# -*- coding: UTF-8 -*-
import csv
import time
from cron_text_attribute import test_cron_text_attribute

#read blacklist user list
def read_black_list():
    f = open('/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/text_attribute/black_list.csv', 'rb')
    reader = csv.reader(f)
    item_list = []
    for item in reader:
        if len(item)!= 10:
            item = item[:10]
        item_list.append(item)
    return iten_list


#test: read user weibo
def read_user_weibo():
    user_weibo_dict = dict()
    csvfile = open('/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/text_attribute/uid_text_0728.csv', 'rb')
    reader = csv.reader(csvfile)
    count = 0
    for line in reader:
        count += 1
        '''
        if count>=10:
            break
        '''
        weibo = dict()
        user = line[0]
        weibo['uname'] = 'unknown'
        weibo['text'] = line[1].decode('utf-8')
        weibo['online_pattern'] = 'weibo.com'
        try:
            user_weibo_dict[user].append(weibo)
        except:
            user_weibo_dict[user] = [weibo]
    print 'all count:', len(user_weibo_dict)
    
    iter_count = 0
    iter_weibo_dict = {}
    start_ts = time.time()
    for user in user_weibo_dict:
        iter_count += 1
        iter_weibo_dict[user] = user_weibo_dict[user]
        if iter_count % 100==0:
            status = test_cron_text_attribute(iter_weibo_dict)
            iter_weibo_dict = {}

    if iter_weibo_dict:
        status = test_cron_text_attribute(iter_weibo_dict)
    end_ts = time.time()
    
    print 'all end count:', iter_count
    print 'time_segment:', end_ts - start_ts
    

if __name__=='__main__':
    read_user_weibo()
