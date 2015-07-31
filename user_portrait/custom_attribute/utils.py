# -*- coding: UTF-8 -*-
import json
import time
from user_portrait.global_utils import es_user_portrait as es
from user_portrait.time_utils import ts2datetime, datetime2ts

attribute_index_name = 'custom_attribute'
attribute_index_type = 'attribute'

user_index_name = 'user_portrait'
user_index_type = 'user'

attribute_dict_key = ['value', 'user', 'date', 'state']

# use to init the es of custom_attribute
def init_custom_attribute():
    index_info = {
        'settings':{
            'number_of_shards':5,
            'number_of_replicas':0
            },
        'mappings':{
            'user':{
                'properties':{
                    'attribute_name':{
                        'type': 'string',
                        'index': 'not_analyzed'
                        },
                    'attribute_value':{
                        'type': 'string',
                        'index': 'not_analyzed'
                        },
                    'date': {
                        'type': 'string',
                        'index': 'not_analyzed'
                        },
                    'user': {
                        'type': 'string',
                        'index': 'not_analyzed'
                        },
                    'state':{
                        'type': 'string',
                        'index': 'not_analyzed'
                        }
                    }
                }
            }
            }
    flag = es.indices.exists(index=attribute_index_name)
    if flag:
        es.indices.delete(index=attribute_index_name)
    es.indices.create(
        index=attribute_index_name,
        body=attribute_index_name,
        ignore = 400
        )

# use to submit attribute to es (custom_attribute, attribute)
def submit_attribute(attribute_name, attribute_value, submit_user, state):
    status = False
    #maybe there have to identify the user admitted to submit attribute
    attribute_exist = es.get(index=attribute_index_name, doc_type=attribute_index_type, id=attribute_name)['docs']
    try:
        source = attribute_exist['_source']
    except:
        input_data = dict()
        now_ts = time.time()
        date = ts2datetime(now_ts)
        input_data['name'] = attribute_name
        input_data['value'] = json.dumps(attribute_value.split('&'))
        input_data['user'] = submit_user
        input_data['state'] = state
        input_data['date'] = date
        es.index(index=attribute_index_name, doc_type=attribute_index_type, id=attribute_name, body=input_data)
        status = True
    return status

# use to search attribute table
def search_attribute(query_body, condition_num):
    result = []
    if condition_num==0:
        try:
            result = es.search(index=attribute_index_name, doc_type=attribute_index_type, \
                               body={'query':{'match_all':{}}})['hits']['hits']
        except Exception, e:
            raise e
    else:
        try:
            result = es.search(index=attribute_index_name, doc_type=attribute_index_type, \
                               body={'query':{'bool':{'must':query_body}}})['hits']['hits']
        except Exception, e:
            raise e
    if result:
        for item in result:
            source = item['_source']
            result.append(source)
    return result


if __name__=='__main__':
    init_custom_attribute()
