# -*- coding=utf-8 -*-

import redis
import math
import json
import sys
import os
import time
from elasticsearch import Elasticsearch
from index_cal import influence_weibo_cal, user_index_cal, deliver_weibo_brust, activity_weibo, statistic_weibo, expand_index_action 
from rediscluster import RedisCluster
from bci_mappings import mappings

reload(sys)
sys.path.append('../../')
from global_utils import  ES_CLUSTER_FLOW1, R_CLUSTER_FLOW1

es = ES_CLUSTER_FLOW1
cluster_redis = R_CLUSTER_FLOW1

def compute(user_set, es):
    bulk_action = []
    count_c = 0
    
    weibo_redis = R_CLUSTER_FLOW1
    for user in user_set:
        user_info = weibo_redis.hgetall(user)#dict
        origin_weibo_retweeted_timestamp = []
        origin_weibo_retweeted_count = []
        origin_weibo_list = []
        origin_weibo_comment_timestamp = []
        origin_weibo_comment_count = []
        retweeted_weibo_retweeted_count = []
        retweeted_weibo_comment_count= []
        retweeted_weibo_retweeted_timestamp = []
        retweeted_weibo_comment_timestamp = []
        retweeted_weibo_list = []
        user_fansnum = 0
        comment_weibo_number = 0
        user_friendsnum = 0
        origin_weibo_list = list(weibo_redis.smembers(user+'_origin_weibo'))
        retweeted_weibo_list = list(weibo_redis.smembers(user+'_retweeted_weibo'))
        for key in user_info.keys():
            if 'origin_weibo_retweeted_timestamp_' in key: # 不同时间段的原创微博被转发的爆发度
                origin_weibo_retweeted_timestamp.append(key.split('_')[-1])
            elif 'origin_weibo_comment_timestamp_' in key: # 不同时间段的原创微博被评论的爆发度
                origin_weibo_comment_timestamp.append(key.split('_')[-1])
            elif 'retweeted_weibo_retweeted_timestamp_' in key:# 不同时间段的转发微博被转发的爆发度
                retweeted_weibo_retweeted_timestamp.append(key.split('_')[-1])
            elif 'retweeted_weibo_comment_timestamp_' in key: # 不同时间段的转发微博被评论的爆发度
                retweeted_weibo_comment_timestamp.append(key.split('_')[-1])
            elif '_origin_weibo_retweeted' in key: # which origin weibo is retweeted, and retwweted number
                origin_weibo_retweeted_count.append(key.split('_')[0]) # origin weibo list
            elif '_origin_weibo_comment' in key: # which origin weibo is commentted, and comment number
                origin_weibo_comment_count.append(key.split('_')[0])
            elif '_retweeted_weibo_retweeted' in key: # which retweeted weibo is retweeted, and retweeted number
                retweeted_weibo_retweeted_count.append(key.split('_')[0]) # which retweeted weibo
            elif '_retweeted_weibo_comment' in key: # which retweeted weibo is commented, and comment number
                retweeted_weibo_comment_count.append(key.split('_')[0])
            elif 'fansnum' in key:
                user_fansnum = user_info[key]
            elif "user_friendsnum" in key:
                user_friendsnum = user_info[key]
            elif 'comment_weibo' == key:
                comment_weibo_number = int(user_info[key])
            elif "_origin_weibo_timestamp" in key:
                pass
            else:
                print user_info
                print key
                print user
        """
        user_origin_weibo_timestamp = [] 
        if len(origin_weibo_list):
            for i in range(len(origin_weibo_list)):
                timestamp = user_info[str(origin_weibo_list[i])+'_origin_weibo_timestamp']
                user_origin_weibo_timestamp.append(timestamp)


        user_retweeted_weibo_timestamp = [] 
        if len(retweeted_weibo_list):
            for i in range(len(retweeted_weibo_list)):
                timestamp = user_info[str(retweeted_weibo_list[i])+'_retweeted_weibo_timestamp']
                user_retweeted_weibo_timestamp.append(timestamp)
        """
        user_id = str(user)
        origin_weibo_retweeted_detail, origin_weibo_retweeted_total_number, origin_weibo_retweeted_top, origin_weibo_retweeted_average_number \
                = statistic_weibo(origin_weibo_retweeted_count, user_info, "_origin_weibo_retweeted")

        origin_weibo_comment_detail, origin_weibo_comment_total_number, origin_weibo_comment_top, origin_weibo_comment_average_number\
                = statistic_weibo(origin_weibo_comment_count, user_info, "_origin_weibo_comment")

        retweeted_weibo_retweeted_detail, retweeted_weibo_retweeted_total_number, retweeted_weibo_retweeted_top, retweeted_weibo_retweeted_average_number \
                = statistic_weibo(retweeted_weibo_retweeted_count, user_info,  '_retweeted_weibo_retweeted')

        retweeted_weibo_comment_detail, retweeted_weibo_comment_total_number, retweeted_weibo_comment_top, retweeted_weibo_comment_average_number\
                = statistic_weibo(retweeted_weibo_comment_count, user_info, '_retweeted_weibo_comment')


        origin_weibo_retweeted_brust= activity_weibo(origin_weibo_retweeted_timestamp, user_info, "origin_weibo_retweeted_timestamp")
        origin_weibo_comment_brust= activity_weibo(origin_weibo_comment_timestamp, user_info, "origin_weibo_comment_timestamp")
        retweeted_weibo_retweeted_brust= activity_weibo(retweeted_weibo_retweeted_timestamp, user_info, "retweeted_weibo_retweeted_timestamp")
        retweeted_weibo_comment_brust= activity_weibo(retweeted_weibo_comment_timestamp, user_info, "retweeted_weibo_comment_timestamp")



        influence_origin_weibo_retweeted = influence_weibo_cal(origin_weibo_retweeted_total_number, origin_weibo_retweeted_average_number, origin_weibo_retweeted_top[0][1],origin_weibo_retweeted_brust)

        influence_origin_weibo_comment = influence_weibo_cal(origin_weibo_comment_total_number, origin_weibo_comment_average_number, origin_weibo_comment_top[0][1], origin_weibo_comment_brust)

        influence_retweeted_weibo_retweeted = influence_weibo_cal(retweeted_weibo_retweeted_total_number, retweeted_weibo_retweeted_average_number, retweeted_weibo_retweeted_top[0][1], retweeted_weibo_retweeted_brust)

        influence_retweeted_weibo_comment = influence_weibo_cal(retweeted_weibo_comment_total_number, retweeted_weibo_comment_average_number, retweeted_weibo_comment_top[0][1], retweeted_weibo_retweeted_brust)

        user_index = user_index_cal(origin_weibo_list, retweeted_weibo_list, user_fansnum, influence_origin_weibo_retweeted, influence_origin_weibo_comment, influence_retweeted_weibo_retweeted, influence_retweeted_weibo_comment)


        user_item = {}
        user_item['user_index'] = user_index
        user_item['user'] = user
        user_item['user_fansnum'] = user_fansnum
        user_item["user_friendsnum"] = user_friendsnum
        user_item['origin_weibo_number'] = len(origin_weibo_list)
        user_item['comment_weibo_number'] = comment_weibo_number
        user_item['retweeted_weibo_number'] = len(retweeted_weibo_list)

        user_item['origin_weibo_retweeted_total_number'] = origin_weibo_retweeted_total_number
        user_item['origin_weibo_retweeted_average_number'] = origin_weibo_retweeted_average_number
        user_item['origin_weibo_retweeted_top_number'] = origin_weibo_retweeted_top[0][1]
        user_item['origin_weibo_retweeted_top'] = json.dumps(origin_weibo_retweeted_top)
        user_item['origin_weibo_retweeted_brust_average'] = origin_weibo_retweeted_brust[1]
        user_item['origin_weibo_top_retweeted_id'] = origin_weibo_retweeted_top[0][0]
        user_item['origin_weibo_retweeted_brust_n'] = origin_weibo_retweeted_brust[0]
        user_item['origin_weibo_retweeted_detail'] = json.dumps(origin_weibo_retweeted_detail)

        user_item['origin_weibo_comment_total_number'] = origin_weibo_comment_total_number
        user_item['origin_weibo_comment_average_number'] = origin_weibo_comment_average_number
        user_item['origin_weibo_comment_top_number'] = origin_weibo_comment_top[0][1]
        user_item['origin_weibo_comment_top'] = json.dumps(origin_weibo_comment_top)
        user_item['origin_weibo_comment_brust_n'] = origin_weibo_comment_brust[0]
        user_item['origin_weibo_comment_brust_average'] = origin_weibo_comment_brust[1]
        user_item['origin_weibo_top_comment_id'] = origin_weibo_comment_top[0][0]
        user_item['origin_weibo_comment_detail'] = json.dumps(origin_weibo_comment_detail)

        user_item['retweeted_weibo_retweeted_total_number'] = retweeted_weibo_retweeted_total_number
        user_item['retweeted_weibo_retweeted_average_number'] = retweeted_weibo_retweeted_average_number
        user_item['retweeted_weibo_retweeted_top_number'] = retweeted_weibo_retweeted_top[0][1]
        user_item['retweeted_weibo_retweeted_top'] = json.dumps(retweeted_weibo_retweeted_top)
        user_item['retweeted_weibo_retweeted_brust_n'] = retweeted_weibo_retweeted_brust[0]
        user_item['retweeted_weibo_retweeted_brust_average'] = retweeted_weibo_retweeted_brust[1]
        user_item['retweeted_weibo_top_retweeted_id'] = retweeted_weibo_retweeted_top[0][0]
        user_item['retweeted_weibo_retweeted_detail'] = json.dumps(retweeted_weibo_retweeted_detail)

        user_item['retweeted_weibo_comment_total_number'] = retweeted_weibo_comment_total_number
        user_item['retweeted_weibo_comment_average_number'] = retweeted_weibo_comment_average_number
        user_item['retweeted_weibo_comment_top_number'] = retweeted_weibo_comment_top[0][1]
        user_item['retweeted_weibo_comment_top'] = json.dumps(retweeted_weibo_comment_top)
        user_item['retweeted_weibo_comment_brust_n'] = retweeted_weibo_comment_brust[0]
        user_item['retweeted_weibo_comment_brust_average'] = retweeted_weibo_comment_brust[1]
        user_item['retweeted_weibo_top_comment_id'] = retweeted_weibo_comment_top[0][0]
        user_item['retweeted_weibo_comment_detail'] = json.dumps(retweeted_weibo_comment_detail)

        x = expand_index_action(user_item)
        bulk_action.extend([x[0], x[1]])
        count_c += 1
        if count_c % 1000 == 0:
            es.bulk(bulk_action, index=es_index, doc_type='bci', timeout=30)
            bulk_action = []
            print count_c


if __name__ == "__main__":

    es_index = time.strftime("%Y%m%d", time.localtime(time.time()-86400))
    es_index = "20130905"
    es_index = "bci_"+es_index
    bool = es.indices.exists(index=es_index)
    print bool
    if not bool:
        mappings(es, es_index)

    count = 0
    tb = time.time()

    while 1:
        id_set=[]
        if 1:
            user_set = cluster_redis.rpop('active_user_id')
            if user_set:
                temp = json.loads(user_set)
                compute(temp, es)
                count += 10000

                if True:
                    ts = time.time()
                    print "%s : %s" %(count, ts - tb)
                    tb = ts
            else:
                print "total_count : %s "  %count
                #os.system("python update_daily_user_index_rank.py &")
                break

