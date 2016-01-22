# -*-coding:utf-8 -*-
import sys
import json
import time
import redis
from elasticsearch import Elasticsearch
from influence_appendix import aggregation, proportion, filter_mid, weiboinfo2url
from user_portrait.global_utils import ES_CLUSTER_FLOW1 as es_cluster
from user_portrait.global_utils import es_user_profile as es_profile
from user_portrait.global_utils import es_user_portrait as es_user_portrait
from user_portrait.time_utils import datetime2ts, ts2datetime, ts2date
#from influence_conclusion import retweeted_threshould, comment_threshould, influence_tag
from user_portrait.parameter import INFLUENCE_RETWEETED_THRESHOLD as retweeted_threshold
from user_portrait.parameter import INFLUENCE_COMMENT_THRESHOLD as comment_threshold
from user_portrait.parameter import INFLUENCE_TAG as influence_tag
from user_portrait.parameter import pre_influence_index as pre_index
from user_portrait.parameter import influence_doctype
from user_portrait.parameter import BCI_LIST, INFLUENCE_TOTAL_THRESHOULD, INFLUENCE_TOTAL_LIST, INFLUENCE_BRUST_THRESHOULD, INFLUENCE_BRUST_LIST
from user_portrait.parameter import CURRNET_INFLUENCE_THRESHOULD, CURRENT_INFLUENCE_CONCLUSION, INFLUENCE_TOTAL_CONCLUSION, INFLUENCE_BRUST_CONCLUSION, UNDERLINE_CONCLUSION
from user_portrait.global_utils import portrait_index_name as user_portrait
from user_portrait.global_utils import es_flow_text as es
from user_portrait.global_utils import flow_text_index_name_pre as pre_text_index
from user_portrait.global_utils import portrait_index_type, flow_text_index_type, profile_index_type, profile_index_name
uid_url = 'http://weibo.com/u/'


user_portrait = "user_portrait_1222"
#es = Elasticsearch("219.224.135.93:9206", timeout=60)
influence_date = ts2datetime(time.time())
index_name = pre_index + influence_date.replace("-","")
index_name = "bci_20130901" # test
index_flow_text = pre_text_index + influence_date
index_flow_text = "flow_text_2013-09-01"



# get user influence of determined date
# date: 2013-09-01
def get_user_influence(uid, date):
    date = str(date).replace("-","")
    index_name = pre_index + date
    try:
        bci_info = es_cluster.get(index=index_name, doc_type=influence_doctype, id=uid)["_source"]
    except:
        bci_info = {}
    result = {}
    for key in BCI_LIST:
        result[key] = bci_info.get(key, 0)

    user_index = result["user_index"]
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "range":{
                        "user_index":{
                            "gt": user_index
                        }
                    }
                }
            }
        }
    }
    total_count = es_cluster.count(index=index_name, doc_type=influence_doctype)['count']
    order_count = es_cluster.count(index=index_name, doc_type=influence_doctype, body=query_body)['count']

    result["total_count"] = total_count
    result["order_count"] = order_count + 1

    return result


def get_text(top_list, date, user_info, style):

# input: [[mid1, no.1], [mid2, no.2], ['mid3', no.3]]
# output: [[text1, no.1], [text2, no.2], [text3, no.3]]
# mid, retweeted, comment, text, geo, timestamp, sentiment, mid_url
    results = []
    detail_list = ["origin_weibo_retweeted_detail", "origin_weibo_comment_detail", "retweeted_weibo_retweeted_detail", "retweeted_weibo_comment_detail"]
    index_flow_text = pre_text_index + date
    if len(top_list) != 0: # no one
        mid_list = []
        for i in range(len(top_list)):
            mid_list.append(top_list[i][0])
        search_result = es.mget(index=index_flow_text, doc_type=flow_text_index_type, body={"ids":mid_list})["docs"]
        for i in range(len(top_list)):
            temp = []
            temp.append(mid_list[i])
            if int(style) == 0:
                temp.append(top_list[i][1])
                temp.append(json.loads(user_info[detail_list[1]]).get(top_list[i][0], 0))
            elif int(style) == 1:
                temp.append(json.loads(user_info[detail_list[0]]).get(top_list[i][0], 0))
                temp.append(top_list[i][1])
            elif int(style) == 2:
                temp.append(top_list[i][1])
                temp.append(json.loads(user_info[detail_list[3]]).get(top_list[i][0], 0))
            else:
                temp.append(json.loads(user_info[detail_list[2]]).get(top_list[i][0], 0))
                temp.append(top_list[i][1])
            if search_result[i]["found"]:
                source = search_result[i]["_source"]
                temp.append(source["text"])
                temp.append(source["geo"])
                temp.append(ts2date(source["timestamp"]))
                temp.append(source["sentiment"])
                temp.append(weiboinfo2url(source['uid'], source['mid']))
                temp.append(uid_url+source['uid'])
                temp.append(source['uid'])
                try:
                    uname = es_profile.get(index=profile_index_name, doc_type=profile_index_type, id=source['uid'])["_source"]["nick_name"]
                    temp.append(uname)
                except:
                    temp.append("unknown")
            else:
                temp.extend(["", "", "", "", "", "", "", ""])
            results.append(temp)
    return results



