#-*- coding:utf-8 -*-

import os
import time
import sys
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from search_user_index_function import search_top_index, search_influence_detail, user_index_range_distribution,\
                                       search_max_single_field, search_portrait_history_active_info
from rank_portrait_in_active_user import search_portrait_user_in_activity
from search_vary_index_function import query_vary_top_k

from user_portrait.global_utils import ES_CLUSTER_FLOW1 as es

portrait_index = "user_portrait" # user_portrait_database
portrait_type = "user"

mod = Blueprint('influence_application', __name__, url_prefix='/influence_application')

@mod.route('/all_active_rank/')
def ajax_all_active_rank():
    date = request.args.get('date', '') # '2013-09-01'
    number = request.args.get('number', 100) # "100"
    date = str(date)
    number = int(number)
    #former_date = time.strftime('%Y%m%d',time.localtime(time.time()-86400))
    former_date = "20130901" # test
    if not date:
        index_name = former_date
    else:
        index_name = date.replace('-','')

    if index_name != former_date: # search date is not the record activity date
        results = 0
    else:
        results = search_top_index(index_name, number)

    return json.dumps(results)


@mod.route('/portrait_user_in_active/')
def ajax_portrait_user_in_active():
    date = request.args.get('date', '') # '2013-09-01'
    number = request.args.get('number', 100) # "100"
    date = str(date)
    number = int(number)
    #former_date = time.strftime('%Y%m%d',time.localtime(time.time()-86400))
    former_date = "20130901" # test
    if not date:
        index_name = former_date
    else:
        index_name = date.replace('-','')

    if index_name != former_date:
        results = 0
    else:
        results = search_portrait_user_in_activity(es, number, index_name, "bci", portrait_index, portrait_type)

    return json.dumps(results)


@mod.route('/specified_user_active/')
def ajax_specified_user_active():
    date = request.args.get('date', '') # '2013-09-01'
    uid_list = request.args.get('uid_list', '') # 123456,123456
    #former_date = time.strftime('%Y%m%d',time.localtime(time.time()-86400))
    former_date = "20130901" # test
    date = str(date)

    if not date:
        index_name = former_date
    else:
        index_name = date.replace('-','')

    list_1 = []
    uid_list = [item for item in uid_list.split(',')]

    if index_name != former_date or uid_list == ['']:
        results = 0
    else:
        results = search_influence_detail(uid_list, index_name, "bci") 

    return json.dumps(results)



@mod.route('/user_index_distribution/')
def ajax_user_index_distribution():
    date = request.args.get('date', '') # '2013-09-01'
    former_date = "20130901" # test
    date = str(date)

    if not date:
        results = 0
    else:
        index_name = date.replace('-','')
        results = user_index_range_distribution(index_name)

    return json.dumps(results)


@mod.route('/hot_origin_weibo/')
def ajax_hot_origin_weibo():
    date = request.args.get('date', '') # '2013-09-01'
    number = request.args.get('number', 3) # default
    #former_date = time.strftime('%Y%m%d',time.localtime(time.time()-86400))
    former_date = "20130901" # test
    date = str(date)

    if not date:
        index_name = former_date
    else:
        index_name = date.replace('-','')
    if index_name != former_date:
        results = 0
    else:
        results = {}
        dict_1 = search_max_single_field("origin_weibo_retweeted_top_number", index_name, "bci", number)
        dict_2 = search_max_single_field("origin_weibo_comment_top_number", index_name, "bci", number)
        results['origin_weibo_retweeted'] = dict_1
        results['origin_weibo_comment'] = dict_2

    return json.dumps(results)

@mod.route('/hot_origin_weibo_brust/')
def ajax_hot_origin_weibo_brust():
    date = request.args.get('date', '') # '2013-09-01'
    number = request.args.get('number', 3) # default
    #former_date = time.strftime('%Y%m%d',time.localtime(time.time()-86400))
    former_date = "20130901" # test
    date = str(date)

    if not date:
        index_name = former_date
    else:
        index_name = date.replace('-','')

    if index_name != former_date:
        results = 0
    else:
        results = {}
        dict_1 = search_portrait_user_in_activity(es, number, index_name, "bci", portrait_index, portrait_type, field="origin_weibo_retweeted_brust_average")
        dict_2 = search_portrait_user_in_activity(es, number, index_name, "bci", portrait_index, portrait_type, field="origin_weibo_comment_brust_average")
        results['origin_weibo_retweeted_brust'] = dict_1
        results['origin_weibo_comment_brust'] = dict_2

    return json.dumps(results)


@mod.route('/portrait_history_active')
def ajax_portrait_history_active():
    start_date = request.args.get('start_date', '')# 2013-09-01
    start_date = str(start_date).replace('-',"")

    end_date = request.args.get('end_date', '')
    end_date = str(end_date).replace('-','')

    uid = request.args.get('uid', '')

    if not uid or not start_date or not end_date:
        results = 0
    else:
        results = search_portrait_history_active_info(uid, start_date, end_date)

    return json.dumps(results)

@mod.route('/vary_top_k/')
def ajax_vary_top_k():
    date = request.args.get('date', '')
    number = request.args.get('number', 100) # "100"
    date = str(date)
    number = int(number)
    #former_date = time.strftime('%Y%m%d',time.localtime(time.time()-86400))
    former_date = "20130901" # test
    if not date:
        index_name = former_date
    else:
        index_name = date.replace('-','')

    if index_name != former_date:
        results = 0
    else:
        results = query_vary_top_k("vary", "bci", number)

    return json.dumps(results)



@mod.route('/portrait_user_in_vary/')
def ajax_portrait_user_in_vary():
    number = request.args.get('number', 100) # "100"
    results = search_portrait_user_in_activity(es, number, "vary", "bci", portrait_index, portrait_type, "vary")

    return json.dumps(results)

