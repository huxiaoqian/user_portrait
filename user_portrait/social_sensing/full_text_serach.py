# -*- coding:utf-8 -*-

import sys
import time
import json
import numpy as np
from elasticsearch import Elasticsearch

from user_portrait.global_utils import es_flow_text as es_text
from user_portrait.global_utils import es_user_profile as es_profile
from user_portrait.global_utils import es_user_portrait
from user_portrait.global_utils import R_SOCIAL_SENSING as r
from user_portrait.time_utils import ts2datetime, datetime2ts
from user_portrait.global_utils import flow_text_index_name_pre, flow_text_index_type, profile_index_name, profile_index_type, \
                         portrait_index_name, portrait_index_type
from user_portrait.parameter import SOCIAL_SENSOR_TIME_INTERVAL as time_interval
from user_portrait.parameter import SOCIAL_SENSOR_FORWARD_RANGE as forward_time_range
from user_portrait.parameter import DETAIL_SOCIAL_SENSING as index_sensing_task
from user_portrait.parameter import INDEX_MANAGE_SOCIAL_SENSING as index_manage_social_task
from user_portrait.parameter import DOC_TYPE_MANAGE_SOCIAL_SENSING as task_doc_type
from user_portrait.parameter import FORWARD_N as forward_n
from user_portrait.parameter import INITIAL_EXIST_COUNT as initial_count
from user_portrait.parameter import IMPORTANT_USER_NUMBER, IMPORTANT_USER_THRESHOULD, signal_brust, signal_track, signal_count_varition, signal_sentiment_varition,signal_nothing, signal_nothing_variation, \
                      unfinish_signal, finish_signal, AGGRAGATION_KEYWORDS_NUMBER, PRE_AGGREGATION_NUMBER
from user_portrait.time_utils import ts2date
day_time = 24*3600



# 获得原创微博内容，按时间排序
def get_origin_weibo_detail(ts, social_sensors, keywords_list, size=100, message_type=1):
    results = []
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"range":{
                                "timestamp":{
                                    "gte": ts - time_interval,
                                    "lt": ts
                                }
                            }},
                            {"terms":{"keywords_string": keywords_list}},
                            {"term": {"message_type": message_type}}
                        ]
                    }
                }
            }
        },
        "size": size,
        "sort": {"timestamp": {"order": "desc"}}
    }

    if social_sensors:
        query_body["query"]["filtered"]["filter"]["bool"]["must"].append({"terms":{"uid": social_sensors}})

    datetime = ts2datetime(ts)
    datetime_1 = ts2datetime(ts-time_interval)
    index_name = flow_text_index_name_pre + datetime
    exist_es = es_text.indices.exists(index_name)
    index_name_1 = flow_text_index_name_pre + datetime_1
    exist_es_1 = es_text.indices.exists(index_name_1)

    if datetime == datetime_1 and exist_es:
        search_results = es_text.search(index=index_name, doc_type=flow_text_index_type, body=query_body)["hits"]["hits"]
    elif datetime != datetime_1 and exist_es_1:
        search_results = es_text.search(index=index_name_1, doc_type=flow_text_index_type, body=query_body)["hits"]["hits"]
    else:
        search_results = []

    uid_list = []
    if search_results:
        for item in search_results:
            uid_list.append(item["_source"]['uid'])
        if uid_list:
            portrait_result = es_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={"ids":uid_list}, fields=['nick_name', 'photo_url'])["docs"]

        for i in range(len(uid_list)):
            item = search_results[i]['_source']
            temp = []
            # uid, nick_name, photo_url, text, sentiment, timestamp, geo, common_keywords
            temp.append(item['uid'])
            if portrait_result[i]['found']:
                temp.append(portrait_result[i]["fields"]["nick_name"][0])
                temp.append(portrait_result[i]["fields"]["photo_url"][0])
            else:
                temp.append("unknown")
                temp.append("")
            temp.append(item["text"])
            print item['text']
            temp.append(item["sentiment"])
            temp.append(ts2date(item['timestamp']))
            temp.append(item['geo'])
            keywords_set = set(item['keywords_string'].split('&'))
            common_keywords = set(keywords_list) & keywords_set
            temp.append(list(common_keywords))
            results.append(temp)

    return results