# top retweeted or commentted weibo context
# date: 20130901
# uid
# style: 0--origin retweeted, 1--origin comment, 2--retweeted-retweeted, 3 --retweeted comment
# return context and number 
def influenced_detail(uid, date, style):
    date1 = str(date).replace('-', '')
    index_name = pre_index + date1
    #detail_text = {}
    style = int(style)
    try:
        user_info = es_cluster.get(index=index_name, doc_type=influence_doctype, id=uid)["_source"]
    except:
        result = {}
        return result
    origin_retweetd = json.loads(user_info["origin_weibo_retweeted_top"])
    origin_comment = json.loads(user_info['origin_weibo_comment_top'])
    retweeted_retweeted = json.loads(user_info["retweeted_weibo_retweeted_top"])
    retweeted_comment = json.loads(user_info["retweeted_weibo_comment_top"])

    if style == 0:
        detail_text = get_text(origin_retweetd, date, user_info, style)
    elif style == 1:
        detail_text = get_text(origin_comment, date, user_info, style)
    elif style == 2:
        detail_text = get_text(retweeted_retweeted, date, user_info, style)
    else:
        detail_text = get_text(retweeted_comment, date, user_info, style)
    #detail_text["origin_retweeted"] = get_text(origin_retweetd, date)
    #detail_text["origin_comment"] = get_text(origin_comment, date)
    #detail_text["retweeted_retweeted"] = get_text(retweeted_retweeted, date)
    #detail_text["retweeted_comment"] = get_text(retweeted_comment, date)

    return detail_text

def get_user_url(uid_list):
    results = []
    try:
        es_results = es_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={"ids": uid_list})['docs']
    except:
        es_results = {}
    for item in es_results:
        temp = []
        if item['found']:
            temp.append(item['_source']["photo_url"])
            temp.append(item['_source']['nick_name'])
            temp.append(item['_id'])
        else:
            temp.append("unknown")
            temp.append("unknown")
            temp.append(item['_id'])
        results.append(temp)
    return results

