# -*- coding:utf-8 -*-

# es 使用 Unicode
import sys
import json
import math
import time
from full_text_serach import count_hot_uid, query_hot_mid
from user_portrait.time_utils import ts2date
from user_portrait.global_utils import es_user_profile as es_profile
from user_portrait.global_utils import es_user_portrait as es
from user_portrait.global_utils import es_flow_text as es_text
from user_portrait.global_utils import profile_index_name, profile_index_type, portrait_index_name, portrait_index_type, \
                         flow_text_index_name_pre, flow_text_index_type
from user_portrait.parameter import INDEX_MANAGE_SOCIAL_SENSING as index_manage_sensing_task
from user_portrait.parameter import DOC_TYPE_MANAGE_SOCIAL_SENSING as task_doc_type
from user_portrait.parameter import DETAIL_SOCIAL_SENSING as index_sensing_task
from user_portrait.parameter import SOCIAL_SENSOR_INFO, signal_count_varition, signal_sentiment_varition, CURRENT_WARNING_DICT, IMPORTANT_USER_THRESHOULD
from user_portrait.time_utils import ts2date_min

portrait_index_name = "user_portrait_1222"

# 特别适用于doc_type=2的事件
def get_task_detail_2(task_name, keywords, ts):
    results = dict()
    index_name = task_name
    task_detail = es.get(index=index_manage_sensing_task, doc_type=task_doc_type, id=task_name)["_source"]
    task_name = task_detail['task_name']
    keywords_list = json.loads(task_detail['keywords'])
    social_sensors = json.loads(task_detail['social_sensors'])
    history_status = json.loads(task_detail['history_status'])
    start_time = task_detail['create_at']
    stop_time = task_detail['stop_time']
    portrait_detail = []
    count = 0 # 计数

    if social_sensors:
        search_results = es.mget(index=portrait_index_name, doc_type=portrait_index_type, body={"ids":social_sensors}, fields=SOCIAL_SENSOR_INFO)['docs']
        for item in search_results:
            temp = []
            if item['found']:
                for iter_item in SOCIAL_SENSOR_INFO:
                    if iter_item == "topic_string":
                        temp.append(item["fields"][iter_item][0].split('&'))
                    else:
                        temp.append(item["fields"][iter_item][0])
                portrait_detail.append(temp)

    time_series = [] # 时间
    positive_sentiment_list = [] # 情绪列表
    neutral_sentiment_list = []
    anger_sentiment_list = []
    sad_sentiment_list = []
    origin_weibo_list = [] # 微博列表
    retweeted_weibo_list = []
    comment_weibo_list = []
    total_number_list = []
    burst_time_list = [] # 爆发时间列表
    important_user_set = set() # 重要人物列表

    ts = int(ts)
    for item in history_status:
        if int(item[0]) <= ts:
            time_series.append(item[0]) # 到目前为止的所有的时间戳
    print time_series
    # get detail task information from es
    if time_series:
        #print time_series
        flow_detail = es.mget(index=index_sensing_task, doc_type=index_name, body={"ids": time_series})['docs']
    else:
        flow_detail = {}
    if flow_detail:
        for item in flow_detail:
            item = item['_source']
            timestamp = item['timestamp']
            sentiment_distribution = json.loads(item["sentiment_distribution"])
            positive_sentiment_list.append(int(sentiment_distribution['1']))
            sad_sentiment_list.append(int(sentiment_distribution['2']))
            anger_sentiment_list.append(int(sentiment_distribution['3']))
            neutral_sentiment_list.append(int(sentiment_distribution['0']))
            origin_weibo_list.append(item["origin_weibo_number"])
            retweeted_weibo_list.append(item['retweeted_weibo_number'])
            comment_weibo_list.append(item['comment_weibo_number'])
            total_number_list.append(item['weibo_total_number'])
            temp_user_list = json.loads(item['important_users'])
            important_user_set = important_user_set | set(temp_user_list)

            burst_reason = item.get("burst_reason", "")
            if burst_reason:
                burst_time_list.append([timestamp, count])
            count += 1
    negetive_sentiment_list = []
    for i in range(len(time_series)):
        negetive_sentiment_list.append(sad_sentiment_list[i]+anger_sentiment_list[i])


    # 统计爆发原因，下相应的结论
    weibo_variation_count = 0
    weibo_variation_time = []
    sentiment_variation_count = 0
    sentiment_variation_time = []
    common_variation_count = 0
    common_variation_time = []
    if burst_time_list:
        for item in burst_time_list:
            if int(item[1]) == int(signal_count_varition):
                weibo_variation_count += 1
                weibo_variation_time.append([ts2date(item[0]), total_number_list[item[1]]])
            elif int(item[1]) == int(signal_sentiment_varition):
                sentiment_variation_count += 1
                sentiment_variation_time.append([ts2date(item[0]), negetive_sentiment_list[item[1]]])
            else:
                weibo_variation_count += 1
                weibo_variation_time.append([ts2date(item[0]), total_number_list[item[1]]])
                sentiment_variation_count += 1
                sentiment_variation_time.append([ts2date(item[0]), negetive_sentiment_list[item[1]]])
                common_variation_count += 1
                common_variation_time.append(ts2date(item[0]))

    if weibo_variation_count == 0 and sentiment_variation_count == 0:
        warning_conclusion = CURRENT_WARNING_DICT['0']
        variation_distribution = [[], [], []]
    elif weibo_variation_count !=0 and sentiment_variation_count == 0:
        warning_conclusion = CURRENT_WARNING_DICT['1']
        variation_distribution = [weibo_variation_time, [], []]
    elif weibo_variation_count ==0 and sentiment_variation_count != 0:
        warning_conclusion = CURRENT_WARNING_DICT['2']
        variation_distribution = [[], sentiment_variation_time, []]
    else:
        warning_conclusion = CURRENT_WARNING_DICT['3']
        variation_distribution = [weibo_variation_time, sentiment_variation_time, common_variation_time]

    results['warning_conclusion'] = warning_conclusion
    results['variation_distribution'] = variation_distribution

    # 每个用户的热度


    # 获取重要用户的个人信息
    important_uid_list = list(important_user_set)
    user_detail_info = [] #
    if important_uid_list:
        user_results = es.mget(index=portrait_index_name, doc_type=portrait_index_type, body={"ids":important_uid_list}, fields=['uid', 'uname', 'domain', 'topic_string', "photo_url", 'importance', 'influence', 'activeness'])['docs']
        for item in user_results:
            if item['found']:
                temp = []
                if int(item['fields']['importance'][0]) < IMPORTANT_USER_THRESHOULD:
                    continue
                temp.append(item['fields']['uid'][0])
                temp.append(item['fields']['uname'][0])
                temp.append(item['fields']['photo_url'][0])
                temp.append(item['fields']['domain'][0])
                temp.append(item['fields']['topic_string'][0].split('&'))
                hot_count = count_hot_uid(item['fields']['uid'][0], start_time, stop_time, keywords_list)
                temp.append(hot_count)
                temp.append(item['fields']['importance'][0])
                temp.append(item['fields']['influence'][0])
                temp.append(item['fields']['activeness'][0])
                user_detail_info.append(temp)
                #print temp

    revise_time_series = []
    for item in time_series:
        revise_time_series.append(ts2date_min(item))

    results['keywords'] = keywords_list
    #results['keywords_list'] = sorted_keywords_list
    results['important_user_detail'] = user_detail_info
    results['burst_time'] = burst_time_list # 爆发时间点，以及爆发原因
    results['time_series'] = revise_time_series
    results['positive_sentiment_list'] = positive_sentiment_list
    results['negetive_sentiment_list'] = negetive_sentiment_list
    results['neutral_sentiment_list'] = neutral_sentiment_list
    results['origin_weibo_list'] = origin_weibo_list
    results['retweeted_weibo_list'] = retweeted_weibo_list
    results['comment_weibo_list'] = comment_weibo_list
    results['total_number_list'] = total_number_list
    results['social_sensors_detail'] = portrait_detail


    return results


# 获得某个时间段的文本内容，返回ts-time_interval~ts之间的
def get_detail_text(task_name, keywords_list, ts, text_type):
    task_detail = es.get(index=index_manage_sensing_task, doc_type=task_doc_type, id=task_name)["_source"]
    keywords_list = json.loads(task_detail['keywords'])
    results = query_hot_mid(ts, keywords_list, text_type="1")

    return results


if __name__ == "__main__":
    print get_task_detail_2('监督维权律师', "keywords", "1378323000")