# 
def return_weibo_text_detail(former_results, keywords_list):
    results = []

    uid_list = []
    former_count_n = 0
    former_count_list = []
    if former_results:
        for item in former_results:
            if item["found"]:
                uid_list.append(item['_source']['uid'])
                former_count_list.append(former_count_n)
            former_count_n += 1
        print "former_count_list: ", former_count_list

        if uid_list:
            portrait_result = es_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={"ids":uid_list}, fields=['nick_name', 'photo_url'])["docs"]
        else:
            portrait_result = []

        if uid_list:
            for i in range(len(uid_list)):
                item = former_results[former_count_list[i]]['_source']
                temp = []
                # uid, nick_name, photo_url, text, sentiment, timestamp, geo, common_keywords
                temp.append(item['uid'])
                if portrait_result[i]['found']:
                    temp.append(portrait_result[i]["fields"]["nick_name"][0])
                    temp.append(portrait_result[i]["fields"]["photo_url"][0])
                else:
                    temp.append("unknown")
                    temp.append("")
                temp.append(item["text"])
                print item['text']
                temp.append(item["sentiment"])
                temp.append(ts2date(item['timestamp']))
                temp.append(item['geo'])
                keywords_set = set(item['keywords_string'].split('&'))
                common_keywords = keywords_set & set(keywords_list)
                temp.append(list(common_keywords))
                results.append(temp)

    return results


def get_retweet_weibo_detail(ts, social_sensors, keywords_list, size, text_type):
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"range":{
                                "timestamp":{
                                    "gte": ts - time_interval,
                                    "lt": ts
                                }
                            }},
                            {"terms": {"keywords_string": keywords_list}},
                            {"term": {"message_type": text_type}}
                        ]
                    }
                }
            }
        },
        "aggs":{
            "hot_origin_list":{
                "terms":{"field":"root_mid", "size": size+50}
            }
        }
    }

    if social_sensors:
        query_body["query"]["filtered"]["filter"]["bool"]["must"].append({"terms":{"uid": social_sensors}})

    datetime = ts2datetime(ts)
    datetime_1 = ts2datetime(ts-time_interval)
    index_name = flow_text_index_name_pre + datetime
    exist_es = es_text.indices.exists(index_name)
    index_name_1 = flow_text_index_name_pre + datetime_1
    exist_es_1 = es_text.indices.exists(index_name_1)

    # 1. 聚合原创微博mid list
    if datetime == datetime_1 and exist_es:
        search_results = es_text.search(index=index_name, doc_type=flow_text_index_type, body=query_body)["aggregations"]["hot_origin_list"]["buckets"]
    elif datetime != datetime_1 and exist_es_1:
        search_results = es_text.search(index=index_name_1, doc_type=flow_text_index_type, body=query_body)["aggregations"]["hot_origin_list"]["buckets"]
    else:
        search_results = []

    count = 0
    if search_results:
        mid_list = []
        for item in search_results:
            mid_list.append(item["key"])

    # 2. 获得原创微博信息
    results = []
    if mid_list:
        if datetime == datetime_1 and exist_es:
            text_results = es_text.mget(index=index_name, doc_type=flow_text_index_type, body={"ids": mid_list})["docs"]
        elif datetime != datetime_1 and exist_es_1:
            text_results = es_text.mget(index=index_name, doc_type=flow_text_index_type, body={"ids": mid_list})["docs"]
        else:
            text_results = []
        print mid_list

        # 3. 获得人的信息
        current_result = return_weibo_text_detail(text_results, keywords_list)
        results.extend(current_result)

        # 前一天
        if datetime == datetime_1:
            former_index = flow_text_index_name_pre + ts2datetime(ts - day_time)
        else:
            former_index = flow_text_index_name_pre + ts2datetime(ts - time_interval - day_time)
        exist_es = es_text.indices.exists(former_index)
        if exist_es:
            former_results = es_text.mget(index=former_index, doc_type=flow_text_index_type, body={"ids": mid_list})["docs"] 
            former_result = return_weibo_text_detail(former_results, keywords_list)
            results.extend(former_result)
            print former_index

        # 前两天
        if datetime == datetime_1:
            former_index = flow_text_index_name_pre + ts2datetime(ts - 2*day_time)
        else:
            former_index = flow_text_index_name_pre + ts2datetime(ts - time_interval - 2*day_time)
        exist_es = es_text.indices.exists(former_index)
        if exist_es:
            former_results = es_text.mget(index=former_index, doc_type=flow_text_index_type, body={"ids": mid_list})["docs"]
            former_result = return_weibo_text_detail(former_results, keywords_list)
            results.extend(former_result)
            print former_index


        """
        uid_list = []
        count_n = 0
        count_list = []
        if text_results:
            for item in text_results:
                if item["found"]:
                    uid_list.append(item['_source']['uid'])
                    count_list.append(count_n)
                count_n += 1 #记录能够找到微博的索引

            if uid_list:
                portrait_result = es_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={"ids":uid_list}, fields=['nick_name', 'photo_url'])["docs"]
            else:
                portrait_result = []
            print "count_list", count_list

            # 4. 获取微博详细信息
            if uid_list:
                for i in range(len(uid_list)):
                    item = text_results[count_list[i]]['_source']
                    temp = []
                    # uid, nick_name, photo_url, text, sentiment, timestamp, geo, common_keywords
                    temp.append(item['uid'])
                    if portrait_result[i]['found']:
                        temp.append(portrait_result[i]["fields"]["nick_name"][0])
                        temp.append(portrait_result[i]["fields"]["photo_url"][0])
                    else:
                        temp.append("unknown")
                        temp.append("")
                    temp.append(item["text"])
                    print item['text']
                    temp.append(item["sentiment"])
                    temp.append(ts2date(item['timestamp']))
                    temp.append(item['geo'])
                    keywords_set = set(item['keywords_string'].split('&'))
                    common_keywords = keywords_set & set(keywords_list)
                    temp.append(list(common_keywords))
                    results.append(temp)
            print results
        """

        sorted_results = sorted(results, key=lambda x:x[5], reverse=False)

    return sorted_results



