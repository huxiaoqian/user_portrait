# -*- coding: UTF-8 -*-
import sys
import json
import time
from elasticsearch.helpers import scan
reload(sys)
sys.path.append('../../')
from global_utils import R_RECOMMENTATION as r
from global_utils import es_user_portrait as es
from global_utils import ES_DAILY_RANK as es_cluster
from global_utils import es_user_profile
from global_utils import R_RECOMMENTATION as r_recomment
from time_utils import ts2datetime, datetime2ts

basic_field = ['user_count', 'gender_ratio', 'location_top', 'verified_ratio']
behavior_field = ['total_status', 'keywords_top', 'activity_geo', 'hashtag_top',\
                  'topic_top', 'online_pattern_top']
user_field = ['domain_top', 'domain_top_user']
compute_field = ['recomment_in_count', 'recomment_out', 'compute_count']

index_name = 'user_portrait'
index_type = 'user'

#there have to add domain user top rank
def get_domain_top_user(domain_top):
    result = {}
    domain_user = {}
    index_name = 'weibo_user'
    index_type = 'user'
    #test user list
    test_user_list = [['2803301701', '1639498782', '2656274875', '1402977920', '3114175427'], \
                      ['3575186384', '1316683401', '1894603174', '1641542052', '1068248497'], \
                      ['1729736051', '1396715380', '2377610962', '1828183230', '2718018210'], \
                      ['1250748474', '3270699555', '1417037145', '1193111400', '1403915120'], \
                      ['1671342103', '1255849511', '1647497355', '1989660417', '1189729754'], \
                      ['1182391231', '1670071920', '1689618340', '1494850741', '1708942053']]
    count = 0
    for item in domain_top:
        domain = item[0]
        #test
        user_list = test_user_list[count]
        result[domain] = []
        profile_result = es_user_profile.mget(index=index_name, doc_type=index_type, body={'ids':user_list})['docs']
        for profile in profile_result:
            uid = profile['_id']
            try:
                uname = profile['_source']['nick_name']
                photo_url = profile['_source']['photo_url']
            except:
                uname = 'unknown'
                photo_url = 'unknown'
            result[domain].append([uid, uname, photo_url])
        count += 1
    return result


def get_user_count():
    count = 0
    query_body = {
            'query':{
                'match_all':{}
                }
            }
    count = es.count(index=index_name, doc_type=index_type, body=query_body)['count']
    #print 'all user count:', count
    return count

'''
# total status
def get_total_status():
    total_count = 0
    return total_count
'''

