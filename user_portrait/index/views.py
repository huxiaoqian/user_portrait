#-*- coding:utf-8 -*-

import json
import time
import datetime
from user_portrait.time_utils import ts2datetime, ts2date
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect, make_response


mod = Blueprint('portrait', __name__, url_prefix='/index')


@mod.route('/')
def loading():

    return render_template('portrait/overview.html')

@mod.route('/group_analysis/')
def group_analysis():

    return render_template('portrait/group_analysis.html')
@mod.route('/group_result/')
def group_result():
    
        return render_template('portrait/group_result.html')
@mod.route('/contrast/')
def contrast():
    
    return render_template('compare.html')

@mod.route('/personal/')
def personal():

    return render_template('portrait/personal.html')

@mod.route('/recommend_in/')
def recommend_in():

    return render_template('portrait/recommend_in.html')

@mod.route('/recommend_out/')
def recommend_out():

    return render_template('portrait/recommend_out.html')

@mod.route('/influence_rank/')
def influence_rank():

    return render_template('portrait/influence_rank.html')

@mod.route('/search_result/')
def search_result():
    stype = request.args.get('stype', 1)
    if stype == 1:
        term = request.args.get('term', '')
        return render_template('portrait/search_result.html', stype=stype, term=term)
    else:
        uid = request.args.get('uid', '')
        uname = request.args.get('uname', '')
        location = request.args.get('location', '')
        adkeyword = request.args.get('adkeyword', '')
        hashtag = request.args.get('hashtag', '')
        psycho_status = request.args.get('psycho_status', '')
        psycho_feature = request.args.get('psycho_feature', '')
        domain = request.args.get('domain', '')
        topic = request.args.get('topic', '')

        return render_template('portrait/search_result.html', stype=stype, uid=uid, uname=uname,\
                location=location, adkeyword=adkeyword, hashtag=hashtag, psycho_status=psycho_status,\
                psycho_feature=psycho_feature, domain=domain, topic=topic)

@mod.route('/test/')
def test():

    return render_template('portrait/stack.html')
"""
@mod.route('/manage/')
def manage():
    return render_template('index/manage.html')
"""


@mod.route('/contact/')
def contact():
    
    return render_template('contact.html')