def influenced_people(uid, mid, influence_style, date, default_number=20):
# uid 
# which weibo----mid, retweeted weibo ---seek for root_mid
# influence_style: retweeted(0) or comment(1)
    date1 = str(date).replace('-', '')
    index_name = pre_index + date1
    index_flow_text = pre_text_index + date
    text_result = es.get(index=index_flow_text, doc_type=flow_text_index_type, id=mid)["_source"]
    temp_mid = text_result.get("root_mid",'') #判断微博是否是原创微博
    print temp_mid
    if temp_mid:
        mid_type = 1 # 非原创微博
    else:
        mid_type = 0 # 原创微博
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                        ]
                    }
                }
            }
        },
        "size": 100000
    }

    if mid_type == 0:
        if int(influence_style) == 0: # origin weibo, all retweeted people
            query_body["query"]["filtered"]["filter"]["bool"]["must"].extend([{"term": {"root_uid": uid}}, {"term": {"message_type": 3}}, {"term": {"root_mid": mid}}])
        else: # commented people
            query_body["query"]["filtered"]["filter"]["bool"]["must"].extend([{"term": {"directed_uid": uid}}, {"term": {"message_type": 2}}, {"term": {"root_mid": mid}}])
    else:
        if int(influence_style) == 0: # origin weibo, all retweeted people
            query_body["query"]["filtered"]["filter"]["bool"]["must"].extend([{"term": {"directed_uid": uid}}, {"term": {"message_type": 3}}, {"term": {"root_mid": temp_mid}}])
        else: # commented people
            query_body["query"]["filtered"]["filter"]["bool"]["must"].extend([{"term": {"directed_uid": uid}}, {"term": {"message_type": 2}}, {"term": {"root_mid": temp_mid}}])
    search_results = es.search(index=index_flow_text, doc_type=flow_text_index_type, body=query_body, fields=["uid"], timeout=30)["hits"]["hits"]
    results = []
    if search_results:
        for item in search_results:
            if int(item["fields"]["uid"][0]) == int(uid):
                pass
            else:
                results.append(item["fields"]["uid"][0])
        results = list(set(results))
    else:
        results = []


    if results:
        portrait_results = es_user_portrait.mget(index=user_portrait, doc_type=portrait_index_type, body={"ids": results}, fields=["domain", "topic_string", "activity_geo_dict","importance", "influence"])["docs"]
    else:
        portrait_results = {}


    in_portrait = []
    out_portrait = []
    in_portrait_info = []
    retweeted_domain = {}
    retweeted_topic = {}
    retweeted_geo = {}
    average_influence = 0
    total_influence = 0
    count = 0

    if portrait_results:
        for item in portrait_results:
            if item["found"]:
                temp = []
                count += 1
                temp.append(item['_id'])
                temp.append(item["fields"]["importance"][0])
                in_portrait.append(temp)
                temp_domain = item["fields"]["domain"][0].split('&')
                temp_topic = item["fields"]["topic_string"][0].split('&')
                temp_geo = json.loads(item["fields"]["activity_geo_dict"][0])[-1].keys()
                total_influence += item["fields"]["influence"][0]
                retweeted_domain = aggregation(temp_domain, retweeted_domain)
                retweeted_topic = aggregation(temp_topic, retweeted_topic)
                retweeted_geo = aggregation(temp_geo, retweeted_geo)
            else:
                out_portrait.append(item['_id'])
        retweeted_domain = proportion(retweeted_domain)
        retweeted_topic = proportion(retweeted_topic)
        retweeted_geo = proportion(retweeted_geo)
        try:
            average_influence = total_influence/count
        except:
            average_influence = 0
    sorted_retweeted_domain = sorted(retweeted_domain.items(),key=lambda x:x[1], reverse=True)
    sorted_retweeted_topic = sorted(retweeted_topic.items(),key=lambda x:x[1], reverse=True)
    sorted_retweeted_geo = sorted(retweeted_geo.items(), key=lambda x:x[1], reverse=True)

    retweeted_results = dict()
    retweeted_results["domian"] = sorted_retweeted_domain[:5]
    retweeted_results["topic"] = sorted_retweeted_topic[:5]
    retweeted_results["geo"] = sorted_retweeted_geo[:5]
    retweeted_results["influence"] = average_influence
    in_portrait = sorted(in_portrait, key=lambda x:x[1], reverse=True)


    temp_list = []
    for item in in_portrait:
        temp_list.append(item[0])
    print temp_list[:20]
    print out_portrait[:20]
    retweeted_results['in_portrait_number'] = len(temp_list)
    retweeted_results['out_portrait_number'] = len(out_portrait)
    in_portrait_url = get_user_url(temp_list[:default_number])
    out_portrait_url = get_user_url(out_portrait[:default_number])

    return_results = dict()
    return_results["influence_users"] = [in_portrait_url, out_portrait_url]
    return_results["influence_distribution"] = retweeted_results


    return return_results





    return ([in_portrait_url[:default_number], out_portrait_url[:default_number]])


