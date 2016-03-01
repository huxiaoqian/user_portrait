#-*- coding:utf-8 -*-

import os
import time
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from utils import get_attr, get_retweeted_top, get_comment_top, get_activeness_top, get_importance_top, \
                  get_hashtag_top, get_geo_top, get_online_pattern

from user_portrait.time_utils import datetime2ts


mod = Blueprint('overview', __name__, url_prefix='/overview')

@mod.route('/show/')
def ajax_recommentation_in():
    date = request.args.get('date', '') # '2013-09-01'
    results = get_attr(date)
    if results:
        return json.dumps(results)
    else:
        return None

@mod.route('/retweeted_top_all/')
def ajax_influence_top():
    results = get_retweeted_top()
    if results:
        return json.dumps(results)
    else:
        return None

@mod.route('/comment_top_all/')
def ajax_comment_top():
    results = get_comment_top()
    if results:
        return json.dumps(results)
    else:
        return None

@mod.route('/activeness_top/')
def ajax_activeness_top():
    results = get_activeness_top()
    if results:
        return json.dumps(results)
    else:
        return None

@mod.route('/importance_top/')
def ajax_importance_top():
    results = get_importance_top()
    if results:
        return json.dumps(results)
    else:
        return None

@mod.route('/hashtag_top/')
def ajax_hashtag_top():
    results = get_hashtag_top()
    if results:
        return json.dumps(results)
    else:
        return None

@mod.route('/geo_all/')
def ajax_geo_top():
    results = get_geo_top()
    if results:
        return json.dumps(results)
    else:
        return None

@mod.route('/online_pattern/')
def ajax_online_pattern_all():
    results = get_online_pattern()
    if results:
        return json.dumps(results)
    else:
        return None

