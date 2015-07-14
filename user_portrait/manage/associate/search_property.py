# -*- coding: UTF-8 -*-

import sys
import time
import json
from connection import profile_match, portrait_match, portrait_exist
sys.path.append('../../../')
from user_portrait.search_user_profile import es_get_source
from user_portrait.search_user_portrait import search_portrait_by_id
from user_portrait.attribute.search import search_attention, search_follower,\
        search_mention, search_location, search_activity
from user_portrait.attribute.search_daily_info import search_origin_attribute,\
        search_retweeted_attribute, search_user_index

def search_profile(uid):
    user_profile_keys = ['input_time', 'uid', 'photo_url', 'statusnum', 'nick_name',\
            'rel_name', 'description', 'sp_type', 'user_location', 'create_at',\
            'sex', 'user_birth', 'blog_url', 'fansnum', 'isreal', 'favoritesnum',\
            'id', 'user_email', 'friendsnum']
    source = es_get_source(uid)
    print 'profile:', source

    results_list = []
    match_keys = ['user_location']

    for key in match_keys:
        token = source[key]
        results = profile_match(key, token)
        sum_dict = {}
        uid_set = set()
        if results:
            for item in results:
                uid_set.add(item["_id"])

                r = item["_source"][key]
                if r not in sum_dict:
                    sum_dict[r] = 0
                    print r
            print 'len:', len(uid_set)
        results_list.append(uid_set)
    return results_list

def search_portrait(uid):
    user_portrait_keys = ['uid', 'uname', 'domain', 'topic', 'psycho_status', \
            'psycho_feature', 'emoticon', 'online_pattern', 'link', 'hashtag',\
            'text_len', 'emotion_words', 'activity_location']
    source = search_portrait_by_id(uid)
    print 'portrait:', source
    # match_keys = ['activity_location']
    token = source['activity_location']
    results = portrait_match('activity_location', token)
    sum_dict = {}
    uid_set = set()
    if results:
        for item in results:
            uid_set.add(item["_id"])

            r = item["_source"]["activity_location"]
            if r not in sum_dict:
                sum_dict[r] = 0
                print r
        print 'len:', len(uid_set)

    topic_set = set()
    results = portrait_exist("教育")
    if results:
        for item in results:
            topic_set.add(item["_id"])

        print 'len:', len(topic_set)

    domain_set = set()
    results = portrait_match('domain', '教育 科技')
    if results:
        for item in results:
            domain_set.add(item["_id"])

        print 'len:', len(domain_set)
    return uid_set, topic_set, domain_set

def search_friends(uid):
    results = search_attention(uid)
    attention_set = set()
    if results:
        print 'attention:', len(results.keys())
        for uid in results:
            attention_set.add(uid)
        print 'attention_len:', len(attention_set)

    results = search_follower(uid)
    follower_set = set()
    if results:
        print 'follow:', len(results.keys())
        for uid in results:
            follower_set.add(uid)
        print 'follower_len:', len(follower_set)
    return attention_set, follower_set

def search_ultra(now_ts, uid):
    results = search_mention(now_ts, uid)
    print 'at_user', results
    mention_set = set()
    if results:
        print 'at_user:', len(results.keys())
        for uid in results:
            mention_set.add(uid)
        print 'mention_len:', len(mention_set)

    """
    results4 = search_location(now_ts, uid)
    print 'location:', results4
    """
    results5 = search_activity(now_ts, uid)
    print 'activity:', results5
    return mention_set

def search_daily_info(user_index, uid, doc_type="bci"):
    result = search_origin_attribute(user_index, uid, doc_type)
    print "origin_attribute:", result
    result = search_retweeted_attribute(user_index, uid, doc_type)
    print "retweeted_attribute:", result
    result = search_user_index(user_index, uid, doc_type)
    print "user_index:", result

def total_select(sets):
    results_dict = {}
    for single_set in sets:
        if not single_set:
            continue
        for item in single_set:
            try:
                results_dict[item] += 1
            except KeyError:
                results_dict[item] = 0
    f = open('test.txt', 'w')
    sum_dict = {}
    for key in results_dict:
        value = str(results_dict[key])
        f.write(key+'\t'+value+'\n')
        try:
            sum_dict[value] += 1
        except KeyError:
            sum_dict[value] = 0
    f.close()
    print sum_dict


if __name__=='__main__':
    uid = '1000004720'
    uid = '1000036312'
    sets = []
    attention_set, follower_set = search_friends(uid)
    sets.append(attention_set)
    sets.append(follower_set)

    now_ts = 1377964800 + 3600 * 24 * 4
    mention_set = search_ultra(now_ts, uid)
    sets.append(mention_set)

    search_daily_info("20130901", uid)
    profile_list = search_profile(uid)
    sets.extend(profile_list)

    uid = "11111"
    portrait_set, topic_set, domain_set = search_portrait(uid)
    sets.append(portrait_set)
    sets.append(topic_set)
    sets.append(domain_set)

    total_select(sets)