# 给定所有转发微博的mid,计算影响到的人的领域、话题、地理位置
def influenced_user_detail(uid, date, origin_retweeted_mid, retweeted_retweeted_mid, message_type, default_number=20):
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "should":[
                        ],
                        "must": [
                        ]
                    }
                }
            }
        },
        "size":10000
    }
    #详细影响到的人 
    date1 = str(date).replace('-', '')
    index_name = pre_index + date1
    index_flow_text = pre_text_index + date
    origin_retweeted_uid = [] # influenced user uid_list
    retweeted_retweeted_uid = []
    origin_comment_uid = []
    retweeted_comment_uid = []
    if origin_retweeted_mid: # 所有转发该条原创微博的用户
        length = len(origin_retweeted_mid)
        if length != 1:
            for iter_mid in origin_retweeted_mid:
                query_body["query"]["filtered"]["filter"]["bool"]["should"].append({"term": {"root_mid": iter_mid}})
        else:
            iter_mid = origin_retweeted_mid[0]
            query_body["query"]["filtered"]["filter"]["bool"]["must"].append({"term": {"root_mid": iter_mid}})
        query_body["query"]["filtered"]["filter"]["bool"]["must"].extend([{"term":{"message_type": message_type}}, {"term":{"root_uid": uid}}])
        origin_retweeted_result = es.search(index=index_flow_text, doc_type=flow_text_index_type, body=query_body, fields=["uid"])["hits"]["hits"]
        if origin_retweeted_result:
            for item in origin_retweeted_result:
                origin_retweeted_uid.append(item["fields"]["uid"][0])
    if retweeted_retweeted_mid: # 所有评论该条原创微博的用户
        length = len(retweeted_retweeted_mid)
        if length != 1:
            for iter_mid in retweeted_retweeted_mid:
                query_body["query"]["filtered"]["filter"]["bool"]["should"].append({"term": {"root_mid": iter_mid}})
        else:
            iter_mid =retweeted_retweeted_mid[0]
            query_body["query"]["filtered"]["filter"]["bool"]["must"].append({"term": {"root_mid": iter_mid}})
        query_body["query"]["filtered"]["filter"]["bool"]["must"].extend([{"term":{"message_type": message_type}},{"term": {"directed_uid": uid}}])
        retweeted_retweeted_result = es.search(index=index_flow_text, doc_type=flow_text_index_type, body=query_body, fields=["uid"])["hits"]["hits"]
        if retweeted_retweeted_result:
            for item in retweeted_retweeted_result:
                retweeted_retweeted_uid.append(item["fields"]["uid"][0])
    retweeted_uid_list = [] # all retweeted user list
    retweeted_results = {} # statistics of all retweeted uid information
    retweeted_domain = {}
    retweeted_topic = {}
    retweeted_geo = {}
    in_portrait = []
    out_portrait = []
    average_influence = 0
    total_influence = 0
    count = 0
    retweeted_uid_list.extend(origin_retweeted_uid)
    retweeted_uid_list.extend(retweeted_retweeted_uid)
    retweeted_uid_list = list(set(retweeted_uid_list) - set([uid])) # filter uids
    if retweeted_uid_list:
        user_portrait_result = es_user_portrait.mget(index=user_portrait, doc_type=portrait_index_type, body={"ids": retweeted_uid_list}, fields=["domain", "topic_string", "activity_geo_dict","importance", "influence"])["docs"]
        for item in user_portrait_result:
            if item["found"]:
                temp = []
                count += 1
                temp.append(item['_id'])
                temp.append(item["fields"]["importance"][0])
                in_portrait.append(temp)
                temp_domain = item["fields"]["domain"][0].split('&')
                temp_topic = item["fields"]["topic_string"][0].split('&')
                temp_geo = json.loads(item["fields"]["activity_geo_dict"][0])[-1].keys()
                total_influence += item["fields"]["influence"][0]
                retweeted_domain = aggregation(temp_domain, retweeted_domain)
                retweeted_topic = aggregation(temp_topic, retweeted_topic)
                retweeted_geo = aggregation(temp_geo, retweeted_geo)
            else:
                out_portrait.append(item['_id'])
        retweeted_domain = proportion(retweeted_domain)
        retweeted_topic = proportion(retweeted_topic)
        retweeted_geo = proportion(retweeted_geo)
        try:
            average_influence = total_influence/count
        except:
            average_influence = 0
    sorted_retweeted_domain = sorted(retweeted_domain.items(),key=lambda x:x[1], reverse=True)
    sorted_retweeted_topic = sorted(retweeted_topic.items(),key=lambda x:x[1], reverse=True)
    sorted_retweeted_geo = sorted(retweeted_geo.items(), key=lambda x:x[1], reverse=True)
    retweeted_results["domian"] = sorted_retweeted_domain[:5]
    retweeted_results["topic"] = sorted_retweeted_topic[:5]
    retweeted_results["geo"] = sorted_retweeted_geo[:5]
    retweeted_results["influence"] = average_influence
    in_portrait = sorted(in_portrait, key=lambda x:x[1], reverse=True)

    temp_list = []
    for item in in_portrait:
        temp_list.append(item[0])
    #print temp_list[:20]
    #print out_portrait[:20]
    retweeted_results['in_portrait_number'] = len(temp_list)
    retweeted_results['out_portrait_number'] = len(out_portrait)
    in_portrait_url = get_user_url(temp_list[:default_number])
    out_portrait_url = get_user_url(out_portrait[:default_number])
    retweeted_results["in_portrait"] = in_portrait_url
    retweeted_results["out_portrait"] = out_portrait_url

    return retweeted_results


