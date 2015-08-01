#-*- coding:utf-8 -*-

import os
import time
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from utils import submit_attribute, search_attribute

from user_portrait.time_utils import ts2datetime

mod = Blueprint('custom_attribute', __name__, url_prefix='/custom_attribute')

# use to add attribute and value filed to the es (cluster:es_user_portrait)
@mod.route('/submit_attribtue/')
def ajax_submit_attribute():
    status = False
    # input cannont be None
    attribute_name = request.args.get('custom_attribute', '') # my_attribute1
    attribute_value = request.args.get('attribute_value', '') # attribute_value =[ '1', '2' ,'3']
    submit_user = request.args.get('user_name', '')           # user_name = admin1
    state = request.args.get('state', '')                     # state = ''
    status = submit_attribute(attribute_name, attribute_value, submit_user, state) # mark success or fail
    return json.dumps(status)

# use to search attribute table
@mod.route('/search_attribute/')
def ajax_search_attribute():
    status = False
    query_field_wildcard = ['name', 'state', 'user']
    query_field_match = ['date']
    query_body = []
    condition_num += 1
    for term in query_field_wildcard:
        item = request.args.get(term, '')
        if term:
            query_body.append({'wildcard':{term: '*'+item+'*'}})
            condition_num += 1
      
    for term in query_field_match:
        item = request.args.get(term, '')
        if term:
            query_body.append({'match':{term: item}})
            condition_num += 1
    result = search_attribute(query_body, condition_num)
    return json.dumps(result)

# use to change attribute table
@mod.route('/change_attribtue/')
def ajax_change_attribtue():
    status = False
    return json.dumps(status)

# use to delete attribute table and user in portrait which have attribtue would be deleted meantime
@mod.route('/delete_attribute/')
def ajax_delete_attribute():
    status = False
    return json.dumps(status)

# use to add attribute and value to user in portrait
@mod.route('/add_attribute/')
def ajax_add_attirbute():
    status = False
    return json.dumps(status)




