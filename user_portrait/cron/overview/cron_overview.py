# -*- coding: UTF-8 -*-
import sys
import json
import time
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
    count = es.count(index=index_time, doc_type=index_type, body=query_body)['count']
    return count

def get_gender_ratio():
    result = {'male':0, 'female':0}
    count = 0
    s_re = scan(es, query={'query':{'match_all':{}}, 'size':1000}, index=index_name, doc_type=index_type)
    while True:
        while True:
            try:
                scan_re = s_re.next()['_source']
                count += 1
                try:
                    result[scan_re['gender']] += 1
                except:
                    pass
            except StopIteration:
                print 'all done'
                sys.exit(0)
            except Exception, r:
                print Exception, r
                sys.exit(0)
    print 'gender_dict:', gender_dict
    count = sum(gender_dict.values())
    gender_ratio ={'male': float(gender_dict['male']) / count, 'female': float(gender_dict['female']) / count}

    return gender_ratio
    

def compute_overview():
    results = {}
    status = False
    results['user_count'] = get_user_count()
    results['gender_ratio'] = get_gender_ratio()
    print 'status:', status
    return status


if __name__=='__main__':
    compute_overview()