# 用于调用，某条微博的影响力，人和分布
# style: 转发或者评论的类型
def detail_weibo_influence(uid, mid, style, date, number):
    results = dict()
    date1 = str(date).replace('-', '')
    index_name = pre_index + date1
    text_index = pre_text_index + date
    results = influenced_people(uid, mid, style, date, number)

    return results


def statistics_influence_people(uid, date, style):
    # output: different retweeted and comment, uids' domain distribution, topic distribution, registeration geo distribution
    results = {} # retwweted weibo people and comment weibo people
    date1 = str(date).replace('-', '')
    index_name = pre_index + date1
    index_flow_text = pre_text_index + date

    try:
        bci_result = es_cluster.get(index=index_name, doc_type=influence_doctype, id=uid)["_source"]
    except:
        bci_result = []
        return results
    origin_retweeted_mid = [] # origin weibo mid
    retweeted_retweeted_mid = [] # retweeted weibo mid
    origin_comment_mid = []
    retweeted_comment_mid = []
    origin_retweeted = json.loads(bci_result["origin_weibo_retweeted_detail"])
    retweeted_retweeted = json.loads(bci_result["retweeted_weibo_retweeted_detail"])
    origin_comment = json.loads(bci_result["origin_weibo_comment_detail"])
    retweeted_comment = json.loads(bci_result["retweeted_weibo_comment_detail"])
    retweeted_total_number = sum(origin_retweeted.values()) + sum(retweeted_retweeted.values())
    comment_total_number = sum(origin_comment.values()) + sum(retweeted_comment.values())
    if origin_retweeted:
        origin_retweeted_mid = filter_mid(origin_retweeted)
    if retweeted_retweeted:
        retweeted_retweeted_mid = filter_mid(retweeted_retweeted)
    if origin_comment:
        origin_comment_mid = filter_mid(origin_comment)
    if retweeted_comment:
        retweeted_comment_mid = filter_mid(retweeted_comment)

    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "should":[
                        ],
                        "must": [
                        ]
                    }
                }
            }
        },
        "size":10000
    }


    if int(style) == 0: # retweeted
        retweeted_origin = []
        if retweeted_retweeted_mid:
            text_result = es.mget(index=index_flow_text, doc_type=flow_text_index_type, body={"ids": retweeted_retweeted_mid})["docs"]
            for item in text_result:
                mid = item.get("source", {}).get("root_mid", '0')
                retweeted_origin.append(mid)
        retweeted_results = influenced_user_detail(uid, date, origin_retweeted_mid, retweeted_origin, 3)
        retweeted_results["total_number"] = retweeted_total_number
        results = retweeted_results
    else:
        retweeted_origin = []
        if retweeted_comment_mid:
            text_result = es.mget(index=index_flow_text, doc_type=flow_text_index_type, body={"ids": retweeted_comment_mid})["docs"]
            for item in text_result:
                mid = item.get("source", {}).get("root_mid", '0')
                retweeted_origin.append(mid)
        comment_results = influenced_user_detail(uid, date, origin_comment_mid, retweeted_origin, 2)
        comment_results["total_number"] = comment_total_number
        results = comment_results

    return results