def get_scan_results():
    result_dict = {}
    gender_result = {'1':0, '2':0}
    verified_result = {'yes':0, 'no':0}
    location_result = {}
    activity_geo_result = {}
    keywords_result = {}
    hashtag_result = {}
    topic_result = {}
    online_pattern_result = {}
    domain_result = {}
    no_gender_count = 0
    no_verified_count = 0
    no_location_count = 0
    no_activity_geo_count = 0
    no_keywords_count = 0
    no_hashtag_count = 0
    no_topic_count = 0
    no_online_pattern_count = 0
    no_domain_count = 0
    s_re = scan(es, query={'query':{'match_all':{}}, 'size':100}, index=index_name, doc_type=index_type)
    print 's_re:', s_re
    activity_count = 0
    while True:
        while True:
            portrait_uid_list = []
            try:
                scan_re = s_re.next()['_source']
                # gender ratio count
                portrait_uid_list.append(scan_re['uid'])
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
                    activity_geo = scan_re['activity_geo_dict']
                    if scan_re:
                        activity_geo_dict = json.loads(activity_geo)
                        for geo in activity_geo_dict:
                            geo_list = geo.split('\t')
                            if geo_list[0]==u'中国' and len(geo_list)>=2:
                                province = geo_list[1]
                                try:
                                    activity_geo_result[province] += activity_geo_dict[geo]
                                except:
                                    activity_geo_result[province] = activity_geo_dict[geo]
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
                    hashtag_dict = json.loads(scan_re['hashtag_dict'])
                    if hashtag_dict:
                        for tag in hashtag_dict:
                            try:
                                hashtag_result[tag] += hashtag_dict[tag]
                            except:
                                hashtag_result[tag] = hashtag_dict[tag]
                except:
                    no_hashtag_count += 1
                # topic top
                try:
                    topic = json.loads(scan_re['topic'])
                    if topic:
                        for item in topic:
                            try:
                                topic_result[item] += 1
                            except:
                                topic_result[item] = 1
                except:
                    no_topic_count += 1
                # online pattern top
                try:
                    online_pattern = json.loads(scan_re['online_pattern'])
                    if online_pattern:
                        for item in online_pattern:
                            try:
                                online_pattern_result[item] += online_pattern[item]
                            except:
                                online_pattern_result[item] = online_pattern[item]
                except:
                    no_online_pattern_count += 1
                # domain top
                try:
                    domain = scan_re['domain']
                    if domain:
                        domain_list = domain.split('_')
                        for item in domain_list:
                            try:
                                domain_result[item] += 1
                            except:
                                domain_result[item] = 1
                except:
                    no_domain_count += 1
                 
            except StopIteration:
                print 'all done'
                # gender ratio count
                count = sum(gender_result.values())
                gender_ratio = {'1':float(gender_result['1']) / count, '2':float(gender_result['2']) / count}
                #print 'gender ratio:', gender_ratio
                result_dict['activity_count'] = activity_count / count
                result_dict['gender_ratio'] = json.dumps(gender_ratio)
                # verified ratio count
                count = sum(verified_result.values())
                if count==0:
                    verified_ratio = {'yes':0.5, 'no':0.5}
                else:
                    verified_ratio = {'yes':float(verified_result['yes']) / count, 'no':float(verified_result['no'])/count}
                #print 'verified ratio:', verified_ratio
                result_dict['verified_ratio'] = json.dumps(verified_ratio)
                # location top
                if location_result:
                    sort_location = sorted(location_result.items(), key=lambda x:x[1], reverse=True)
                    location_top = sort_location[:5]
                else:
                    location_top = {}
                #print 'location top:', location_top
                result_dict['location_top'] = json.dumps(location_top)
                # activity geo top
                if activity_geo_result:
                    sort_activity_geo = sorted(activity_geo_result.items(), key=lambda x:x[1], reverse=True)
                    activity_geo_top = sort_activity_geo[:50]
                else:
                    activity_geo_top = {}
                print 'activity_geo_top:', activity_geo_top
                result_dict['activity_geo_top'] = json.dumps(activity_geo_top)
                # keywords top
                if keywords_result:
                    sort_keywords = sorted(keywords_result.items(), key=lambda x:x[1], reverse=True)
                    keywords_top = sort_keywords[:50]
                else:
                    keywords_top = {}
                #print 'keywords_top:', keywords_top
                result_dict['keywords_top'] = json.dumps(keywords_top)
                # hashtag top
                if hashtag_result:
                    sort_hashtag = sorted(hashtag_result.items(), key=lambda x:x[1], reverse=True)
                    hashtag_top = sort_hashtag[:50]
                else:
                    hashtag_top = {}
                #print 'hashtag top:', hashtag_top
                result_dict['hashtag_top'] = json.dumps(hashtag_top)
                # topic top
                if topic_result:
                    sort_topic = sorted(topic_result.items(), key=lambda x:x[1], reverse=True)
                    topic_top = sort_topic[:50]
                else:
                    topic_top = {}
                #print 'topic top:', topic_top
                result_dict['topic_top'] = json.dumps(topic_top)
                # online_pattern top
                if online_pattern_result:
                    sort_online_pattern = sorted(online_pattern_result.items(), key=lambda x:x[1], reverse=True)
                    online_pattern_top = sort_online_pattern[:50]
                else:
                    online_pattern_top = {}
                #print 'online pattern top:', online_pattern_top
                result_dict['online_pattern_top'] = json.dumps(online_pattern_top)
                # domain top
                if domain_result:
                    sort_domain = sorted(domain_result.items(), key=lambda x:x[1], reverse=True)
                    domain_top = sort_domain[:20]
                    #test:
                    domain_top = [('education',50), ('art', 40), ('lawyer', 30), ('student', 20), ('media', 10), ('oversea',1)]
                else:
                    domain_top = {}
                #print 'domain top:', domain_top
                result_dict['domain_top'] = json.dumps(domain_top)
                #test need to add domain top user
                domain_top = [[u'媒体',1],[u'法律人士',1], [u'政府机构人士',1], [u'活跃人士',1], [u'媒体人士',1], [u'商业人士',1]]
                result_dict['domain_top_user'] = json.dumps(get_domain_top_user(domain_top))
                return result_dict 
            except Exception, r:
                print Exception, r
                return result_dict
        activity_result = es.mget(index='20130907', doc_type='bci', body={'ids':portrait_uid_list})['docs']
        for activity_item in activity_result:
            if activity_item['found']:
                activity_count += 1

    return result_dict

