#-*- coding:utf-8 -*-

import os
import time
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from utils import get_attr

from user_portrait.time_utils import datetime2ts

# use to test 13-09-08
test_time = 1378569600
test_date = '2013-09-07'

mod = Blueprint('overview', __name__, url_prefix='/overview')

@mod.route('/show/')
def ajax_recommentation_in():
    date = request.args.get('date', '') # '2013-09-01'
    results = get_attr(date)
    return json.dumps(results)
