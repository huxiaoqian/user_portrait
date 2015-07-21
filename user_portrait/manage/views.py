#-*- coding:utf-8 -*-

import os
import time
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from utils import compare_user_portrait, compare_user_activity, compare_user_profile
from utils import imagine
from user_portrait.time_utils import datetime2ts

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
    if uid:
        result = imagine(uid)
    if result:
        return json.dumps(result)
    else:
        return None
