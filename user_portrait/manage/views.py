#-*- coding:utf-8 -*-

import os
import time
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from utils import compare_user_portrait, compare_user_activity, compare_user_profile
from utils import compare_user_portrait_new
from user_portrait.time_utils import datetime2ts
from imagine import imagine


mod = Blueprint('manage', __name__, url_prefix='/manage')

# compare the attr in the es_user_portrait
@mod.route('/compare_user_portrait/')
def ajax_compare_user_portrait():
    results = {}
    uid_string = request.args.get('uid_list', '') # uid_list = [uid1, uid2, uid3]
    uid_list = uid_string.split(',')
    if uid_list:
        results = compare_user_portrait_new(uid_list)
    if results:
        return json.dumps(results)
    else:
        return None


# compare the detail of activity attribute
# output data: {user:[weibo_count]}, {user:[(date, weibo)]}, ts_list
@mod.route('/compare_user_activity/')
def ajax_compare_user_activity():
    results = {}
    uid_string = request.args.get('uid_list', '') # uid_list = [uid1, uid2, uid3]
    uid_list = uid_string.split(',')
    if uid_list:
        results = compare_user_activity(uid_list)
    if results:
        return json.dumps(results)
    else:
        return None


# compare the detail of user profile
# output data: {user:{profile_information}}
@mod.route('/compare_user_profile/')
def ajax_user_profile():
    results = {}
    uid_string = request.args.get('uid_list', '')
    uid_list = uid_string.split(',')
    if uid_list:
        results = compare_user_profile(uid_list)
    if results:
        return json.dumps(results)
    else:
        return None


@mod.route('/imagine/')
def ajax_imagine():
    uid = request.args.get('uid', '') # uid
    query_keywords = request.args.get('keywords','') # query dict and corresponding weight
    keywords_list = query_keywords.split(',')
    query_weight = request.args.get('weight','')
    weight_list = query_weight.split(',')

    if len(keywords_list) != len(weight_list):
        return "0"

    # 'field' control search order
    # order_list = ['importance', 'influence', 'activeness', 'default']

    query_fields_dict = {}
    for i in range(len(keywords_list)):
        print type(keywords_list[i]), keywords_list[i]
        query_fields_dict[keywords_list[i]] = int(weight_list[i])
    field = request.args.get('field', '')
    query_fields_dict['field'] = field

    size = request.args.get('size', 15)
    query_fields_dict['size'] = int(size)

    if uid and query_fields_dict:
        result = imagine(uid, query_fields_dict)
    if result:
        return json.dumps(result)

    return "0"
