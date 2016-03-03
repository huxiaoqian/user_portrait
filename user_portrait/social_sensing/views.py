#-*- coding:utf-8 -*-

import os
import time
import math
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from user_portrait.time_utils import datetime2ts, ts2datetime
from user_portrait.global_utils import R_SOCIAL_SENSING as r
from user_portrait.global_utils import es_user_portrait as es
from user_portrait.global_utils import portrait_index_name, portrait_index_type
from user_portrait.global_utils import group_index_name as index_group_manage
from user_portrait.global_utils import group_index_type as doc_type_group
from user_portrait.parameter import INDEX_MANAGE_SOCIAL_SENSING as index_manage_sensing_task
from user_portrait.parameter import DOC_TYPE_MANAGE_SOCIAL_SENSING as task_doc_type
from user_portrait.parameter import DETAIL_SOCIAL_SENSING as index_sensing_task
from user_portrait.parameter import finish_signal, unfinish_signal, SOCIAL_SENSOR_INFO
from utils import get_warning_detail, get_text_detail
from full_text_serach import aggregation_hot_keywords
from delete_es import delete_es

mod = Blueprint('social_sensing', __name__, url_prefix='/social_sensing')

#portrait_index_name = "user_portrait_1222"

# 前台设置好的参数传入次函数，创建感知任务,放入es, 从es中读取所有任务信息放入redis:sensing_task 任务队列中
# parameters: task_name, create_by, stop_time, remark, social_sensors, keywords
# other parameters: create_at, warning_status,
# warning_status: 0-no, 1-burst, 2-tracking, 3-ever_brusing, now no
# task_type：任务类型：{"0": no keywords and no sensors, "1": no keywords and some sensors, "2": "some keywords and no sensors", "3": "some keywords and some sensors"}
@mod.route('/create_task/')
def ajax_create_task():
    # task_name forbid illegal enter
    task_name = request.args.get('task_name','') # must
    create_by = request.args.get('create_by', 'admin') #
    stop_time = request.args.get('stop_time', "default") #timestamp, 1234567890
    social_sensors = request.args.get("social_sensors", "") #uid_list, split with ","
    keywords = request.args.get("keywords", "") # keywords_string, split with ","
    sensitive_words = request.args.get("sensitive_words", "") # sensitive_words, split with ","
    remark = request.args.get("remark", "")
    create_time = request.args.get('create_time', '')

    exist_es = es.exists(index=index_manage_sensing_task, doc_type=task_doc_type, id=task_name)
    if exist_es:
        return json.dumps(["0"]) # 任务名不能重合

    if task_name:
        task_detail = dict()
        task_detail["task_name"] = task_name
        task_detail["create_by"] = create_by
        task_detail["stop_time"] = stop_time
        task_detail["remark"] = remark
        if social_sensors:
            task_detail["social_sensors"] = json.dumps(list(set(social_sensors.split(','))))
        else:
            task_detail["social_sensors"] = json.dumps([])
        if keywords:
            task_detail["keywords"] = json.dumps(keywords.split(","))
        else:
            task_detail["keywords"] = json.dumps([])
        if sensitive_words:
            task_detail["sensitive_words"] = json.dumps(sensitive_words.split(","))
        else:
            task_detail["sensitive_words"] = json.dumps([])
        now_ts = int(time.time())
        task_detail["create_at"] = create_time # now_ts
        task_detail["warning_status"] = '0'
        task_detail["finish"] = "0" # not end the task
        task_detail["history_status"] = json.dumps([]) # ts, keywords, warning_status
        task_detail['burst_reason'] = ''
        task_detail['processing_status'] = "1" #任务正在进行
        if keywords:
            if social_sensors:
                task_detail["task_type"] = "3"
            else:
                task_detail["task_type"] = "2"
        else:
            if social_sensors:
                task_detail["task_type"] = "1"
            else:
                task_detail["task_type"] = "0"

    # store task detail into es
    es.index(index=index_manage_sensing_task, doc_type=task_doc_type, id=task_name, body=task_detail)


    return json.dumps(["1"])


