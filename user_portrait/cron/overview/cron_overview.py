# -*- coding: UTF-8 -*-
import sys
import json
import time
from elasticsearch.helpers import scan
reload(sys)
sys.path.append('../../')
from global_utils import R_RECOMMENTATION as r
from global_utils import es_user_portrait as es
from time_utils import ts2datetime, datetime2ts

basic_field = ['user_count', 'gender_ratio', 'location_top', 'verified_ratio']
behavior_field = ['total_status', 'keywords_top', 'activity_geo', 'hashtag_top',\
                  'topic_top', 'online_pattern_top']
user_field = ['domain_top', 'domain_top_user']
compute_field = ['recomment_in_count', 'recomment_out', 'compute_count']

index_name = 'user_portrait'
index_type = 'user'

def get_user_count():
    count = 0
    query_body = {
            'query':{
                'match_all':{}
                }
            }
    count = es.count(index=index_name, doc_type=index_type, body=query_body)['count']
    print 'all user count:', count
    return count

# ?? data source
def get_total_status():
    total_count = 0
    return total_count

def get_scan_results():
    gender_result = {'1':0, '2':0}
    verified_result = {'yes':0, 'no':0}
    location_result = {}
    activity_geo_result = {}
    keywords_result = {}
    hashtag_result = {}
    topic_result = {}
    no_gender_count = 0
    no_verified_count = 0
    no_location_count = 0
    no_activity_geo_count = 0
    no_keywords_count = 0
    no_hashtage_count = 0
    no_topic_count = 0
    s_re = scan(es, query={'query':{'match_all':{}}, 'size':100}, index=index_name, doc_type=index_type)
    while True:
        while True:
            try:
                scan_re = s_re.next()['_source']
                # gender ratio count
                try:
                    gender_result[str(scan_re['gender'])] += 1
                except:
                    no_gender_count += 1
                # verified ratio count
                try:
                    verified_result[str(scan_re['verified'])] += 1
                except:
                    no_verified_count += 1
                # loation top
                try:
                    location = scan_re['location']
                    if len(location.split(' '))>1:
                        location = location.split(' ')[0]
                    try:
                        location_result[location] += 1
                    except:
                        location_result[location] = 1
                except:
                    no_location_count += 1
                # activity geo
                try:
                    activity_geo = scan_re['activity_geo']
                    if scan_re:
                        activity_geo_list = activity_geo.split('&')
                        for geo in activity_geo_list:
                            try:
                                activity_geo_result[geo] += 1
                            except:
                                activity_geo_result[geo] = 1
                except:
                    no_activity_geo_count += 1
                # keywords
                try:
                    keywords = json.loads(scan_re['keywords'])
                    if keywords:
                        for word in keywords:
                            try:
                                keywords_result[word] += keywords[word]
                            except:
                                keywords_result[word] = keywords[word]
                except:
                    no_keywords_count += 1
                # hashtag top
                try:
                    hashtag = scan_re['hashtag']
                    if hashtag:
                        hashtag_list = hashtag.split(' ')
                        for tag in hashtag_list:
                            try:
                                hashtag_result[tag] += 1
                            except:
                                hashtag_result[tag] = 1
                except:
                    no_hashtag_count += 1
                # topic top
                try:
                    topic = scan_re['topic']
                    if topic:
                        topic_list = topic.split(' ')
                        for item in topic_list:
                            try:
                                topic_result[item] += 1
                            except:
                                topic_result[item] = 1
                except:
                    no_topic_count += 1
            except StopIteration:
                print 'all done'
                # gender ratio count
                count = sum(gender_result.values())
                gender_ratio = {'1':float(gender_result['1']) / count, '2':float(gender_result['2']) / count}
                print 'gender ratio:', gender_ratio
                # verified ratio count
                count = sum(verified_result.values())
                verified_ratio = {'yes':float(verified_result['yes']) / count, 'no':float(verified_result['no'])/count}
                print 'verified ratio:', verified_ratio
                # location top
                if location_result:
                    sort_location = sorted(location_result.items(), key=lambda x:x[1], reverse=True)
                    location_top = sort_location[:5]
                else:
                    location_top = {}
                print 'location top:', location_top
                # activity geo top
                if activity_geo_result:
                    sort_activity_geo = sorted(activity_geo_result.items(), key=lambda x:x[1], reverse=True)
                    activity_geo_top = sort_activity_geo[:5]
                else:
                    activity_geo_top = {}
                print 'activity_geo_top:', activity_geo_top
                # keywords top
                if keywords_result:
                    sort_keywords = sorted(keywords_result.items(), key=lambda x:x[1], reverse=True)
                    keywords_top = sort_keywords[:50]
                else:
                    keywords_top = {}
                print 'keywords_top:', keywords_top
                # hashtag top
                if hashtag_result:
                    sort_hashtag = sorted(hashtag_result.items(), key=lambda x:x[1], reverse=True)
                    hashtag_top = sort_hashtag[:50]
                else:
                    hashtag_top = {}
                print 'hashtag top:', hashtag_top
                # topic top
                if topic_result:
                    sort_topic = sorted(topic_result.items(), key=lambda x:x[1], reverse=True)
                    topic_top = sort_topic[:5]
                else:
                    topic_top = {}
                print 'topic top:', topic_top
                sys.exit(0)
            except Exception, r:
                print Exception, r
                sys.exit(0)
    return gender_ratio

def compute_overview():
    results = {}
    results['user_count'] = get_user_count()
    results['total_status'] = get_total_status()
    scan_result = get_scan_results()
    results = dict(results, **scan_result)
    print 'results:', results
    return results


if __name__=='__main__':
    compute_overview()