def tag_vector(uid, date):
    date1 = str(date).replace('-', '')
    index_name = pre_index + date1
    index_flow_text = pre_text_index + date
    result = []

    try:
        bci_result = es_cluster.get(index=index_name, doc_type=influence_doctype, id=uid)["_source"]
    except:
        tag = influence_tag["0"]
        result.append(tag)
        return result

    origin_retweeted = json.loads(bci_result["origin_weibo_retweeted_detail"])
    retweeted_retweeted = json.loads(bci_result["retweeted_weibo_retweeted_detail"])
    origin_comment = json.loads(bci_result["origin_weibo_comment_detail"])
    retweeted_comment = json.loads(bci_result["retweeted_weibo_comment_detail"])
    sum_retweeted = sum(origin_retweeted.values()) + sum(origin_comment.values())
    sum_comment = sum(retweeted_retweeted.values()) + sum(retweeted_comment.values())

    if sum_retweeted >= retweeted_threshold:
        if sum_comment >= comment_threshold:
            tag = influence_tag['3']
        else:
            tag = influence_tag['1']
    else:
        if sum_comment >= comment_threshold:
            tag = influence_tag['2']
        else:
            tag = influence_tag['4']
    result.append(tag)
    return result


def comment_on_influence(uid, date):
    date1 = str(date).replace('-', '')
    index_name = pre_index + date1
    index_flow_text = pre_text_index + date
    result = []
    underline = []

    try:
        bci_result = es_cluster.get(index=index_name, doc_type=influence_doctype, id=uid)["_source"]
    except:
        description = CURRENT_INFLUENCE_CONCLUSION['0']
        result.append(description)
        return ([result, underline])

    user_index = bci_result['user_index']
    if user_index < CURRNET_INFLUENCE_THRESHOULD[0]:
        description = CURRENT_INFLUENCE_CONCLUSION['0']
    elif user_index >= CURRNET_INFLUENCE_THRESHOULD[0] and user_index < CURRNET_INFLUENCE_THRESHOULD[1]:
        description = CURRENT_INFLUENCE_CONCLUSION['1']
    elif user_index >= CURRNET_INFLUENCE_THRESHOULD[1] and user_index < CURRNET_INFLUENCE_THRESHOULD[2]:
        description = CURRENT_INFLUENCE_CONCLUSION['2']
    elif user_index >= CURRNET_INFLUENCE_THRESHOULD[2] and user_index < CURRNET_INFLUENCE_THRESHOULD[3]:
        description = CURRENT_INFLUENCE_CONCLUSION['3']
    elif user_index >= CURRNET_INFLUENCE_THRESHOULD[3] and user_index < CURRNET_INFLUENCE_THRESHOULD[4]:
        description = CURRENT_INFLUENCE_CONCLUSION['4']
    else:
        description = CURRENT_INFLUENCE_CONCLUSION['5']
    result.append(description)

    for i in range(4):
        if bci_result[INFLUENCE_TOTAL_LIST[i]] > INFLUENCE_TOTAL_THRESHOULD[i]:
            result.append(INFLUENCE_TOTAL_CONCLUSION[i])
            if bci_result[INFLUENCE_BRUST_LIST[i]] > INFLUENCE_BRUST_THRESHOULD[i]:
                result.append(INFLUENCE_BRUST_CONCLUSION[i])
                underline.append(UNDERLINE_CONCLUSION[i])
            else:
                result.append('')
                underline.append('')
        else:
            result.extend(['',''])
            underline.append('')

    return [result, underline]


def influence_summary(uid, date):
    result = []
    current_influence = comment_on_influence(uid, date)
    result.append([current_influence[0][0]])
    result.append(current_influence[1])

    retweeted_result = statistics_influence_people(uid, date, 0)
    comment_result = statistics_influence_people(uid, date, 1)
    domain = set()
    topic = set()
    if retweeted_result:
        for item in retweeted_result["domian"]:
            domain.add(item[0])
        for item in retweeted_result["topic"]:
            topic.add(item[0])
    if comment_result:
        for item in comment_result["domian"]:
            domain.add(item[0])
        for item in comment_result["topic"]:
            topic.add(item[0])
    result.append(list(domain))
    result.append(list(topic))
    #print result
    return result

if __name__ == "__main__":
    #print influenced_detail("3396850362", "20130901")
    #print get_text([["3617510756389302",10],["3617510748726939", 5], ["617510752637061", 3]])
    #print influenced_people("2758565493","3616273092968593",0)
    #statistics_influence_people("2796627290")
    #print tag_vector("33711188092")
    print get_user_influence("3286115545", "20130902")
