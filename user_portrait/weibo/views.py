#-*- coding:utf-8 -*-
import os
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from utils import get_user_weibo
from user_portrait.time_utils import ts2datetime, datetime2ts

mod = Blueprint('weibo', __name__, url_prefix='/weibo')

# use to show user weibo
@mod.route('/show_user_weibo/')
def ajax_show_user_weibo():
    uid = request.args.get('uid', '')
    user_weibo_result = get_user_weibo(uid)
    return json.dumps(user_weibo_result)
