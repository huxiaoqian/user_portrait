#-*- coding:utf-8 -*-

import json
import time
import datetime
from user_portrait.time_utils import ts2datetime, ts2date
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect, make_response


mod = Blueprint('portrait', __name__, url_prefix='/index')


@mod.route('/')
def loading():

    return render_template('portrait/index.html')

@mod.route('/test/')
def test():

    return render_template('portrait/test_bubble.html')

@mod.route('/personal/')
def personal():

    return render_template('portrait/personal.html')
"""
@mod.route('/manage/')
def manage():
    return render_template('index/manage.html')
"""