# 获得积极情绪的微博
def get_positive_weibo_detail(ts, social_sensors, keywords_list, size, sentiment_type=1):
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"range":{
                                "timestamp":{
                                    "gte": ts - time_interval,
                                    "lt": ts
                                }
                            }},
                            {"terms":{"keywords_string": keywords_list}},
                           # {"term":{"sentiment": "1"}}
                        ]
                    }
                }
            }
        },
        "size": size,
        "sort": {"timestamp": {"order": "desc"}}
    }

    if social_sensors:
        query_body["query"]["filtered"]["filter"]["bool"]["must"].append({"terms":{"uid": social_sensors}})

    if int(sentiment_type) == 1 or int(sentiment_type) == 0:
        query_body["query"]["filtered"]["filter"]["bool"]["must"].append({"term":{"sentiment":sentiment_type}})
    else:
        query_body["query"]["filtered"]["filter"]["bool"]["should"] = [{"terms":{"sentiment": ["2", "3"]}}]

    # 判断当前ts和ts-time_interval是否属于同一天，确定查询哪个es
    datetime = ts2datetime(ts)
    datetime_1 = ts2datetime(ts-time_interval)
    index_name = flow_text_index_name_pre + datetime
    exist_es = es_text.indices.exists(index_name)
    index_name_1 = flow_text_index_name_pre + datetime_1
    exist_es_1 = es_text.indices.exists(index_name_1)

    # 1. 聚合原创微博mid list
    if datetime == datetime_1 and exist_es:
        search_results = es_text.search(index=index_name, doc_type=flow_text_index_type, body=query_body)["hits"]["hits"]
    elif datetime != datetime_1 and exist_es_1:
        search_results = es_text.search(index=index_name_1, doc_type=flow_text_index_type, body=query_body)["hits"]["hits"]
    else:
        search_results = []
    print search_results
    uid_list = []
    results = []
    if search_results:
        for item in search_results:
            uid_list.append(item["_source"]['uid'])
        if uid_list:
            portrait_result = es_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={"ids":uid_list}, fields=['nick_name', 'photo_url'])["docs"]

        for i in range(len(uid_list)):
            item = search_results[i]['_source']
            temp = []
            # uid, nick_name, photo_url, text, sentiment, timestamp, geo, common_keywords
            temp.append(item['uid'])
            if portrait_result[i]['found']:
                temp.append(portrait_result[i]["fields"]["nick_name"][0])
                temp.append(portrait_result[i]["fields"]["photo_url"][0])
            else:
                temp.append("unknown")
                temp.append("")
            temp.append(item["text"])
            print item['text']
            temp.append(item["sentiment"])
            temp.append(ts2date(item['timestamp']))
            temp.append(item['geo'])
            keywords_set = set(item['keywords_string'].split('&'))
            common_keywords = set(keywords_list) & keywords_set
            temp.append(list(common_keywords))
            results.append(temp)

    return results





