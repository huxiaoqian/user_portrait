#-*- coding:utf-8 -*-

import os
import time
import json

from user_portrait.global_utils import es_user_portrait, portrait_index_name, portrait_index_type
from user_portrait.global_utils import es_flow_text, flow_text_index_name_pre, flow_text_index_type
from user_portrait.global_utils import retweet_index_name_pre, retweet_index_type,\
                                       be_retweet_index_name_pre, be_retweet_index_type,\
                                       comment_index_name_pre, comment_index_type,\
                                       be_comment_index_name_pre, be_comment_index_type

#use to save detect task
#input: {}
#output: {}
def save_detect_task():
    results = {}
    save_detect2es()
    save_detect2redis()
    return results


#use to save parameter and task information to group redis queue
#input: {}
#output: {}
def save_detect2redis():
    results = {}
    return results

#use to save parameter and task information to group es
#input: {}
#output: {}
def save_detect2es():
    results = {}
    return results

#use to show detect task information
#input: {}
#output: {}
def show_detect_task():
    results = {}
    return results

#use to add detect task having been done to group analysis
#input:{}
#output: {}
def detect2analysis():
    results = {}
    return results