@mod.route('/delete_task/')
def ajax_delete_task():
    # delete task based on task_name
    task_name = request.args.get('task_name','') # must
    if task_name:
        es.delete(index=index_manage_sensing_task, doc_type=task_doc_type, id=task_name)
        try:
            delete_es(task_name)
        except Exception, r:
            print Exception, r
        return json.dumps(['1'])
    else:
        return json.dumps([])



# 终止任务，即在到达终止时间前就终止任务
@mod.route('/stop_task/')
def ajax_stop_task():
    task_name = request.args.get('task_name','') # must
    if task_name:
        task_detail = es.get(index=index_manage_sensing_task, doc_type=task_doc_type, id=task_name)['_source']
        #task_detail["finish"] = finish_signal
        task_detail['processing_status'] = '0'
        es.index(index=index_manage_sensing_task, doc_type=task_doc_type, id=task_name, body=task_detail)
        return json.dumps(['1'])
    else:
        return json.dumps([])


# 修改任务终止时间
# 修改finish=0代表重启任务
# 修改终止时间，当任务停止后即使延迟终止时间，仍需要设置finish=0代表重新启动
# if finish == 1:
#    finish
# else:
#    if processing_status == 0:
#        print "stop"
#    else:
#        print "working"
@mod.route('/revise_task/')
def ajax_revise_task():
    task_name = request.args.get('task_name','') # must
    finish = request.args.get("finish", "10")
    stop_time = request.args.get('stop_time', '') # timestamp

    now_ts = datetime2ts("2013-09-06")
    #now_ts = time.time()
    if stop_time and stop_time < now_ts:
        return json.dumps([])

    if task_name:
        task_detail = es.get(index=index_manage_sensing_task, doc_type=task_doc_type, id=task_name)['_source']
        if stop_time:
            task_detail['stop_time'] = stop_time
        if int(finish) == 0:
            task_detail['finish'] = finish
            task_detail['processing_status'] = "1" # 重启时将处理状态改为
        if stop_time or int(finish) == 0:
            es.index(index=index_manage_sensing_task, doc_type=task_doc_type, id=task_name, body=task_detail)
            return json.dumps(['1'])
    return json.dumps([])



@mod.route('/show_task/')
def ajax_show_task():
    # show all working task
    # "0": unfinish working task
    # "1": finish working task
    status = request.args.get("finish", "01")
    length = len(status)
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                }
            }
        },
        "sort": {"create_at": {"order": "desc"}},
        "size": 10000
    }
    if length == 2:
        category_list = [status[0], status[1]]
        query_body['query']['filtered']['filter']['terms'] = {"finish": category_list}
    elif length == 1:
        query_body['query']['filtered']['filter']['term'] = {"finish": status}
    else:
        print "error"

    search_results = es.search(index=index_manage_sensing_task, doc_type=task_doc_type, body=query_body)['hits']['hits']

    results = []
    if search_results:
        for item in search_results:
            item = item['_source']
            history_status = json.loads(item['history_status'])
            keywords = json.loads(item['keywords'])
            item['keywords'] = keywords
            if history_status:
                temp_list = []
                temp_list.append(history_status[-1])
                for iter_item in history_status[:-1]:
                    if int(iter_item[-1]) != 0:
                        temp_list.append(iter_item)
                sorted_list = sorted(temp_list, key=lambda x:x[0], reverse=True)
                item['history_status'] = sorted_list
            else:
                item['history_status'] = history_status
            results.append(item)

    return json.dumps(results)


