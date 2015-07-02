# -*- coding = utf-8 -*-

import redis
import math
import logging
import time
from elasticsearch import Elasticsearch
from config import REDIS_HOST, REDIS_VENT_PORT, _default_cluster_redis
from index_cal import influence_weibo_cal, user_index_cal
from rediscluster import RedisCluster

def deliver_weibo_brust(time_list, division=900, percent=0.5): 
    time_list = [int(value) for value in time_list]
    max_value = max(time_list)
    if max_value <= 100:
        return 0, 0
    else:
        list_brust = [value for value in time_list if value >= percent*max_value]
        brust_time = len(list_brust) 
        brust_velosity = sum(list_brust)/float(brust_time) 
        return brust_time, brust_velosity

def activity_origin_weibo_retweeted(origin_weibo_retweeted_timestamp, user_info):
    user_origin_weibo_retweeted_timestamp = [0]*96
    if origin_weibo_retweeted_timestamp != []:
        for i in origin_weibo_retweeted_timestamp:
            count = user_info['origin_weibo_retweeted_timestamp_%s' %i]
            user_origin_weibo_retweeted_timestamp[int(i)-1] = count
    origin_weibo_retweeted_brust = deliver_weibo_brust(user_origin_weibo_retweeted_timestamp)
    return origin_weibo_retweeted_brust


def activity_retweeted_weibo_retweeted(retweeted_weibo_retweeted_timestamp, user_info):
    user_retweeted_weibo_retweeted_timestamp = [0]*96
    if retweeted_weibo_retweeted_timestamp != []:
        for i in retweeted_weibo_retweeted_timestamp:
            count = user_info['retweeted_weibo_retweeted_timestamp_%s' %i]
            user_retweeted_weibo_retweeted_timestamp[int(i)-1] = count
    retweeted_weibo_retweeted_brust = deliver_weibo_brust(user_retweeted_weibo_retweeted_timestamp)
    return retweeted_weibo_retweeted_brust


def activity_origin_weibo_comment(origin_weibo_comment_timestamp, user_info):
    user_origin_weibo_comment_timestamp = [0]*96
    if origin_weibo_comment_timestamp != []:
        for i in origin_weibo_comment_timestamp:
            count = user_info['origin_weibo_comment_timestamp_%s' %i]
            user_origin_weibo_comment_timestamp[int(i)-1] = count
    origin_weibo_comment_brust = deliver_weibo_brust(user_origin_weibo_comment_timestamp)
    return origin_weibo_comment_brust


def activity_retweeted_weibo_comment(retweeted_weibo_comment_timestamp, user_info):
    user_retweeted_weibo_comment_timestamp = [0]*96
    if retweeted_weibo_comment_timestamp != []:
        for i in retweeted_weibo_comment_timestamp:
            count = user_info['retweeted_weibo_comment_timestamp_%s' %i]
            user_retweeted_weibo_comment_timestamp[int(i)-1]= count
    retweeted_weibo_comment_brust = deliver_weibo_brust(user_retweeted_weibo_comment_timestamp)
    return retweeted_weibo_comment_brust 

def statis_origin_weibo_retweeted(origin_weibo_retweeted_count,user_info,origin_weibo_list,total_number=0, top_retweeted=0,average_number=0):
    origin_weibo_retweeted_detail = {}
    origin_weibo_top_retweeted_id = 0
    if len(origin_weibo_retweeted_count) != 0:
        for origin_weibo_id in origin_weibo_retweeted_count:
            origin_weibo_id = str(origin_weibo_id)
            origin_weibo_retweeted_detail[origin_weibo_id] = int(user_info[origin_weibo_id+'_origin_weibo_retweeted'])
            if top_retweeted < origin_weibo_retweeted_detail[origin_weibo_id]:
                origin_weibo_top_retweeted_id = origin_weibo_id
            top_retweeted = max(top_retweeted, origin_weibo_retweeted_detail[origin_weibo_id])
            total_number += int(origin_weibo_retweeted_detail[origin_weibo_id])
        try:
            average_number = float(total_number) / len(origin_weibo_list)
        except:
            average_number = float(total_number) / len(origin_weibo_retweeted_count)

    return origin_weibo_retweeted_detail, total_number, top_retweeted, average_number,origin_weibo_top_retweeted_id


