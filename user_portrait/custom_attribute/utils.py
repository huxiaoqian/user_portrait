# -*- coding: UTF-8 -*-
import json
import time
from user_portrait.global_utils import es_user_portrait as es
from user_portrait.time_utils import ts2datetime, datetime2ts

attribute_index_name = 'custom_attribute'
attribute_index_type = 'attribute'

user_index_name = 'user_portrait'
user_index_type = 'user'

attribute_dict_key = ['attribute_value', 'attribute_user', 'date', 'user']


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

# use to change attribtue
def change_attribute(attribute_name, value, user, state):
    status = False
    # identify the attribute_name is in ES - custom attribute
    try:
        result =  es.get(index=attribute_index_name, doc_type=attribute_index_type, id=attribute_name)['_source']
    except:
        result = None
        return status
    value_list = value.split('&')
    result['value'] = json.dumps(value_list)
    result['user'] = user
    result['state'] = state
    now_ts = time.time()
    now_date = ts2datetime(now_ts)
    result['date'] = now_date
    es.index(index=attribute_index_name, doc_type=attribute_index_type, body=result)
    status = True
    return status

# use to delete attribute
def delete_attribute(attribute_name):
    status = False
    try:
        result = es.get(index=attribute_index_name, doc_type=attribute_index_type, id=attribute_name)['_source']
    except:
        return status
    attribute_value = json.loads(result['value'])
    es.delete(index=attribute_index_name, doc_type=attribute_index_type, id=attribute_name)
    # delete attribute in user_portrait
    query = []
    for value in attribute_value:
        query.append({'match':{attribute_name: value}})
    try:
        attribute_user_result = es.search(index=user_index_name, doc_type=user_index_type, \
                                         body={'query':{'bool':{'must':query}}})['hits']['hits']
    except:
        attribute_user_result = []
    if attribute_user_result==[]:
        status = True
        return status
    bulk_action = []
    for user_dict in attribute_user_result:
        try:
            user_item = user_dict['_source']
        except:
            next
        user_item.pop(attribute)
        user = user_item['uid']
        action = {'index':{'_id':str(user)}}
        bulk_action.extend([action, user_item])
    es.bulk(bulk_action, index=user_index_name, doc_type=index_type)
    status = True
    return status

# use to add attribute to user in es_user_portrait
def add_attribute_portrait(uid, attribute_name, attribute_value, submit_user):
    status = False
    # identify the user exist
    # identify the attribute exist
    # identify the attribute exist in user_portrait
    # add attribute in user_portrait
    # submit user should has power to change???without
    try:
        user_result = es.get(index=user_index_name, doc_type=user_index_type, id=uid)['_source']
    except:
        return 'no user'
    try:
        attribute_result = es.get(index=attribute_index_name, doc_type=user_index_type, id=attribute_name)['_source']
    except:
        return 'no attribute'
    attribute_value_list = json.loads(attribute_result['value'])
    if attribute_value not in attribute_value_list:
        return 'no attribute value'
    if attribute_name in user_result:
        return 'attribute exist'
    add_attribute_dict = {attribute_name: attribute_value}
    
    es.update(index=user_index_name, doc_type=user_index_type, id=uid, body={'doc':body})
    status = True
    return status

# use to change attribute of user in es_user_portrait
def change_attribute_portrait(uid, attribute_name, attribute_value, submit_user):
    status = False
    #identify the user exist
    #identify the attribute exist
    #identify the attribute value exist
    #identify the submit_user have been admitted----without 
    try:
        user_exist = es.get(index=user_index_name, doc_type=user_index_type, id=uid)['_source']
    except:
        return 'no user'
    try:
        attribute_result = es.get(index=attribute_index_name, doc_type=user_index_type, id=uid)['_source']
    except:
        return 'no attribute'
    value_list = json.loads(attribute_result['value'])
    if attribute_value not in value_list:
        return 'no attribute value'
    es.update(index=user_index_name, doc_type=user_index_type, id=uid, body={'doc':body})
    status = True
    return status

# use to delete attribute of user in es_user_portrait
def delete_attribute_portrait(uid, attribute_name, submit_user):
    status = False
    #identify the user exist
    #identify the attribute value exist in es_user_portrait
    #identify the submit_user have been admitted---without
    try:
        user_exist = es.get(index=user_index_name, doc_type=user_index_type, id=uid)['_source']
    except:
        return 'no user'
    if attribute_name not in user_exist:
        return 'user have no attribtue'
    try:
        del_attribute_value = user_exist.pop(attribute)
        es.index(index=user_index_name, doc_type=user_index_type, body=user_exist)
        status = True
    except Exception, e:
        raise e

    return status