@mod.route('/get_task_detail_info/')
def ajax_get_task_detail_info():
    task_name = request.args.get('task_name','') # task_name
    task_detail = es.get(index=index_manage_sensing_task, doc_type=task_doc_type, id=task_name)['_source']
    task_detail["social_sensors"] = json.loads(task_detail["social_sensors"])
    task_detail['keywords'] = json.loads(task_detail['keywords'])
    task_detail["sensitive_words"]= json.loads(task_detail["sensitive_words"])
    history_status = json.loads(task_detail['history_status'])
    if history_status:
        temp_list = []
        temp_list.append(history_status[-1])
        for item in history_status[:-1]:
            if int(item[-1]) != 0:
                temp_list.append(item)
        sorted_list = sorted(temp_list, key=lambda x:x[0], reverse=True)
        task_detail['history_status'] = sorted_list
    else:
        task_detail['history_status'] = history_status
    task_detail['social_sensors_portrait'] = []
    portrait_detail = []

    if task_detail["social_sensors"]:
        search_results = es.mget(index=portrait_index_name, doc_type=portrait_index_type, body={"ids": task_detail["social_sensors"]})['docs']
        if search_results:
            for item in search_results:
                temp = []
                if item['found']:
                    for iter_item in SOCIAL_SENSOR_INFO:
                        if iter_item == "topic_string":
                            temp.append(item["_source"][iter_item].split('&'))
                        else:
                            temp.append(item["_source"][iter_item])
                    portrait_detail.append(temp)
        if portrait_detail:
            portrait_detail = sorted(portrait_detail, key=lambda x:x[5], reverse=True)
    task_detail['social_sensors_portrait'] = portrait_detail

    return json.dumps(task_detail)



# unfinished
@mod.route('/get_group_list/')
def ajax_get_group_list():
    # get all group list from group manage
    results = [] #
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"term": {"task_type": "analysis"}},
                            {"term": {"status": 1}} # attention-------------------------
                        ]
                    }
                }
            }
        },
        "sort": {"submit_date": {"order": "desc"}},
        "size": 10000
    }

    search_results = es.search(index=index_group_manage, doc_type=doc_type_group, body=query_body, timeout=600)['hits']['hits']
    if search_results:
        for item in search_results:
            item = item['_source']
            temp = []
            temp.append(item['task_name'])
            temp.append(item['submit_user'])
            temp.append(item['submit_date'])
            temp.append(item['count'])
            temp.append(item.get('state', ""))
            try:
                temp.append(json.loads(item['uid_list']))
            except:
                temp.append(item['uid_list'])
            results.append(temp)

    return json.dumps(results)

def get_top_influence(key):
    query_body = {
        "query":{
            "match_all": {}
        },
        "sort":{key:{"order":"desc"}},
        "size": 1
    }

    search_result = es.search(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)['hits']['hits']
    if search_result:
        result = search_result[0]['_source'][key]

    return result

@mod.route('/get_group_detail/')
def ajax_get_group_detail():
    task_name = request.args.get('task_name','') # task_name
    portrait_detail = []
    top_activeness = get_top_influence("activeness")
    top_influence = get_top_influence("influence")
    top_importance = get_top_influence("importance")
    search_result = es.get(index=index_group_manage, doc_type=doc_type_group, id=task_name).get('_source', {})
    if search_result:
        try:
            uid_list = json.loads(search_result['uid_list'])
        except:
            uid_list = search_result['uid_list']
        if uid_list:
            search_results = es.mget(index=portrait_index_name, doc_type=portrait_index_type, body={"ids":uid_list}, fields=SOCIAL_SENSOR_INFO)['docs']
            for item in search_results:
                temp = []
                if item['found']:
                    for iter_item in SOCIAL_SENSOR_INFO:
                        if iter_item == "topic_string":
                            temp.append(item["fields"][iter_item][0].split('&'))
                            temp.append(item["fields"][iter_item][0].split('&'))
                        elif iter_item == "activeness":
                            temp.append(math.ceil(item["fields"][iter_item][0]/float(top_activeness)*100))
                        elif iter_item == "importance":
                            temp.append(math.ceil(item["fields"][iter_item][0]/float(top_importance)*100))
                        elif iter_item == "influence":
                            temp.append(math.ceil(item["fields"][iter_item][0]/float(top_influence)*100))
                        else:
                            temp.append(item["fields"][iter_item][0])
                    portrait_detail.append(temp)

    return json.dumps(portrait_detail)


# 返回某个预警事件的详细信息，包括微博量、情感和参与的人
@mod.route('/get_warning_detail/')
def ajax_get_warning_detail():
    task_name = request.args.get('task_name','') # task_name
    keywords = request.args.get('keywords', '') # warning keywords, seperate with ","
    keywords_list = keywords.split(',')
    ts = request.args.get('ts', '') # timestamp: 123456789

    results = get_warning_detail(task_name, keywords_list, ts)

    return json.dumps(results)

