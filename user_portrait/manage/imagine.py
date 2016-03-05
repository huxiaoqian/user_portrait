# -*- coding:utf-8 -*-

import sys
import json
import math
from elasticsearch import Elasticsearch
from user_portrait.global_utils import es_user_portrait as es
from user_portrait.global_utils import portrait_index_name, portrait_index_type
from user_portrait.filter_uid import all_delete_uid

#use to get evaluate max
def get_evaluate_max():
    max_result = {}
    evaluate_index = ['influence', 'activeness', 'importance']
    for evaluate in evaluate_index:
        query_body = {
            'query':{
                'match_all':{}
                    },
                'size':1,
                'sort':[{evaluate: {'order': 'desc'}}]
                }
        try:
            result = es.search(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)['hits']['hits']
        except Exception, e:
            raise e
        max_evaluate = result[0]['_source'][evaluate]
        max_result[evaluate] = max_evaluate
    return max_result











"""
reload(sys)
sys.path.append('./../')
from global_utils import es_user_portrait as es
"""
def imagine(uid, query_fields_dict,index_name=portrait_index_name, doctype=portrait_index_type):

    """
    uid: search users relate to uid
    query_fields_dict: defined search field weight
    fields: domain, topic, keywords, psycho_status, psycho_feature, activity_geo, hashtag
    for example: "domain": 2
    domain, psycho_feature
    """
    personal_info = es.get(index=portrait_index_name, doc_type=portrait_index_type, id=uid, _source=True)['_source']

    keys_list = query_fields_dict.keys()
    keys_list.remove('field')
    keys_list.remove('size')

    search_dict = {}
    iter_list = []

    for iter_key in keys_list:
        if personal_info[iter_key] == '' or not personal_info[iter_key]:
            query_fields_dict.pop(iter_key)
        else:
            iter_list.append(iter_key)
            temp = personal_info[iter_key]
            search_dict[iter_key] = temp.split('&')

    if len(iter_list) == 0:
        return []

    query_body = {
        'query':{
            'function_score':{
                'query':{
                    'bool':{
                        'must':[
                        ]
                    }
                },
                "field_value_factor":{
                }
            }
        }
    }

    score_standard = {}
    score_standard["modifier"] = "log1p"
    if query_fields_dict['field'] == "activeness":
        score_standard['field'] = "activeness"
        score_standard['factor'] = 100
    elif query_fields_dict['field'] == "importance":
        score_standard['field'] = "importance"
        score_standard['factor'] = 0.01
    elif query_fields_dict['field'] == 'influence':
        score_standard['field'] = "influence"
        score_standard['factor'] = 0.1
    else:
        score_standard['field'] = "influence"
        score_standard['factor'] = 0
        query_body['query']['function_score']['boost_mode'] = "sum"

    query_body['query']['function_score']['field_value_factor'] = score_standard

    query_fields_dict.pop('field')
    number = es.count(index=index_name, doc_type=doctype, body=query_body)['count']
    query_body['size'] = 100 # default number
    query_number = query_fields_dict['size'] #  required number
    query_fields_dict.pop('size')

    for (k,v) in query_fields_dict.items():

        temp = {}
        temp_list = []
        for iter_key in search_dict[k]:
            temp_list.append({'wildcard':{k:{'wildcard':'*'+iter_key+'*','boost': v}}})

        query_body['query']['function_score']['query']['bool']['must'].append({'bool':{'should':temp_list}})

    filter_uid = all_delete_uid()

    result = es.search(index=index_name, doc_type=doctype, body=query_body)['hits']['hits']
    field_list = ['uid','uname', 'activeness','importance', 'influence']
    evaluate_index_list = ['activeness', 'importance', 'influence']
    return_list = []
    count = 0
    #get evaluate max to normal
    evaluate_max_dict = get_evaluate_max()
    for item in result:
        if uid == item['_id'] or uid in filter_uid:
            score = item['_score']
            continue
        info = []
        for field in field_list:
            if field in evaluate_index_list:
                value = item['_source'][field]
                normal_value = math.log(value / evaluate_max_dict[field] * 9 + 1, 10) * 100
            else:
                normal_value = item['_source'][field]
            info.append(normal_value)
        info.append(item['_score'])
        return_list.append(info)
        count += 1

        if count == query_number:
            break

    return_list.append(number)

    temp_list = []
    for field in field_list:
        temp_list.append(personal_info[field])

    results = []
    results.append(temp_list)
    results.extend(return_list)


    return results




if __name__ == '__main__':
    print imagine(2010832710, {'topic':1, 'keywords':2,'field':'default','size':11}, index_name='test_user_portrait', doctype='user')

