#-*- coding:utf-8 -*-

import os
import time
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from utils import compare_user_portrait, compare_user_activity, compare_user_profile
from utils import imagine
from user_portrait.time_utils import datetime2ts
from imagine import imagine

mod = Blueprint('manage', __name__, url_prefix='/manage')

# compare the attr in the es_user_portrait
@mod.route('/compare_user_portrait/')
def ajax_compare_user_portrait():
    uid_list = request.args.get('uid_list', '') # uid_list = [uid1, uid2, uid3]
    if uid_list:
        results = compare_user_portrait(uid_list)
    if results:
        return json.dumps(results)
    else:
        return None

# compare the detail of activity attribute
# output data: {user:[weibo_count]}, {user:[(date, weibo)]}, ts_list
@mod.route('/compare_user_activity/')
def ajax_compare_user_activity():
    uid_list = request.args.get('uid_list', '') # uid_list = [uid1, uid2, uid3]
    if uid_list:
        results = compare_user_activity(uid_list)
    if result:
        return json.dumps(results)
    else:
        return None


# compare the detail of user profile
# output data: {user:{profile_information}}
@mod.route('/compare_user_profile/')
def ajax_user_profile():
    uid_list = request.args.get('uid_list', '')
    if uid_list:
        results = compare_user_profile(uid_list)
    if result:
        return json.dumps(results)
    else:
        return None


@mod.route('/imagine/')
def ajax_imagine():
    uid = request.args.get('uid', '') # uid
    query_fields_dict = request.args.get('query_fields_dict','') # query dict and corresponding weight
    keys_list = ['domain', 'topic', 'keywords', 'psycho_status', 'psycho_feature', 'activity_geo', 'hashtag']
    weight_list = ['domain_weight', 'topic_weight', 'keywords_weight', 'psycho_status_weight', 'psycho_feature_weight', 'activity_geo_weight', 'hashtag_weight']
    # 'field' control search order
    # order_list = ['importance', 'influence', 'activeness', 'default']

    query_fields_dict = {}
    for i in range(7):
        key = request.args.get(keys_list[i], '') # if not selected, key is set to ''
        value = request.args.get(weight_list[i], '')
        if key:
            query_fields_dict[keys_list[i]] = int(value)
    field = request.args.get('field', '')
    query_fields_dict['field'] = field

    size = request.args.get('size', 10)
    if size == "":
        size = 10
    query_fields_dict['size'] = int(size)

    if uid and query_fields_dict:
        result = imagine(uid, query_fields_dict)
    if result:
        return json.dumps(result)

    return None
