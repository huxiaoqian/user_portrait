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

@mod.route('/social_sensing/')
def social_sensing():
    return render_template('portrait/social_sensing.html')

@mod.route('/sensing_analysis/')
def sensing_analysis():
    task_name = request.args.get('task_name','监督维权律师' )
    keywords = request.args.get('keywords','律师,维权' )
    ts = request.args.get('ts','1378567800' )
    return render_template('portrait/sensing_analysis.html', task_name=task_name, keywords=keywords, ts=ts)

@mod.route('/group/')
def group_identify():
    return render_template('portrait/group_identify.html')

@mod.route('/group_analysis/')
def group_analysis():
    name = request.args.get('name', 'test_task')

    return render_template('portrait/group_analysis.html', name=name)
'''
@mod.route('/group_result/')
def group_result():
    
        return render_template('portrait/group_result.html')
'''
@mod.route('/contrast/')
def contrast():
    
    return render_template('portrait/compare.html')

@mod.route('/personal/')
def personal():
    uid = request.args.get('uid', '1642591402')

    return render_template('portrait/personal.html', uid=uid)

@mod.route('/recommend_in/')
def recommend_in():

    return render_template('portrait/recommend_in.html')

@mod.route('/recommend_out/')
def recommend_out():

    return render_template('portrait/recommend_out.html')

@mod.route('/influence_rank/')
def influence_rank():

    return render_template('portrait/influence_rank.html')
@mod.route('/tag/')
def tag():

    return render_template('portrait/tag.html')
@mod.route('/contrast_analysis/')
def contrast_analysis():
    return render_template('portrait/contrast_analysis.html')

@mod.route('/search_result/')
def search_result():
    stype = request.args.get('stype', '1')
    if stype == '1':
        term = request.args.get('term', '')
        #print term
        return render_template('portrait/search_result.html', stype=stype, term=term)
    else:
        uid = request.args.get('uid', '')
        uname = request.args.get('uname', '')
        location = request.args.get('location', '')
        activity_geo = request.args.get('activity_geo', '')
        adkeyword = request.args.get('adkeyword', '')
        hashtag = request.args.get('hashtag', '')
        psycho_status_by_emotion = request.args.get('psycho_status_by_emotion', '')
        psycho_status_by_word = request.args.get('psycho_status_by_word','')
        psycho_feature = request.args.get('psycho_feature', '')
        domain = request.args.get('domain', '')
        topic = request.args.get('topic', '')
        tag = request.args.get('tag', '')

        return render_template('portrait/search_result.html', stype=stype, uid=uid, uname=uname,\
                location=location, activity_geo=activity_geo, adkeyword=adkeyword, hashtag=hashtag, psycho_status_by_emotion=psycho_status_by_emotion,psycho_status_by_word=psycho_status_by_word,\
                psycho_feature=psycho_feature, domain=domain, topic=topic, tag=tag)


@mod.route('/contact/')
def contact():
    uid = request.args.get('uid', '2001627641')
    return render_template('portrait/contact.html', uid=uid)


