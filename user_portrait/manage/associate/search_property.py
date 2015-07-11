# -*- coding: UTF-8 -*-

import sys
import time
import json
sys.path.append('../../../')
from user_portrait.search_user_profile import es_get_source
from user_portrait.search_user_portrait import search_portrait_by_id
from user_portrait.attribute.search import search_attention, search_follower,\
        search_mention, search_location, search_activity
from user_portrait.attribute.search_daily_info import search_origin_attribute,\
        search_retweeted_attribute, search_fans_attribute

def search_profile(uid):
    user_profile_keys = ['input_time', 'uid', 'photo_url', 'statusnum', 'nick_name',\
            'rel_name', 'description', 'sp_type', 'user_location', 'create_at',\
            'sex', 'user_birth', 'blog_url', 'fansnum', 'isreal', 'favoritesnum',\
            'id', 'user_email', 'friendsnum']
    source = es_get_source(uid)
    print 'profile:', source

def search_portrait(uid):
    source = search_portrait_by_id(uid)
    print 'portrait:', source

def search_friends(uid):
    results1 = search_attention(uid)
    print 'attention:', results1
    results2 = search_follower(uid)
    print 'follow:', results2

def search_ultra(now_ts, uid):
    results3 = search_mention(now_ts, uid)
    print 'at_user:', results3
    results4 = search_location(now_ts, uid)
    print 'location:', results4
    results5 = search_activity(now_ts, uid)
    print 'activity:', results5

def search_daily_info(user_index, uid, doc_type="bci"):
    result = search_origin_attribute(user_index, uid, doc_type)
    print "origin_attribute:", result
    result = search_retweeted_attribute(user_index, uid, doc_type)
    print "retweeted_attribute:", result
    result = search_fans_attribute(user_index, uid, doc_type)
    print "fans_attribute:", result

if __name__=='__main__':
    uid = '1798289842'
    search_friends(uid)

    now_ts = 1377964800 + 3600 * 24 * 4
    search_ultra(now_ts, uid)

    search_daily_info("20130901", "1713926427")

    uid = '1829417897'
    search_profile(uid)

    uid = '1111111111'
    search_portrait(uid)
