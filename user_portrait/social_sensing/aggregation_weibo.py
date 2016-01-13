# -*- coding:utf-8 -*-


import sys
import time
import json
reload(sys)
sys.path.append("./../")
from global_utils import es_flow_text as es_text
from global_utils import es_user_profile as es_profile
from global_utils import es_user_portrait
from time_utils import ts2datetime, datetime2ts
from global_utils import flow_text_index_name_pre, flow_text_index_type, profile_index_name, profile_index_type, \
                         portrait_index_name, portrait_index_type

# aggragate weibo keywords of timestamp ts1 and ts2
def aggregation_range(ts1, ts2): 
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "range":{
                        "timestamp":{
                            "gte": ts1,
                            "lt": ts2
                        }
                    }
                }
            }
        },
        "aggs":{
            "all_interests":{
                "terms": {"field": "keywords_string",
                          "size": 100
                }
            }
        }
    }

    return query_body

# aggregate sentiment with a specified keyword or keywords----list
def aggregation_sentiment(ts1, ts2, keyword_list, aggregation_word, size=10):
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[{
                            "range":{
                                "timestamp":{
                                    "gte": ts1,
                                    "lt": ts2
                                }
                            }},
                            {"terms":{
                                "keywords_string": keyword_list
                            }
                        }]
                    }
                }
            }
        },
        "aggs":{
            "all_sentiment":{
                "terms":{"field": aggregation_word, "size": size}
            }
        }
    }

    return query_body


#聚合一段时间内特定社会传感器的微博的关键词
def aggregation_sensor_keywords(ts1, ts2, uid_list, aggregation_word, size=10):
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[{
                            "range":{
                                "timestamp":{
                                    "gte": ts1,
                                    "lt": ts2
                                }
                            }}
                        ],
                        "should":[
                        ]
                    }
                }
            }
        },
        "aggs":{
            "all_keywords":{
                "terms":{ "field": aggregation_word, "size": size}
            }
        }
    }

    if len(uid_list) == 0:
        pass
    elif len(uid_list) == 1:
        query_body["query"]["filtered"]["filter"]["bool"]["must"].append({"term": {"uid": uid_list[0]}})
    else:
        for iter_uid in uid_list:
            query_body["query"]["filtered"]["filter"]["bool"]["should"].append({"term": {"uid": iter_uid}})

    return query_body


def temporal_keywords(ts1, ts2):
    keywords_set = set()
    date = ts2datetime(time.time())
    date = "2013-09-07"
    index_date = flow_text_index_name_pre + date
    #search_results = es_text.search(index=index_date, doc_type=flow_text_index_type, body=aggregation_range(ts1, ts2))['aggregations']['all_interests']['buckets']
    search_results = es_text.search(index=index_date, doc_type=flow_text_index_type, body=aggregation_sentiment(ts1, ts2, ["水灾", "余姚", "洪水", "救灾"], "root_uid", 20))['aggregations']['all_sentiment']['buckets']

    # print keywords
    for item in search_results:
        print item["key"].encode("utf-8", "ignore"), item["doc_count"], "\n"
        #keywords_set.add(item["key"].encode("utf-8", "ignore"))

    return keywords_set


if __name__ == "__main__":

    temporal_keywords(1378531296, 1378531296+10*3600)



