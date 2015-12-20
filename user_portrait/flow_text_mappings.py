# -*- coding: UTF-8 -*-
'''
use to save text from flow_text --for all people 7day
'''
from elasticsearch import Elasticsearch
from global_utils import es_flow_text as es


def get_mappings(index_name):
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
                'text':{
                    'properties':{
                        'text':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'mid':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'ip':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'directed_uid':{
                            'type':'string',
                            'index': 'not_analyzed'
                            },
                        'directed_uname':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'timestamp':{
                            'type': 'long',
                            },
                        'sentiment': {
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'geo':{
                            'type': 'string',
                            'analyzer': 'my_analyzer'
                            },
                        'keywords_dict':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'keywords_string':{
                            'type': 'string',
                            'analyzer': 'my_analyzer'
                            },
                        'message_type':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'uid':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            }
                        }
                    }
                }
            }
    es.indices.create(index=index_name, body=index_info, ignore=400)
    #es.index(index=index_name, doc_type='text', id='test', body={'uid':'test'})

if __name__=='__main__':
    index_name = 'flow_text_2013-09-03'
    get_mappings(index_name)