# origin retweeted number top 5 user and mid
def get_retweeted_top():
    top_results = []
    k = 100000
    count = 0
    now_ts = time.time()
    date = ts2datetime(now_ts-3600*24)
    index_time = ''.join(date.split('-'))
    # test
    index_time = '20130907'
    index_type = 'bci'
    query_body = {
        'query':{
            'match_all':{}
            },
        'size':k,
        'sort':[{'origin_weibo_retweeted_top_number':{'order':'desc'}}]
        }
    try:
        result = es_cluster.search(index=index_time, doc_type=index_type, body=query_body)['hits']['hits']
    except:
        return None
    #print 'result:', len(result)
    for item in result:
        if count==100:
            break
        uid = item['_id']
        try:
            exist_result = es.get(index='user_portrait', doc_type='user', id=uid)
            #print 'exist_result:', exist_result
            try:
                source = exist_result['_source']
                count += 1
                #print 'count:', count
                uname = source['uname']
                top_mid = item['_source']['origin_weibo_top_retweeted_id']
                top_retweeted_number = item['_source']['origin_weibo_retweeted_top_number']
                top_results.append([uid, uname, top_mid, top_retweeted_number])
            except:
                continue
        except:
            continue
    #print 'retweeted top user:', top_results
    return {'top_retweeted_user':json.dumps(top_results)}

# origin comment number top100 user and mid
def get_comment_top():
    top_results = []
    k = 100000
    count = 0
    now_ts = time.time()
    date = ts2datetime(now_ts - 3600*24)
    index_time = ''.join(date.split('-'))
    #test
    index_time = '20130907'
    index_type = 'bci'
    query_body = {
            'query':{
                'match_all':{}
                },
            'size':k,
            'sort':[{'origin_weibo_comment_top_number':{'order':'desc'}}]
            }
    try:
        result = es_cluster.search(index=index_time, doc_type=index_type, body=query_body)['hits']['hits']
        #print 'result:', result
    except:
        return None
    for item in result:
        if count == 100:
            break
        uid = item['_id']
        try:
            exist_result = es.get(index='user_portrait', doc_type='user', id=uid)
            try:
                source = exist_result['_source']
                count += 1
                uname = source['uname']
                top_mid = item['_source']['origin_weibo_top_comment_id']
                top_comment_number = item['_source']['origin_weibo_comment_top_number']
                top_results.append([uid, uname, top_mid, top_comment_number])
            except:
                continue
        except:
            continue
    #print 'top_results:', top_results
    return {'top_comment_user':json.dumps(top_results)}

# get activeness top 100
def get_activeness_top():
    result = []
    index_name = 'user_portrait'
    index_type = 'user'
    query_body = {'query':{'match_all':{}}, 'sort':[{'activeness':{'order': 'desc'}}], 'size':100}
    try:
        es_result = es.search(index=index_name, doc_type=index_type, body=query_body)['hits']['hits']
    except Exception, e:
        raise e
    if es_result:
        for user_dict in es_result:
            item = user_dict['_source']
            activeness = item['activeness']
            uname = item['uname']
            uid = item['uid']
            result.append([uid, uname, activeness])
    else:
        result = None
    #print 'result:', result
    return {'top_activeness': json.dumps(result)}

# get importance top 100
def get_importance_top():
    result = []
    index_name = 'user_portrait'
    index_type = 'user'
    query_body = {'query':{'match_all':{}}, 'sort':[{'importance':{'order':'desc'}}], 'size':100}
    try:
        es_result = es.search(index=index_name, doc_type=index_type, body=query_body)['hits']['hits']
    except Exception, e:
        raise e
    if es_result:
        for user_dict in es_result:
            item = user_dict['_source']
            importance = item['importance']
            uname = item['uname']
            uid = item['uid']
            result.append([uid, uname, importance])
    else:
        result = None
    #print 'result:', result
    return {'top_importance': json.dumps(result)}

