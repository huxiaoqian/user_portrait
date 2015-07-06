#-*- coding:utf-8 -*-

import os
import time
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from search import search_recommentation_in

from global_config.time_utils import datetime2ts

# use to test 13-09-08
test_time = 1378569600
test_date = '2013-09-08'

mod = Blueprint('recommentation', __name__, url_prefix='/recommentation')

@mod.route('/in/')
def ajax_recommentation_in():
    date = request.args.get('date', '') # '2013-09-01'
    # test
    date = test_date 
    input_ts = datetime2ts(date)
    now_ts = time.time()
    #
    now_ts = test_time
    if now_ts - 3600*24*7 > input_ts:
        return None
    else:
        results = search_recommentation_in(input_ts)

        return json.dumps(results)

@mod.route('/out/')
def ajax_recommentation_out():
    results = dict()
    return json.dumps(results)
