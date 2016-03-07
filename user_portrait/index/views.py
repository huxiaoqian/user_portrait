#-*- coding:utf-8 -*-

import json
import time
import datetime
from user_portrait.time_utils import ts2datetime, ts2date
from flask import redirect, url_for, session, Blueprint, url_for, render_template, request, abort, flash, session, redirect, make_response
from flask.ext.login import login_required

mod = Blueprint('portrait', __name__, url_prefix='/index')

@mod.route('/')
#@login_required
def loading():
    if 'logged_in' in session and session['logged_in']:
        return render_template('portrait/overview.html')
    else:
        return redirect('/login/')


@mod.route('/social_sensing/')
#@login_required
def social_sensing():
    if 'logged_in' in session and session['logged_in']:
        return render_template('portrait/social_sensing.html')
    else:
        return redirect('/login/')

@mod.route('/sensing_analysis/')
#@login_required
def sensing_analysis():
    if 'logged_in' in session and session['logged_in']:
        task_name = request.args.get('task_name','监督维权律师' )
        keywords = request.args.get('keywords','律师,维权' )
        ts = request.args.get('ts','1378567800' )
        return render_template('portrait/sensing_analysis.html', task_name=task_name, keywords=keywords, ts=ts)
    else:
        return redirect('/login/')

@mod.route('/group/')
#@login_required
def group_identify():
    if 'logged_in' in session and session['logged_in']:
        return render_template('portrait/group_identify.html')
    else:
        return redirect('/login/')

@mod.route('/group_analysis/')
#@login_required
def group_analysis():
    if 'logged_in' in session and session['logged_in']:
        name = request.args.get('name', 'test_task')
        return render_template('portrait/group_analysis.html', name=name)
    else:
        return redirect('/login/')

@mod.route('/contrast/')
#@login_required
def contrast():
    if 'logged_in' in session and session['logged_in']:
        return render_template('portrait/compare.html')
    else:
        return redirect('/login/')

@mod.route('/personal/')
#@login_required
def personal():
    if 'logged_in' in session and session['logged_in']:
        uid = request.args.get('uid', '1642591402')

        return render_template('portrait/personal.html', uid=uid)
    else:
        return redirect('/login/')

@mod.route('/recommend_in/')
#@login_required
def recommend_in():
    if 'logged_in' in session and session['logged_in']:
        return render_template('portrait/recommend_in.html')
    else:
        return redirect('/login/')


@mod.route('/recommend_out/')
#@login_required
def recommend_out():
    if 'logged_in' in session and session['logged_in']:
        return render_template('portrait/recommend_out.html')
    else:
        return redirect('/login/')


@mod.route('/influence_rank/')
#@login_required
def influence_rank():
    if 'logged_in' in session and session['logged_in']:
        return render_template('portrait/influence_rank.html')
    else:
        return redirect('/login/')

@mod.route('/tag/')
#@login_required
def tag():
    if 'logged_in' in session and session['logged_in']:
        return render_template('portrait/tag.html')
    else:
        return redirect('/login/')

@mod.route('/contrast_analysis/')
#@login_required
def contrast_analysis():
    if 'logged_in' in session and session['logged_in']:
        return render_template('portrait/contrast_analysis.html')
    else:
        return redirect('/login/')

@mod.route('/search_result/')
#@login_required
def search_result():
    if 'logged_in' in session and session['logged_in']:
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
    else:
        return redirect('/login/')


@mod.route('/contact/')
#@login_required
def contact():
    if 'logged_in' in session and session['logged_in']:
        uid = request.args.get('uid', '2001627641')
        return render_template('portrait/contact.html', uid=uid)
    else:
        return redirect('/login/')


