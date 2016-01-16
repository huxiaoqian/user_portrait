# -*- coding:utf-8 -*-

import sys
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
reload(sys)
sys.path.append("./../")
from global_utils import es_user_portrait as es

current_sensing_info = {
    "mappings":{
        "task":{
            "properties":{
                "task_name":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "create_by":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "create_at":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "start_time":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "stop_time":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "remark":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "social_sensor":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "keywords":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "warming_status":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "history_warning":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "finish":{
                    "type": "string",
                    "index": "not_analyzed"
                }
            }
        }
    }
}

social_burst_sensing = {
    "mappings":{
        "warning":{
            "properties":{
                "origin_weibo_time_series":{
                    "type": "string",
                    "index": "no"
                },
                "retweeted_weibo_time_series":{
                    "type": "string",
                    "index": "no"
                },
                "comment_weibo_time_series":{
                    "type": "string",
                    "index": "no"
                },
                "sentiment_time_series":{
                    "type": "string",
                    "index": "no"
                },
                "important_users":{
                    "type": "string",
                    "index": "no"
                }
            }
        }
    }
}



es.indices.create(index="social_sensing_task", body=current_sensing_info, ignore=400)
es.indices.create(index="social_burst_sensing", body=social_burst_sensing, ignore=400)



