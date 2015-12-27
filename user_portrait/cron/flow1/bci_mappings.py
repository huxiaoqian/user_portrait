# -*- coding:utf-8 -*-
from elasticsearch import Elasticsearch

index_info = {
    "mappings":{
        "bci":{
            "properties":{
                "origin_weibo_retweeted_detail": {
                    "type": "string",
                    "index": "no"
                },
                "origin_weibo_retweeted_top": {
                    "type": "string",
                    "index": "no"
                },
                'origin_weibo_comment_detail': {
                    "type": "string",
                    "index": "no"
                },
                'origin_weibo_comment_top': {
                    "type": "string",
                    "index": "no"
                },
                'retweeted_weibo_retweeted_detail':{
                    "type": "string",
                    "index": "no"
                },
                'retweeted_weibo_retweeted_top':{
                    "type": "string",
                    "index": "no"
                },
                'retweeted_weibo_comment_detail': {
                    "type": "string",
                    "index": "no"
                }, 
                'retweeted_weibo_comment_top': {
                    "type": "string",
                    "index": "no"
                }, 
                'origin_weibo_retweeted_brust_n': {
                    "type": "string",
                    "index": "no"
                },
                'origin_weibo_retweeted_average_number': {
                    "type": "string",
                    "index": "not_analyzed"
                },
                'retweeted_weibo_comment_brust_n': {
                    "type": "string",
                    "index": "no"
                },
                'origin_weibo_comment_top_number': {
                    "type": "string",
                    "index": "not_analyzed"
                },
                'origin_weibo_comment_brust_average': {
                    "type": "string",
                    "index": "not_analyzed"
                },
                'retweeted_weibo_retweeted_brust_average': {
                    "type": "string",
                    "index": "not_analyzed"
                },
                'retweeted_weibo_top_retweeted_id': {
                    "type": "string",
                    "index": "no"
                },
                'retweeted_weibo_number': {
                    "type": "string",
                    "index": "not_analyzed"
                },
                'retweeted_weibo_comment_top_number': {
                    "type": "string",
                    "index": "not_analyzed"
                },
                'user_friendsnum': {
                    "type": "string",
                    "index": "not_analyzed"
                },
                'origin_weibo_top_comment_id': {
                    "type": "string",
                    "index": "no"
                },
                'retweeted_weibo_retweeted_total_number': {
                    "type": "string",
                    "index": "not_analyzed"
                },
                'retweeted_weibo_retweeted_average_number': {
                    "type": "string",
                    "index": "not_analyzed"
                },
                'origin_weibo_retweeted_total_number': {
                    "type": "string",
                    "index": "not_analyzed"
                },
                'retweeted_weibo_top_comment_id': {
                    "type": "string",
                    "index": "no"
                },
                'user_fansnum': {
                    "type": "string",
                    "index": "not_analyzed"
                },
                'origin_weibo_comment_brust_n': {
                    "type": "string",
                    "index": "no"
                },
                'origin_weibo_top_retweeted_id': {
                    "type": "string",
                    "index": "no"
                },
                'origin_weibo_comment_average_number': {
                    "type": "string",
                    "index": "not_analyzed"
                },
                'origin_weibo_retweeted_brust_average': {
                    "type": "string",
                    "index": "not_analyzed"
                },
                'origin_weibo_retweeted_top_number': {
                    "type": "string",
                    "index": "not_analyzed"
                },
                'comment_weibo_number': {
                    "type": "string",
                    "index": "not_analyzed"
                },
                'retweeted_weibo_retweeted_brust_n': {
                    "type": "string",
                    "index": "no"
                },
                'retweeted_weibo_retweeted_top_number': {
                    "type": "string",
                    "index": "not_analyzed"
                },
                'origin_weibo_number': {
                    "type": "string",
                    "index": "not_analyzed"
                },
                'retweeted_weibo_comment_total_number': {
                    "type": "string",
                    "index": "not_analyzed"
                },
                'retweeted_weibo_comment_brust_average': {
                    "type": "string",
                    "index": "not_analyzed"
                },
                'origin_weibo_comment_total_number': {
                    "type": "string",
                    "index": "not_analyzed"
                },
                'retweeted_weibo_comment_average_number': {
                    "type": "string",
                    "index": "not_analyzed"
                } 

            }
        }
    }
}


def mappings(es, index_name):
    es.indices.create(index=index_name, body=index_info, ignore=400)
    return 1








