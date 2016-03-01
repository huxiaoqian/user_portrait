# -*- coding:UTF-8 -*-
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

index_info = {
    'settings':{
        'number_of_shards':5,
        'number_of_replicas':0,
        },
    'mappings':{
        'group':{
            'properties':{
                'task_name':{
                    'type':'string',
                    'index': 'not_analyzed'
                    },
                'state':{
                    'type':'string',
                    'index': 'not_analyzed'
                    },
                'status':{
                    'type':'long'
                    },
                'submit_date':{
                    'type': 'long'
                    },
                'submit_user':{
                    'type': 'string',
                    'index': 'not_analyzed'
                    },
                'task_type':{
                    'type': 'string',
                    'index': 'not_analyzed'
                    },
                'detect_type':{
                    'type': 'string',
                    'index': 'not_analyzed'
                    },
                'detect_process':{
                    'type': 'long'
                    },
                'query_condition':{
                    'type': 'string',
                    'index': 'not_analyzed'
                    },
                'uid_list':{
                    'type': 'string',
                    'index': 'not_analyzed'
                    },
                'count':{
                    'type': 'long'
                    },
                'status':{
                    'type': 'long'
                    },
                'test_field':{
                    'type': 'string',
                    'index': 'not_analyzed'
                    }
                }
            }
        }
    }

es = Elasticsearch('219.224.134.213')

#es.indices.create(index='group_result', body=index_info, ignore=400)
es.indices.put_mapping(index='group_result', doc_type='group', \
        body={'properties':{'test_field':{'type':'string', 'index':'not_analyzed'}}}, ignore=400)

