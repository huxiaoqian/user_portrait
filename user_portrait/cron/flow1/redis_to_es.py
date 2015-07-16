# -*- coding = utf-8 -*-

import redis
import math
import sys
import os
import time
from elasticsearch import Elasticsearch
from index_cal import influence_weibo_cal, user_index_cal, deliver_weibo_brust, activity_weibo, statistic_weibo, expand_index_action 
from rediscluster import RedisCluster

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
        for key in user_info.iterkeys():
            if 'origin_weibo_retweeted_timestamp_' in key:
                origin_weibo_retweeted_timestamp.append(key.split('_')[-1])
            elif 'origin_weibo_comment_timestamp_' in key:
                origin_weibo_comment_timestamp.append(key.split('_')[-1])
            elif 'retweeted_weibo_retweeted_timestamp_' in key:
                retweeted_weibo_retweeted_timestamp.append(key.split('_')[-1])
            elif 'retweeted_weibo_comment_timestamp_' in key:
                retweeted_weibo_comment_timestamp.append(key.split('_')[-1])
            elif '_origin_weibo_timestamp' in key:
                origin_weibo_list.append(key.split('_')[0])
            elif '_retweeted_weibo_timestamp' in key:
                retweeted_weibo_list.append(key.split('_')[0])
            elif '_origin_weibo_retweeted' in key:
                origin_weibo_retweeted_count.append(key.split('_')[0])
            elif '_origin_weibo_comment' in key:
                origin_weibo_comment_count.append(key.split('_')[0])
            elif '_retweeted_weibo_retweeted' in key:
                retweeted_weibo_retweeted_count.append(key.split('_')[0])
            elif '_retweeted_weibo_comment' in key:
                retweeted_weibo_comment_count.append(key.split('_')[0])
            elif 'fansnum' in key:
                user_fansnum = user_info[key]
            elif "user_friendsnum" in key:
                user_friendsnum = user_info[key]
            elif 'comment_weibo' in key:
                comment_weibo_number = user_info[key]
            else:
                print user_info, key

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

        user_id = str(user)
        origin_weibo_retweeted_detail, origin_weibo_retweeted_total_number, origin_weibo_retweeted_top_number, origin_weibo_retweeted_average_number, origin_weibo_top_retweeted_id \
                = statistic_weibo(origin_weibo_retweeted_count, user_info, origin_weibo_list, "_origin_weibo_retweeted")

        origin_weibo_comment_detail, origin_weibo_comment_total_number, origin_weibo_comment_top_number, origin_weibo_comment_average_number, origin_weibo_top_comment_id \
                = statistic_weibo(origin_weibo_comment_count, user_info, origin_weibo_list, "_origin_weibo_comment")

        retweeted_weibo_retweeted_detail, retweeted_weibo_retweeted_total_number, retweeted_weibo_retweeted_top_number, retweeted_weibo_retweeted_average_number, retweeted_weibo_top_retweeted_id \
                = statistic_weibo(retweeted_weibo_retweeted_count, user_info, retweeted_weibo_list, '_retweeted_weibo_retweeted')

        retweeted_weibo_comment_detail, retweeted_weibo_comment_total_number, retweeted_weibo_comment_top_number, retweeted_weibo_comment_average_number, retweeted_weibo_top_comment_id \
                = statistic_weibo(retweeted_weibo_comment_count, user_info, retweeted_weibo_list, '_retweeted_weibo_comment')


        origin_weibo_retweeted_brust= activity_weibo(origin_weibo_retweeted_timestamp, user_info, "origin_weibo_retweeted_timestamp")
        origin_weibo_comment_brust= activity_weibo(origin_weibo_comment_timestamp, user_info, "origin_weibo_comment_timestamp")
        retweeted_weibo_retweeted_brust= activity_weibo(retweeted_weibo_retweeted_timestamp, user_info, "retweeted_weibo_retweeted_timestamp")
        retweeted_weibo_comment_brust= activity_weibo(retweeted_weibo_comment_timestamp, user_info, "retweeted_weibo_comment_timestamp")



        influence_origin_weibo_retweeted = influence_weibo_cal(origin_weibo_retweeted_total_number, origin_weibo_retweeted_average_number, origin_weibo_retweeted_top_number,origin_weibo_retweeted_brust)

        influence_origin_weibo_comment = influence_weibo_cal(origin_weibo_comment_total_number, origin_weibo_comment_average_number, origin_weibo_comment_top_number, origin_weibo_comment_brust)

        influence_retweeted_weibo_retweeted = influence_weibo_cal(retweeted_weibo_retweeted_total_number, retweeted_weibo_retweeted_average_number, retweeted_weibo_retweeted_top_number, retweeted_weibo_retweeted_brust)

        influence_retweeted_weibo_comment = influence_weibo_cal(retweeted_weibo_comment_total_number, retweeted_weibo_comment_average_number, retweeted_weibo_comment_top_number, retweeted_weibo_retweeted_brust)

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
        user_item['origin_weibo_retweeted_top_number'] = origin_weibo_retweeted_top_number
        user_item['origin_weibo_retweeted_brust_average'] = origin_weibo_retweeted_brust[1]
        user_item['origin_weibo_top_retweeted_id'] = origin_weibo_top_retweeted_id
        user_item['origin_weibo_retweeted_brust_n'] = origin_weibo_retweeted_brust[0]
        #user_item['origin_weibo_retweeted_detail'] = origin_weibo_retweeted_detail

        user_item['origin_weibo_comment_total_number'] = origin_weibo_comment_total_number
        user_item['origin_weibo_comment_average_number'] = origin_weibo_comment_average_number
        user_item['origin_weibo_comment_top_number'] = origin_weibo_comment_top_number
        user_item['origin_weibo_comment_brust_n'] = origin_weibo_comment_brust[0]
        user_item['origin_weibo_comment_brust_average'] = origin_weibo_comment_brust[1]
        user_item['origin_weibo_top_comment_id'] = origin_weibo_top_comment_id
        #user_item['origin_weibo_comment_detail'] = origin_weibo_comment_detail

        user_item['retweeted_weibo_retweeted_total_number'] = retweeted_weibo_retweeted_total_number
        user_item['retweeted_weibo_retweeted_average_number'] = retweeted_weibo_retweeted_average_number
        user_item['retweeted_weibo_retweeted_top_number'] = retweeted_weibo_retweeted_top_number
        user_item['retweeted_weibo_retweeted_brust_n'] = retweeted_weibo_retweeted_brust[0]
        user_item['retweeted_weibo_retweeted_brust_average'] = retweeted_weibo_retweeted_brust[1]
        user_item['retweeted_weibo_top_retweeted_id'] = retweeted_weibo_top_retweeted_id
        #user_item['retweeted_weibo_retweeted_detail'] = retweeted_weibo_retweeted_detail

        user_item['retweeted_weibo_comment_total_number'] = retweeted_weibo_comment_total_number
        user_item['retweeted_weibo_comment_average_number'] = retweeted_weibo_comment_average_number
        user_item['retweeted_weibo_comment_top_number'] = retweeted_weibo_comment_top_number
        user_item['retweeted_weibo_comment_brust_n'] = retweeted_weibo_comment_brust[0]
        user_item['retweeted_weibo_comment_brust_average'] = retweeted_weibo_comment_brust[1]
        user_item['retweeted_weibo_top_comment_id'] = retweeted_weibo_top_comment_id
        #user_item['retweeted_weibo_comment_detail'] = retweeted_weibo_comment_detail

        x = expand_index_action(user_item)
        bulk_action.extend([x[0], x[1]])
        count_c += 1
        if count_c % 1000 == 0:
            while True:
                try:
                    es.bulk(bulk_action, index=es_index, doc_type='bci', timeout=30)
                    bulk_action = []
                    break
                except Exception,r:
                    es = ES_CLUSTER_FLOW1
                    print "bulk error"
            print count_c


if __name__ == "__main__":

    es_index = time.strftime("%Y%m%d", time.localtime(time.time()-86400))
    bool = es.indices.exists(index=es_index)
    print bool
    if not bool:
        es.indices.create(index=es_index, ignore=400)

    count = 0
    tb = time.time()
#    print es.nodes.info("node_id=all")
#    print es.cluster.health()

    while 1:
        id_set=[]
        try:
            user_set = cluster_redis.rpop('active_user_id')
            if user_set:
                temp = user_set.split(",")
                for item in temp:
                    user = item.split("'")[1]
                    count += 1
                    id_set.append(user)
                compute(id_set, es)
                print "ok"

                if True:
                    ts = time.time()
                    print "%s : %s" %(count, ts - tb)
                    tb = ts
            else:
                os.system("python update_daily_user_index_rank.py &")
                sys.exit(0)
        except Exception ,r:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + " : " + Exception + " : "+r
            time.sleep(60)

