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

@mod.route('/overview/')
def overview():

    return render_template('portrait/overview.html')

@mod.route('/group_analysis/')
def group_analysis():

    return render_template('portrait/group_analysis.html')

@mod.route('/contrast/')
def contrast():

    return render_template('portrait/contrast.html')

@mod.route('/personal/')
def personal():

    return render_template('portrait/personal.html')

@mod.route('/recommend_in/')
def recommend_in():

    return render_template('portrait/recommend_in.html')

@mod.route('/recommend_out/')
def recommend_out():

    return render_template('portrait/recommend_out.html')

@mod.route('/search_result/')
def search_result():
    stype = request.args.get('stype', 1)
    if stype == 1:
        term = request.args.get('term', '')
        return render_template('portrait/search_result.html', stype=stype, term=term)
    else:
        term = request.args.get('term', '')
        return render_template('portrait/search_result.html', stype=stype, term=term)

@mod.route('/test/')
def test():

    return render_template('portrait/stack.html')
"""
@mod.route('/manage/')
def manage():
    return render_template('index/manage.html')
"""