def statis_origin_weibo_comment(origin_weibo_comment_count, user_info, origin_weibo_list, total_number=0, top_comment=0,average_number=0):
    origin_weibo_comment_detail = {}
    origin_weibo_top_comment_id = 0
    if len(origin_weibo_comment_count) != 0:
        for origin_weibo_id in origin_weibo_comment_count:
            origin_weibo_id = str(origin_weibo_id)
            origin_weibo_comment_detail[origin_weibo_id] = int(user_info[origin_weibo_id+'_origin_weibo_comment'])
            if top_comment < origin_weibo_comment_detail[origin_weibo_id]:
                origin_weibo_top_comment_id = origin_weibo_id
            top_comment = max(origin_weibo_comment_detail[origin_weibo_id], top_comment)
            total_number += int(origin_weibo_comment_detail[origin_weibo_id])
        try:
            average_number = float(total_number) / len(origin_weibo_list)
        except:
            average_number = float(total_number) / len(origin_weibo_comment_count)
    return origin_weibo_comment_detail, total_number, top_comment, average_number,origin_weibo_top_comment_id


def statis_retweeted_weibo_retweeted(retweeted_weibo_retweeted_count, user_info,retweeted_weibo_list, total_number=0, top_retweeted=0,average_number=0):
    retweeted_weibo_retweeted_detail = {}
    retweeted_weibo_top_retweeted_id = 0
    if len(retweeted_weibo_retweeted_count) !=0:
        for retweeted_weibo_id in retweeted_weibo_retweeted_count:
            retweeted_weibo_id = str(retweeted_weibo_id)
            retweeted_weibo_retweeted_detail[retweeted_weibo_id] = int(user_info[retweeted_weibo_id+'_retweeted_weibo_retweeted'])
            if top_retweeted < retweeted_weibo_retweeted_detail[retweeted_weibo_id]:
                retweeted_weibo_top_retweeted_id = retweeted_weibo_id
            top_retweeted = max(top_retweeted, retweeted_weibo_retweeted_detail[retweeted_weibo_id])
            total_number += int(retweeted_weibo_retweeted_detail[retweeted_weibo_id])                
        try:
            average_number = float(total_number) / len(retweeted_weibo_list)
        except:
            average_number = float(total_number) / len(retweeted_weibo_retweeted_count)
    return retweeted_weibo_retweeted_detail, total_number, top_retweeted, average_number,retweeted_weibo_top_retweeted_id


def statis_retweeted_weibo_comment(retweeted_weibo_comment_count, user_info, retweeted_weibo_list,total_number=0, top_comment=0,average_number=0):
    retweeted_weibo_comment_detail = {}
    retweeted_weibo_top_comment_id = 0
    if len(retweeted_weibo_comment_count) != 0:
        for retweeted_weibo_id in retweeted_weibo_comment_count:
            retweeted_weibo_id = str(retweeted_weibo_id)
            retweeted_weibo_comment_detail[retweeted_weibo_id] = int(user_info[retweeted_weibo_id+'_retweeted_weibo_comment'])
            if top_comment < retweeted_weibo_comment_detail[retweeted_weibo_id]:
                retweeted_weibo_top_comment_id = retweeted_weibo_id
            top_comment = max(retweeted_weibo_comment_detail[retweeted_weibo_id], top_comment)
            total_number += int(retweeted_weibo_comment_detail[retweeted_weibo_id])
        try:
            average_number = float(total_number) / len(retweeted_weibo_list)
        except:
            average_number = float(total_number) / len(retweeted_weibo_comment_count)
    return retweeted_weibo_comment_detail, total_number, top_comment, average_number,retweeted_weibo_top_comment_id


def expand_index_action(data):
    _id = data['user']
    action = {'index': {"_id": _id}}
    return action, data

