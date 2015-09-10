#-*- coding:utf-8 -*-
import os
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from utils import get_user_weibo, user_weibo_date, user_weibo_ts, get_group_weibo
from user_portrait.time_utils import ts2datetime, datetime2ts

mod = Blueprint('weibo', __name__, url_prefix='/weibo')

# use to show user weibo
@mod.route('/show_user_weibo/')
def ajax_show_user_weibo():
    uid = request.args.get('uid', '')
    user_weibo_result = get_user_weibo(uid)
    return json.dumps(user_weibo_result)

# use to show user weibo by date
@mod.route('/show_user_weibo_date/')
def ajax_show_weibo_date():
    uid = request.args.get('uid', '')
    date = request.args.get('date', '') # date = '2013-09-07'
    user_weibo = user_weibo_date(uid, date)
    return json.dumps(user_weibo)

# use to show user weibo by 4 hour
@mod.route('/show_user_weibo_ts/')
def ajax_show_weibo_ts():
    uid = request.args.get('uid', '')
    ts = request.args.get('ts', '') # ts=123456789
    user_weibo = user_weibo_ts(uid, ts)
    return json.dumps(user_weibo)

# use to show group weibo by date
@mod.route('/show_group_weibo/')
def ajax_show_group_weibo():
    task_name = request.args.get('task_name', '')
    date = request.args.get('date', '') # date = '2013-09-01'
    group_weibo = get_group_weibo(task_name, date)
    return json.dumps(group_weibo)
