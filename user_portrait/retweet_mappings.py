# -*- coding:UTF-8 -*-
import time
from elasticsearch import Elasticsearch
from global_utils import es_user_portrait as es
from time_utils import ts2datetime, datetime2ts


#use to mappings for retweet es
def retweet_es_mappings(db_number):
    index_info = {
            'settings':{
                'number_of_shards':5,
                'number_of_replicas':0
                },
            'mappings':{
                'user':{
                    'properties':{
                        'uid':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'uid_retweet':{
                            'type': 'string',
                            'index': 'no'
                            }
                        }
                    }
                }
             }
    index_name = '1225_retweet_'+db_number
    exist_indice = es.indices.exists(index=index_name)
    if exist_indice:
        es.indices.delete(index=index_name)
    es.indices.create(index=index_name, body=index_info, ignore=400)

    return True


#use to mappings for be_retweet es
def be_retweet_es_mappings(db_number):
    index_info = {
            'settings':{
                'number_of_shards': 5,
                'number_of_replicas':0
                },
            'mappings':{
                'user':{
                    'properties':{
                    'uid':{
                        'type': 'string',
                        'index': 'not_analyzed'
                        },
                    'uid_be_retweet':{
                        'type': 'string',
                        'index': 'no'
                        }
                    }
                    }
                }
        }
    index_name = '1225_be_retweet_'+db_number
    exist_indice = es.indices.exists(index=index_name)
    if exist_indice:
        es.indices.delete(index=index_name)

    es.indices.create(index=index_name, body=index_info, ignore=400)
    return True

if __name__=='__main__':
    #test
    db_number = '1'
    retweet_mark = retweet_es_mappings(db_number)
    be_retweet_mark = be_retweet_es_mappings(db_number)
