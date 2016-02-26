# -*- coding: UTF-8 -*-
import csv
import time
from cron_text_attribute import test_cron_text_attribute
from user_portrait.parameter import DAY, WEEK,MAX_VALUE
from user_portrait.time_utils import ts2datetime, datetime2ts
from user_portrait.global_utils import es_flow_text, flow_text_index_name_pre, flow_text_index_type

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
    csvfile = open('/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/text_attribute/uid_text.csv', 'rb')
    reader = csv.reader(csvfile)
    count = 0
    for line in reader:
        count += 1
        '''
        if count>20:
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
    for user in user_weibo_dict:
        iter_count += 1
        iter_weibo_dict[user] = user_weibo_dict[user]
        if iter_count % 100==0:
            status = test_cron_text_attribute(iter_weibo_dict)
            iter_weibo_dict = {}

    if iter_weibo_dict:
        status = test_cron_text_attribute(iter_weibo_dict)
    print 'all end count:', iter_count
    

def read_flow_text(uid_list):
    text_result = {}
    now_ts = time.time()
    now_date_ts = datetime2ts(ts2datetime(now_ts))
    #test
    now_date_ts = datetime2ts('2013-09-08')
    start_date_ts = now_date_ts - DAY * WEEK
    for i in range(0,WEEK):
        iter_date_ts = start_date_ts + DAY * i
        flow_text_index_date = ts2datetime(iter_date_ts)
        flow_text_index_name = flow_text_index_name_pre + flow_text_index_date
        print flow_text_index_name
        for uid in uid_list:
            try:
                flow_text_exist = es_flow_text.search(index=flow_text_index_name, doc_type=flow_text_index_type,\
                        body={'query':{'filtered':{'filter':{'terms':{'uid': [uid]}}}}, 'size': MAX_VALUE}, _source=False,  fields=['text','uid','uname'])['hits']['hits']
            except:
                flow_text_exist = []
            uid_text = []
            for flow_text_item in flow_text_exist:
                uid = flow_text_item['fields']['uid'][0]
                text = flow_text_item['fields']['text'][0]
                #uname = flow_text_item['fields']['uname'][0]
                uid_text.append({'text':text,'online_pattern':1})
            text_result[uid] = uid_text
            
    return  text_result
        

if __name__=='__main__':
    #read_user_weibo()
    read_flow_text([2098261223,2991483613])