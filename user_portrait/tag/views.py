#-*- coding:utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from utils import submit_attribute, search_attribute, change_attribute, delete_attribute ,\
                  add_attribute_portrait, change_attribute_portrait, delete_attribute_portrait, \
                  get_user_tag, get_group_tag, add_tag2group, get_attribute_name, get_attribute_value, \
                  get_user_attribute_name

from user_portrait.time_utils import ts2datetime

mod = Blueprint('tag', __name__, url_prefix='/tag')

# use to add attribute and value filed to the es (cluster:es_user_portrait)
@mod.route('/submit_attribute/')
def ajax_submit_attribute():
    status = False
    # input cannont be None
    attribute_name = request.args.get('attribute_name', '') # my_attribute1
    attribute_value = request.args.get('attribute_value', '') # attribute_value ='tag1,tag2'
    submit_user = request.args.get('user', '')           # user_name = admin1
    submit_date = request.args.get('date', '')         # submit_date = 2013-09-08
    status = submit_attribute(attribute_name, attribute_value, submit_user, submit_date) # mark success or fail
    return json.dumps(status)

# use to search attribute table
@mod.route('/search_attribute/')
def ajax_search_attribute():
    status = False
    query_field_wildcard = ['attribute_name', 'attribute_value']
    query_field_match = ['date', 'user']
    query_body = []
    condition_num = 0
    for term in query_field_wildcard:
        item = request.args.get(term, '')
        if item:
            query_body.append({'wildcard':{term: '*'+item+'*'}})
            condition_num += 1
      
    for term in query_field_match:
        item = request.args.get(term, '')
        if item:
            query_body.append({'match':{term: item}})
            condition_num += 1
    result = search_attribute(query_body, condition_num)
    return json.dumps(result)

# use to change attribute table
@mod.route('/change_attribute/')
def ajax_change_attribtue():
    status = False
    #need to identify the user have the power to change the attribute table
    attribute_name = request.args.get('attribute_name', '')
    attribute_value = request.args.get('attribute_value', '')   # attribute_value = 'tag1&tag2'
    submit_user = request.args.get('user', '')
    submit_date = request.args.get('date', '')
    status = change_attribute(attribute_name, attribute_value, submit_user, submit_date)
    return json.dumps(status)

# use to delete attribute table and user in portrait which have attribtue would be deleted meantime
@mod.route('/delete_attribute/')
def ajax_delete_attribute():
    status = False
    attribute_name = request.args.get('attribute_name', '')
    status = delete_attribute(attribute_name)
    return json.dumps(status)

# use to add attribute and value to user in portrait
@mod.route('/add_attribute/')
def ajax_add_attirbute():
    status = False
    uid = request.args.get('uid', '')
    attribute_name = request.args.get('attribute_name', '')
    attribute_value = request.args.get('attribute_value', '')
    submit_user = request.args.get('user', '')
    
    status = add_attribute_portrait(uid, attribute_name, attribute_value, submit_user)
    return json.dumps(status)

# use to change attribute in user_portrait
@mod.route('/change_attribute_portrait/')
def ajax_change_attribute_portrait():
    status = False
    uid = request.args.get('uid', '')
    attribute_name = request.args.get('attribute_name', '')
    attribute_value = request.args.get('attribute_value', '')
    submit_user = request.args.get('user', '')
    status = change_attribute_portrait(uid, attribute_name, attribute_value, submit_user)
    return json.dumps(status)

# use to delete attribute in user_portrait
@mod.route('/delete_user_tag/')
def ajax_delete_attribute_portrait():
    status = False
    uid = request.args.get('uid', '')
    attribute_name = request.args.get('attribute_name', '')
    submit_user = request.args.get('user', '')
    status = delete_attribute_portrait(uid, attribute_name, submit_user)
    return json.dumps(status)

# use to show user tags(one/group)
@mod.route('/show_user_tag/')
def ajax_show_user_tag():
    result = {}
    uid_list_string = request.args.get('uid_list', '') # uid_list = 'uid1,uid2'
    uid_list = uid_list_string.split(',')
    result = get_user_tag(uid_list)
    return json.dumps(result)


# use to show user attribute_name for imagin deal
@mod.route('/show_user_attribute_name/')
def ajax_show_user_attribute_name():
    result = []
    uid = request.args.get('uid', '')
    result = get_user_attribute_name(uid)
    return json.dumps(result)


# use to show group tag statistic result
@mod.route('/show_group_tag/')
def ajax_show_group_tag():
    result = {}
    group_task_name = request.args.get('task_name', '')
    result = get_group_tag(group_task_name)
    return json.dumps(result)

# use to add tag to group
@mod.route('/add_group_tag/')
def ajax_aff_group_tag():
    status = False
    uid_list_string = request.args.get('uid_list', '')
    uid_list = uid_list_string.split(',')
    attribute_name = request.args.get('attribute_name', '')
    attribute_value = request.args.get('attribute_value', '')
    status = add_tag2group(uid_list, attribute_name, attribute_value)
    return json.dumps(status)


# use to show custom_attribtue_name in search conditon as drop_down_box
@mod.route('/show_attribute_name/')
def ajax_show_attribtue_name():
    result = []
    attribute_name_list = get_attribute_name()
    return json.dumps(attribute_name_list)

# use to show custom_attribtue_value in search condition as drop_down_box
@mod.route('/show_attribute_value/')
def ajax_show_attribute_value():
    result = []
    attribute_name = request.args.get('attribute_name', '')
    attribute_value_list = get_attribute_value(attribute_name)
    return json.dumps(attribute_value_list)
