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

#user to detect group by single-person
#input: {}
#output: {}
def single_detect():
    results = {}
    #step1: identify the uid or uname is right
    #step2: get user by three type parameter
    return results

