# -*- coding: utf-8 -*-
import sys
import json
from elasticsearch import Elasticsearch
from global_utils import es_tag as es
from global_utils import tag_index_name as attribute_index_name
from global_utils import tag_index_type as attribute_index_type

'''
es = Elasticsearch('219.224.134.213')

attribute_index_name = 'custom_attribute'
attribute_index_type = 'attribute'
'''
#custom attribute information
attribute_dict_key = ['attribute_name', 'attribute_value', 'date', 'user']

#use to init the es of custom_attribute
def init_custom_attribute():
    index_info = {
            'settings':{
                'analysis':{
                    'analyzer':{
                        'my_analyzer':{
                            'type': 'pattern',
                            'pattern': '&'
                            }
                        }
                    }
                },
            'mappings':{
                'attribute':{
                    'properties':{
                        'attribute_name':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'attribute_value':{
                            'type': 'string',
                            'analyzer': 'my_analyzer'
                            },
                        'date':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'user':{
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
            index = attribute_index_name,
            body = index_info,
            ignore = 400
            )
    #test
    es.index(index=attribute_index_name, doc_type=attribute_index_type, id='test_tag', body={'attribute_name':'test_tag', 'attribute_value':'tag1&tag2', 'date':'2013-09-08', 'user':'admin1'})


if __name__=='__main__':
    init_custom_attribute()