# 聚合关键词
@mod.route('/get_keywords_list/')
def ajax_get_keywords_list():
    task_name = request.args.get('task_name','') # task_name
    keywords = request.args.get('keywords', '') # warning keywords, seperate with ","
    keywords_list = keywords.split(',')
    ts = request.args.get('ts', '') # timestamp: 123456789

    task_detail = es.get(index=index_manage_sensing_task, doc_type=task_doc_type, id=task_name)['_source']
    start_time = task_detail['create_at']

    results = aggregation_hot_keywords(start_time, ts, keywords_list)

    return json.dumps(results)


# 返回某个时间段特定的文本，按照热度排序
@mod.route('/get_text_detail/')
def ajax_get_text_detail():
    task_name = request.args.get('task_name','') # task_name
    ts = int(request.args.get('ts', '')) # timestamp: 123456789
    text_type = request.args.get('text_type', '') # which line

    results = get_text_detail(task_name, ts, text_type)

    return json.dumps(results)

# 返回某个预警点的微博主题, 没有则为空
@mod.route('/get_clustering_topic/')
def ajax_get_clustering_topic():
    task_name = request.args.get('task_name','') # task_name
    ts = int(request.args.get('ts', '')) # timestamp: 123456789
    topic_list = []
    try:
        task_detail = es.get(index=index_sensing_task, doc_type=task_name, id=ts)['_source']
    except:
        return json.dumps([])
    burst_reason = task_detail['burst_reason']
    if burst_reason:
        topic_list = task_detail.get("clustering_topic", [])
        if topic_list:
            topic_list = json.loads(topic_list)

    return json.dumps(topic_list)

# 返回传感词
@mod.route('/get_sensing_words/')
def ajax_get_sensing_words():
    tmp = json.dumps([])
    sensing_words = r.hget('sensing_words', "sensing_words")
    if sensing_words:
        return sensing_words
    else:
        return tmp

# 返回敏感词
@mod.route('/get_sensitive_words/')
def ajax_get_sensitive_words():
    tmp = json.dumps([])
    sensitive_words = r.hget("sensitive_words", "sensitive_words")
    if sensitive_words:
        return sensitive_words
    else:
        return tmp

# 增加传感词
@mod.route('/add_sensing_words/')
def ajax_add_sensing_words():
    add_words = request.args.get("add_words_list", "") #seperate with ","
    add_words_list = add_words.split(',')
    sensing_words = json.loads(r.hget('sensing_words', "sensing_words"))
    new_words_list = list(set(sensing_words) | set(add_words_list))
    r.hset('sensing_words', "sensing_words", json.dumps(new_words_list))

    return "1"

# 增加敏感词
@mod.route('/add_sensitive_words/')
def ajax_add_sensitive_words():
    add_words = request.args.get("add_words_list", "") #seperate with ","
    add_words_list = add_words.split(',')
    sensing_words = json.loads(r.hget('sensitive_words', "sensitive_words"))
    new_words_list = list(set(sensing_words) | set(add_words_list))
    r.hset('sensitive_words', "sensitive_words", json.dumps(new_words_list))

    return "1"


# 删除传感词
@mod.route('/delete_sensing_words/')
def ajax_delete_sensing_words():
    delete_words = request.args.get("delete_words_list", "") #seperate with ","
    delete_words_list = delete_words.split(',')
    sensing_words = json.loads(r.hget('sensing_words', "sensing_words"))
    new_words_list = list(set(sensing_words) - set(delete_words_list))
    r.hset('sensing_words', "sensing_words", json.dumps(new_words_list))

    return "1"


# 删除敏感词
@mod.route('/delete_sensitive_words/')
def ajax_delete_sensitive_words():
    delete_words = request.args.get("delete_words_list", "") #seperate with ","
    delete_words_list = delete_words.split(',')
    sensentive_words = json.loads(r.hget('sensitive_words', "sensitive_words"))
    new_words_list = list(set(sensitive_words) - set(delete_words_list))
    r.hset('sensitive_words', "sensitive_words", json.dumps(new_words_list))

    return "1"


