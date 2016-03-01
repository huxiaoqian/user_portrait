# -*- coding: UTF-8 -*-
import sys
import json
from user_portrait.global_utils import R_RECOMMENTATION as r

hash_name = 'overview'

rank_field = ['top_retweeted_user', 'top_comment_user', 'top_activeness', 'top_importance' ,\
              'hashtag_top', 'activity_geo_top', 'online_pattern_top']

def get_attr(date):
    results = {}
    overview_result = r.hgetall(hash_name)
    for item in overview_result:
        value = overview_result[item]
        if isinstance(value, str):
            value = json.loads(value)
        results[item] = value
    return results

def get_retweeted_top():
    overview_result = r.hgetall(hash_name)
    retweeted_top = json.loads(overview_result['top_retweeted_user'])
    return retweeted_top

def get_comment_top():
    overview_result = r.hgetall(hash_name)
    comment_top = json.loads(overview_result['top_comment_user'])
    return comment_top

def get_activeness_top():
    overview_result = r.hgetall(hash_name)
    activeness_top = json.loads(overview_result['top_activeness'])
    return activeness_top

def get_importance_top():
    overview_result = r.hgetall(hash_name)
    importance_top = json.loads(overview_result['top_importance'])
    return importance_top

def get_hashtag_top():
    overview_result = r.hgetall(hash_name)
    hashtag_top = json.loads(overview_result['hashtag_top'])
    return hashtag_top

def get_geo_top():
    overview_result = r.hgetall(hash_name)
    geo_top = json.loads(overview_result['activity_geo_top'])
    return geo_top

def get_online_pattern():
    overview_result = r.hgetall(hash_name)
    online_pattern = json.loads(overview_result['online_pattern_top'])
    return online_pattern