# get influence top 100
def get_influence_top():
    result = []
    index_name = 'user_portrait'
    index_type = 'user'
    query_body = {'query':{'match_all':{}}, 'sort':[{'influence':{'order':'desc'}}], 'size':100}
    try:
        es_result = es.search(index=index_name, doc_type=index_type, body=query_body)['hits']['hits']
    except Exception, e:
        raise e
    if es_result:
        for user_dict in es_result:
            item = user_dict['_source']
            influence = item['influence']
            uname = item['uname']
            uid = item['uid']
            result.append([uid, uname, influence])
    else:
        result = None
    #print 'result:', result
    return {'top_influence': json.dumps(result)}

# get inlfuence vary top
def get_influence_vary_top():
    result = []
    query_body = {
        'query':{
            'match_all':{}
            },
        'size': 10000,
        'sort':[{'vary':{'order': 'desc'}}]
        }
    try:
        es_result =  es.search(index='vary', doc_type='bci', body=query_body)['hits']['hits']
    except Exception, e:
        raise e
    uid_list = [user_dict['_id'] for user_dict in es_result]
    #print 'uid_list:', uid_list
    portrait_result = es.mget(index='user_portrait', doc_type='user', body={'ids':uid_list}, _source=True)['docs']
    #print 'portrait_result:', portrait_result
    count = 0
    for i in range(len(portrait_result)):
        if count >=100:
            break
        #print 'portrait_result:', portrait_result
        if portrait_result[i]['found']:
            uid = portrait_result[i]['_source']['uid']
            uname = portrait_result[i]['_source']['uname']
            vary = es_result[i]['_source']['vary']
            result.append([uid, uname, vary])
            count += 1
        else:
            next
    #print 'result:', result
    return {'top_influence_vary': json.dumps(result)}

# get influence top count
def get_influence_top_count(top_threshold, user_count):
    query_body = {
            'query':{
                'filtered':{
                    'query':{
                        'match_all':{}
                        },
                    'filter':{
                        'range':{
                            'influence':{
                                'gte': top_threshold,
                                'lt': 3000
                                }
                            }
                        }
                    }
                }
            }
    result = es.count(index='user_portrait', doc_type='user', body=query_body)['count']
    #print 'result:', result
    return {'top_influence_ratio':float(result)/user_count}



# operate information: recomment in count , out count, compute count
def get_operate_information():
    result = dict()
    now_ts = time.time()
    date = ts2datetime(now_ts - 24*3600)
    #test
    date = '2013-09-07'
    delete_date = ''.join(date.split('-'))
    #test
    delete_date = '20150727'
    result['in_count'] = len(r_recomment.hkeys('recomment_'+str(date)))
    out_count_list = r_recomment.hget('recommend_delete_list', delete_date)
    #print 'out_count_list:', out_count_list
    if out_count_list:
        result['out_count'] = len(json.loads(out_count_list))
    else:
        result['out_count'] = 0
    compute_list = r_recomment.hkeys('compute')
    if compute_list:
        result['compute'] = len(compute_list)
    #print 'operate compute:', result
    return result


def save_result(results):
    hash_name = 'overview'
    for item in results:
        r_recomment.hset(hash_name, item, results[item])
    return True

def compute_overview():
    results = {}
    results['user_count'] = get_user_count()
    #results['total_status'] = get_total_status()
    scan_result = get_scan_results()
    #print 'scan_result:', scan_result
    results = dict(results, **scan_result)
    retweeted_top = get_retweeted_top()
    results = dict(results, **retweeted_top)
    comment_top = get_comment_top()
    results = dict(results, **comment_top)
    activeness_top = get_activeness_top()
    results = dict(results, **activeness_top)
    importance_top = get_importance_top()
    results = dict(results, **importance_top)
    influence_top = get_influence_top()
    results = dict(results, **influence_top)
    influence_vary_top = get_influence_vary_top()
    results = dict(results, **influence_vary_top)
    top_threshold = 900 # it can be changed
    top_influence_ratio = get_influence_top_count(top_threshold, results['user_count'])
    results = dict(results, **top_influence_ratio)
    operate_result = get_operate_information()
    results = dict(results, **operate_result)
    #print 'results:', results
    save_result(results)
    return results


if __name__=='__main__':
    compute_overview()
    #get_retweeted_top()
    #get_operate_information()
    #get_comment_top()
    #get_activeness_top()
    #get_importance_top()
    #get_influence_top()
    #get_influence_vary_top()
    #get_influence_top_count(900, 3795)