def query_hot_mid(ts, keywords_list, text_type,size=100):
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"range":{
                                "timestamp":{
                                    "gte":ts - time_interval,
                                    "lt": ts
                                }
                            }},
                            {"terms": {"keywords_string": keywords_list}},
                            {"term": {"message_type": "0"}}
                        ]
                    }
                }
            }
        },
        "aggs":{
            "all_interests":{
                "terms":{"field": "root_mid", "size": size}
            }
        }
    }

    datetime = ts2datetime(ts)
    datetime_1 = ts2datetime(ts-time_interval)
    index_name = flow_text_index_name_pre + datetime
    exist_es = es_text.indices.exists(index_name)
    index_name_1 = flow_text_index_name_pre + datetime_1
    exist_bool_1 = es_text.indices.exists(index_name_1)
    print datetime, datetime_1
    if datetime == datetime_1 and exist_es:
        search_results = es_text.search(index=index_name, doc_type=flow_text_index_type, body=query_body)["aggregations"]["all_interests"]["buckets"]
    elif datetime != datetime_1 and exist_bool_1:
        search_results = es_text.search(index=index_name_1, doc_type=flow_text_index_type, body=query_body)["aggregations"]["all_interests"]["buckets"]
    else:
        search_results = []

    hot_mid_list = []
    if search_results:
        for item in search_results:
            print item
            temp = []
            temp.append(item['key'])
            temp.append(item['doc_count'])
            hot_mid_list.append(temp)

    print hot_mid_list

    return hot_mid_list


def count_hot_uid(uid, start_time, stop_time, keywords_list):
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"range":{
                                "timestamp":{
                                    "gte":start_time,
                                    "lt": stop_time
                                }
                            }},
                            {"term": {"root_uid": uid}}
                        ]
                    }
                }
#                "query":{
#                    "bool":{
#                        "should":[
#                        ]
#                    }
#                }
            }
        }
    }

    if keywords_list:
        query_body['query']['filtered']['filter']['bool']['must'].append({"terms": {"keywords_string": keywords_list}})
        #for word in keywords_list:
            #query_body['query']['filtered']['query']['bool']['should'].append({'wildcard':{"text": "*"+word+"*"}})

    count = 0
    datetime = ts2datetime(float(stop_time))
    index_name = flow_text_index_name_pre + datetime
    exist_es = es_text.indices.exists(index_name)
    if exist_es:
        count = es_text.count(index=index_name, doc_type=flow_text_index_type, body=query_body)["count"]
    else:
        count = 0

    datetime_1 = ts2datetime(float(start_time))
    if datetime_1 == datetime:
        pass
    else:
        ts = float(stop_time)
        while 1:
            ts = ts-day_time
            datetime = ts2datetime(ts)
            index_name = flow_text_index_name_pre + datetime
            exist_es = es_text.indices.exists(index_name)
            if exist_es:
                count = es_text.count(index=index_name, doc_type=flow_text_index_type, body=query_body)["count"]
            else:
                count += 0
            if datetime_1 == datetime:
                break

    return count



def aggregation_hot_keywords(start_time, stop_time, keywords_list):
    start_time = int(start_time)
    stop_time = int(stop_time)
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"terms": {"keywords_string": keywords_list}},
                            {"range":{
                                "timestamp":{
                                    "gte":start_time,
                                    "lt": stop_time
                                }
                            }}
                        ]
                    }
                }
            }
        },
        "aggs":{
            "all_keywords":{
                "terms": {"field": "keywords_string", "size": PRE_AGGREGATION_NUMBER}
            }
        }
    }


    keywords_dict = dict()
    datetime = ts2datetime(float(stop_time))
    index_name = flow_text_index_name_pre + datetime
    exist_es = es_text.indices.exists(index_name)
    if exist_es:
        search_results = es_text.search(index=index_name, doc_type=flow_text_index_type, body=query_body)["aggregations"]['all_keywords']['buckets']
        if search_results:
            for item in search_results:
                keywords_dict[item['key']] = item['doc_count']

    datetime_1 = ts2datetime(float(start_time))
    if datetime_1 == datetime:
        pass
    else:
        ts = float(stop_time)
        while 1:
            keywords_dict_1 = dict()
            ts = ts-day_time
            datetime = ts2datetime(ts)
            index_name = flow_text_index_name_pre + datetime
            exist_es = es_text.indices.exists(index_name)
            if exist_es:
                search_results_1 = es_text.search(index=index_name, doc_type=flow_text_index_type, body=query_body)["aggregations"]['all_keywords']['buckets']
                if search_results_1:
                    print search_results_1
                    for item in search_results_1:
                        keywords_dict_1[item['key']] = item['doc_count']
                for iter_key in keywords_dict_1.keys():
                    if keywords_dict.has_key(iter_key):
                        keywords_dict[iter_key] += keywords_dict_1[iter_key]
                    else:
                        keywords_dict[iter_key] = keywords_dict_1[iter_key]
            if datetime_1 == datetime:
                break
    print keywords_dict
    return_dict = sorted(keywords_dict.items(), key=lambda x:x[1], reverse=True)[:AGGRAGATION_KEYWORDS_NUMBER]
    return return_dict




