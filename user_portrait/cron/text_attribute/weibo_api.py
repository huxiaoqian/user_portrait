# -*- coding: UTF-8 -*-
import csv


'''
# read from weibo api
def compute_in(uid_list):
    user_weibo_dict = dict()
    return user_weibo_dict
'''

# test: read user weibo
def read_user_weibo(uid_list):
    user_weibo_dict = dict()
    csvfile = open('/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/text_attribute/uid_text.csv', 'rb')
    reader = csv.reader(csvfile)
    for line in reader:
        weibo = dict()
        user = line[0]
        weibo['uname'] = 'unknown'
        weibo['text'] = line[1].decode('utf-8')
        weibo['online_pattern'] = 'weibo.com'
        try:
            user_weibo_dict[user].append(weibo)
        except:
            user_weibo_dict[user] = [weibo]
            
    return user_weibo_dict
