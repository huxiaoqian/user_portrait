# -*- coding:utf-8 -*-

# es 使用 Unicode
import sys
import json
import math
import time

reload(sys)
sys.path.append('./../')
from global_utils import es_user_profile as es_profile
from global_utils import es_user_portrait as es
from global_utils import es_flow_text as es_text
from global_utils import profile_index_name, profile_index_type, portrait_index_name, portrait_index_type, \
                         flow_text_index_name_pre, flow_text_index_type
from parameter import INDEX_MANAGE_SOCIAL_SENSING as index_manage_sensing_task
from parameter import DOC_TYPE_MANAGE_SOCIAL_SENSING as task_doc_type
from parameter import DETAIL_SOCIAL_SENSING as index_sensing_task


# 特别适用于doc_type=2的事件
def get_task_detail_2(task_name, keywords, ts):
    results = dict()
    index_name = task_name.decode('utf-8') # 可能的index-name
    task_detail = es.get(index=index_manage_sensing_task, doc_type=task_doc_type, id=index_name)["_source"]
    history_status = json.loads(task_detail['history_status'])

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
            important_user_set | set(temp_user_list)

            burst_reason = item.get("burst_reason", "")
            if burst_reason:
                burst_time_list.append([timestamp, burst_reason])

    # 获取重要用户的个人信息
    important_uid_list = list(important_user_set)
    user_detail_info = [] #
    if important_uid_list:
        user_results = es.mget(index=portrait_index_name, doc_type=portrait_index_type, body={"ids":important_uid_list}, fields=['uid', 'uname', 'domain', 'topic_string', "fansnum", 'importance', 'influence', 'activeness'])['docs']
        for item in user_results:
            if item['found']:
                temp = []
                temp.append(item['fields']['uid'][0])
                temp.append(item['fields']['uname'][0])
                temp.append(item['fields']['domain'][0])
                temp.append(item['fields']['topic_string'][0].split('&'))
                temp.append(item['fields']['fansnum'][0])
                temp.append(item['fields']['importance'][0])
                temp.append(item['fields']['influence'][0])
                temp.append(item['fields']['activeness'][0])
                user_detail_info.append(temp)

    results['important_user_detail'] = user_detail_info
    results['burst_time'] = burst_time_list
    results['time_series'] = time_series
    results['positive_sentiment_list'] = positive_sentiment_list
    results['sad_sentiment_list'] = sad_sentiment_list
    results['anger_sentiment_list'] = anger_sentiment_list
    results['neutral_sentiment_list'] = neutral_sentiment_list
    results['origin_weibo_list'] = origin_weibo_list
    results['retweeted_weibo_list'] = retweeted_weibo_list
    results['comment_weibo_list'] = comment_weibo_list
    results['total_number_list'] = total_number_list

    return results



#def get_detail_text(ts):


if __name__ == "__main__":
    print get_task_detail_2("监督政府腐败舆论", "keywords", "1378045800")


