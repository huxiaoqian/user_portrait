#-*- coding:utf-8 -*-

import json
import time
import datetime
from case.time_utils import ts2datetime, ts2date
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect, make_response

scws = load_scws()

mod = Blueprint('portrait', __name__, url_prefix='/index')


em = EventManager()

'''
def acquire_user_by_id(uid):
    user_search = XapianSearch(path=XAPIAN_USER_DATA_PATH, name='master_timeline_user', schema_version=1)
    result = user_search.search_by_id(int(uid), fields=['name', 'location', 'followers_count', 'friends_count', 'profile_image_url'])
    user = {}

    if result:
        user['name'] = result['name']
        user['location'] = result['location']
        user['followers_count'] = result['followers_count']
        user['friends_count'] = result['friends_count']
        user['profile_image_url'] = result['profile_image_url']
    else:
        return None

    return user

def get_default_timerange():
    return u'20150123-20150202'

def get_default_topic():
    return u'张灵甫遗骨疑似被埋羊圈'

def get_default_pointInterval():
    return {'zh': u'1天', 'en': 3600 * 24}

def get_pointIntervals():
    return [{'zh': u'15分钟', 'en': 900}, {'zh': u'1小时', 'en': 3600}, {'zh': u'1天', 'en': 3600 * 24}]

def get_gaishu_yaosus():
    return {'yaosu': [('gaishu', u'概述分析')]}
    # return {'yaosu': (('gaishu', u'概述分析'), ('zhibiao', u'指标分析'))}

def get_deep_yaosus():
    return {'yaosu': (('time', u'时间分析'), ('area', u'地域分析'), \
                      ('moodlens', u'情绪分析'), ('network', u'网络分析'))}

default_timerange = get_default_timerange()
default_topic = get_default_topic()
default_pointInterval = get_default_pointInterval()
pointIntervals = get_pointIntervals()
gaishu_yaosus = get_gaishu_yaosus()
deep_yaosus = get_deep_yaosus()
'''
@mod.route('/')
def loading():
    """舆情案例首页（前台）,用户可以查看相应的案例，进入相应案例的分析页面
    """
    topics_list = topics_name_start_end()
    return render_template('index/gl.html', topics_list=topics_list)


@mod.route('/manage/')
def manage():
    """案例定制页面（后台），用户可以新增案例，启动后台计算
    """
    return render_template('index/manage.html')