def compute(user_set):
    bulk_action = []
    count_c = 0
    
    startup_nodes = [{"host": REDIS_VENT_HOST, "port": REDIS_VENT_PORT}]
    weibo_redis = RedisCluster(startup_nodes = startup_nodes)
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
        origin_weibo_retweeted_detail, origin_weibo_retweeted_total_number, origin_weibo_retweeted_top_number, origin_weibo_retweeted_average_number, origin_weibo_top_retweeted_id=statis_origin_weibo_retweeted(origin_weibo_retweeted_count, user_info, origin_weibo_list)

        origin_weibo_comment_detail, origin_weibo_comment_total_number, origin_weibo_comment_top_number, origin_weibo_comment_average_number, origin_weibo_top_comment_id=statis_origin_weibo_comment(origin_weibo_comment_count, user_info, origin_weibo_list)

        retweeted_weibo_retweeted_detail, retweeted_weibo_retweeted_total_number, retweeted_weibo_retweeted_top_number, retweeted_weibo_retweeted_average_number, retweeted_weibo_top_retweeted_id=statis_retweeted_weibo_retweeted(retweeted_weibo_retweeted_count, user_info, retweeted_weibo_list)

        retweeted_weibo_comment_detail, retweeted_weibo_comment_total_number, retweeted_weibo_comment_top_number, retweeted_weibo_comment_average_number, retweeted_weibo_top_comment_id=statis_retweeted_weibo_comment(retweeted_weibo_comment_count, user_info, retweeted_weibo_list)


        origin_weibo_retweeted_brust= activity_origin_weibo_retweeted(origin_weibo_retweeted_timestamp, user_info)
        origin_weibo_comment_brust= activity_origin_weibo_comment(origin_weibo_comment_timestamp, user_info)
        retweeted_weibo_retweeted_brust= activity_retweeted_weibo_retweeted(retweeted_weibo_retweeted_timestamp, user_info)
        retweeted_weibo_comment_brust= activity_retweeted_weibo_comment(retweeted_weibo_comment_timestamp, user_info)



        influence_origin_weibo_retweeted = influence_weibo_cal(origin_weibo_retweeted_total_number, origin_weibo_retweeted_average_number, origin_weibo_retweeted_top_number,origin_weibo_retweeted_brust)

        influence_origin_weibo_comment = influence_weibo_cal(origin_weibo_comment_total_number, origin_weibo_comment_average_number, origin_weibo_comment_top_number, origin_weibo_comment_brust)

        influence_retweeted_weibo_retweeted = influence_weibo_cal(retweeted_weibo_retweeted_total_number, retweeted_weibo_retweeted_average_number, retweeted_weibo_retweeted_top_number, retweeted_weibo_retweeted_brust)

        influence_retweeted_weibo_comment = influence_weibo_cal(retweeted_weibo_comment_total_number, retweeted_weibo_comment_average_number, retweeted_weibo_comment_top_number, retweeted_weibo_retweeted_brust)

        user_index = user_index_cal(origin_weibo_list, retweeted_weibo_list, user_fansnum, influence_origin_weibo_retweeted, influence_origin_weibo_comment, influence_retweeted_weibo_retweeted, influence_retweeted_weibo_comment)


        user_item = {}
        user_item['user_index'] = user_index
        user_item['user'] = user
        user_item['user_fansnum'] = user_fansnum
        user_item['origin_weibo_number'] = len(origin_weibo_list)
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
                    print "bulk error"
           print count_c


if __name__ == "__main__":

    startup_nodes = [{"host": REDIS_VENT_HOST, "port": REDIS_VENT_PORT}]
    cluster_redis = RedisCluster(startup_nodes = startup_nodes)


    es_logger = logging.getLogger("elasticsearch")
    es_logger.setLevel(logging.ERROR)
    FileHandler = logging.FileHandler("es.log")
    formatter = logging.Formatter("%(asctime)s_%(name)s_%(levelname)s_%(message)s")
    FileHandler.setFormatter(formatter)
    es_logger.addHandler(FileHandler)

    es =  Elasticsearch(['se13', 'se14'], timeout = 60, retry_on_timeout=True, max_retries=6)
    count = 0
    tb = time.time()
    print es.nodes.info("node_id=all")
    print es.cluster.health()

    while 1:
        es_index = time.strftime("%Y%m%d", time.localtime(time.time()-86400))
        try:
            bool = es.indices.exists(index=es_index)
            print bool
            if not bool:
                es.indices.create(index=es_index, ignore=400)
        except Exception,r:
            print Exception,":",r
            print "retry"
            es =  Elasticsearch(['se13', 'se14'], timeout = 60, retry_on_timeout=True,max_retries=6)
            continue

        id_set=[]
        try:
            user_set = cluster_redis.rpop('active_user_id')
            if user_set:
                temp = user_set.split(",")
                for item in temp:
                    user = item.split("'")[1]
                    count += 1
                    id_set.append(user)
                compute(id_set)

                if True:
                    ts = time.time()
                    print "%s : %s" %(count, ts - tb)
                    tb = ts
            else:
                time.sleep(60)
        except:
            print "redis cluster is flushed"
            time.sleep(60)


