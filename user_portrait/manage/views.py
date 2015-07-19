#-*- coding:utf-8 -*-

import os
import time
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from utils import compare, imagine
from user_portrait.time_utils import datetime2ts

mod = Blueprint('manage', __name__, url_prefix='/manage')

@mod.route('/compare/')
def ajax_compare():
    uid_list = request.args.get('uid_list', '') # uid_list = [uid1, uid2, uid3]
    if uid_list:
        results = compare(uid_list)
    if results:
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
