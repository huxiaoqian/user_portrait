# -*- coding: UTF-8 -*-
import sys
import json
import math
import time
from elasticsearch.helpers import scan
reload(sys)
sys.path.append('../../')
from global_utils import R_RECOMMENTATION as r
from global_utils import es_user_portrait, portrait_index_name, portrait_index_type
from global_utils import ES_DAILY_RANK as es_cluster
from global_utils import es_user_profile
from global_utils import R_RECOMMENTATION as r_recomment
from time_utils import ts2datetime, datetime2ts
from parameter import DAY, RUN_TYPE, RUN_TEST_TIME

basic_field = ['user_count', 'gender_ratio', 'location_top', 'verified_ratio']
behavior_field = ['total_status', 'keywords_top', 'activity_geo', 'hashtag_top',\
                  'topic_top', 'online_pattern_top']
user_field = ['domain_top', 'domain_top_user']
compute_field = ['recomment_in_count', 'recomment_out', 'compute_count']

# index_name = 'user_portrait'
# index_type = 'user'
portrait_index_name = 'user_portrait_1222'

#there have to add domain user top rank
def get_domain_top_user(domain_top):
    result = {}
    domain_user = {}
    #test user list
    """
    test_user_list = [['2803301701', '1639498782', '2656274875', '1402977920', '3114175427'], \
                      ['3575186384', '1316683401', '1894603174', '1641542052', '1068248497'], \
                      ['1729736051', '1396715380', '2377610962', '1828183230', '2718018210'], \
                      ['1250748474', '3270699555', '1417037145', '1193111400', '1403915120'], \
                      ['1671342103', '1255849511', '1647497355', '1989660417', '1189729754'], \
                      ['1182391231', '1670071920', '1689618340', '1494850741', '1708942053'],\
                      ['3400918220', '2685504141', '2056115850', '1768001547', '3317008062'],\
                      ['2001627641', '1773489534', '2458194884', '1822155333', '1799201635'],\
                      ['1709157165', '2074370833', '2167425990', '3204839810', '3690518992'],\
                      ['1664065962', '3299094722', '1942531237', '2799434700', '1784404677'],\
                      ['1218353337', '1761179351', '3482911112', '1220291284', '2504433601'],\
                      ['3682473195', '1627673351', '1779065471', '3316144700', '1896701827']]
    """
    count = 0
    k = 5
    for item in domain_top:
        domain = item[0]
        #test
        #user_list = test_user_list[count]
        result[domain] = []
        query_body = {
            'query':{
                'filtered':{
                    'filter':{'term':{'domain':domain}}    
                }
            },
            'size':k,
            'sort':[{'influence':{'order':'desc'}}]
        }
        profile_result = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type, \
                body=query_body, _source=False, fields=['uid', 'uname', 'photo_url'])['hits']['hits']
        for profile in profile_result:
            uid = profile['_id']
            try:
                uname = profile['fields']['uname'][0]
                photo_url = profile['fields']['photo_url'][0]
            except:
                uname = 'unknown'
                photo_url = 'unknown'
            result[domain].append([uid, uname, photo_url])
        count += 1
    return result

# there have to add topic user top rank
def get_topic_top_user(topic_top):
    result = {}
    topic_user = {}
    #test user list
    """
    test_user_list = [['1499104401', '1265965213', '3270699555', '2073915493', '1686474312'],\
                      ['2803301701', '2105426467', '1665372775', '3716504593', '2892376557'],\
                      ['1457530250', '1698513182', '2793591492', '2218894100', '1737961042'],\
                      ['1656818110', '1660127070', '1890124610', '1182391230', '1243861100'],\
                      ['1680430844', '2998045524', '2202896360', '1639498782', '3494698730'],\
                      ['2587093162', '1677675054', '1871767009', '1193111400', '1672418622'],\
                      ['1730726640', '1752502540', '1868725480', '1262486750', '1235733080'],\
                      ['1250041100', '2275231150', '1268642530', '1658606270', '1857599860'],\
                      ['1929496477', '2167425990', '1164667670', '2417139911', '1708853044'],\
                      ['1993292930', '1645823930', '1890926610', '1641561810', '2023833990'],\
                      ['2005471590', '1233628160', '2074684140', '1396715380', '1236762250'],\
                      ['1423592890', '2612799560', '1926127090', '2684951180', '1760607220']]
    """
    count = 0
    k = 5
    for item in topic_top:
        topic = item[0]
        #test
        #user_list = test_user_list[count]
        result[topic] = []
        query_body = {
            'query':{
                'wildcard':{'topic_string':'*'+topic+'*'}
            },
            'size':k,
            'sort':[{'influence':{'order':'desc'}}]
        }
        profile_result = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type, \
                body=query_body, _source=False, fields=['uid', 'uname', 'photo_url'])['hits']['hits']
        for profile in profile_result:
            uid = profile['_id']
            try:
                uname = profile['fields']['uname'][0]
                photo_url = profile['fields']['photo_url'][0]
            except:
                uname = 'unknown'
                photo_url = 'unknown'
            result[topic].append([uid, uname, photo_url])
        count += 1
    return result


def get_user_count():
    count = 0
    query_body = {
            'query':{
                'match_all':{}
                }
            }
    count = es_user_portrait.count(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)['count']
    return count


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
    s_re = scan(es_user_portrait, query={'query':{'match_all':{}}, 'size':100}, index=portrait_index_name, doc_type=portrait_index_type)
    print 's_re:', s_re
    activity_count = 0
    while True:
        portrait_uid_list = []
        while True:
            try:
                scan_re = s_re.next()['_source']
                # gender ratio count
                portrait_uid_list.append(scan_re['uid'])
                #print 'portrait_uid_list:', len(portrait_uid_list)
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
                    if activity_geo:
                        activity_geo_dict = json.loads(activity_geo)[-1]
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
                    topic = scan_re['topic_string']
                    if topic:
                        topic_list = topic.split('&')
                        for item in topic_list:
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
                        try:
                            domain_result[domain] += 1
                        except:
                            domain_result[domain] = 1
                except:
                        no_domain_count += 1
            except StopIteration:
                print 'all done'
                now_ts = time.time()
                now_date = ts2datetime(now_ts - DAY)
                index_time = ''.join(now_date.split('-'))
                #test
                index_time = '20130907'
                # gender ratio count
                #count = sum(gender_result.values())
                all_count = es_user_portrait.count(index=portrait_index_name,doc_type=portrait_index_type,\
                    body={'query':{'match_all':{}}})['count']
                count = all_count
                print "count:",count
                gender_ratio = {'1':float(gender_result['1']) / count, '2':float(gender_result['2']) / count}
                #print 'gender ratio:', gender_ratio
                activity_result = es_user_portrait.mget(index='bci_'+index_time, doc_type='bci', body={'ids':portrait_uid_list})['docs']
                for activity_item in activity_result:
                    if activity_item['found']:
                        activity_count += 1
                #print 'activity_count:', activity_count
                result_dict['activity_count'] = float(activity_count) / count
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
                #print 'activity_geo_top:', activity_geo_top
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
                    #domain_top = [('education',50), ('art', 40), ('lawyer', 30), ('student', 20), ('media', 10), ('oversea',1)]
                else:
                    domain_top = {}
                #print 'domain top:', domain_top
                result_dict['domain_top'] = json.dumps(domain_top)
                #test need to add domain top user
                #domain_top = [[u'媒体',1],[u'法律人士',1], [u'政府机构人士',1], [u'活跃人士',1], [u'媒体人士',1], [u'商业人士',1],\
                #              [u'高校微博', 1], [u'境内机构', 1], [u'境外机构', 1], [u'民间组织',1], [u'草根',1], [u'其他', 1]]
                result_dict['domain_top_user'] = json.dumps(get_domain_top_user(domain_top))
                #test need to add topic user
                #topic_top = [[u'军事', 1], [u'政治',1], [u'体育',1], [u'计算机',1], [u'民生',1], [u'生活',1],\
                #              [u'娱乐',1], [u'健康',1], [u'交通',1], [u'经济',1], [u'教育',1], [u'自然',1]]
                result_dict['topic_top_user'] = json.dumps(get_topic_top_user(topic_top))
                return result_dict 
            except Exception, r:
                print Exception, r
                return result_dict
        #print 'portrait_uid_list:', len(portrait_uid_list)
        activity_result = es.mget(index='20130907', doc_type='bci', body={'ids':portrait_uid_list})['docs']
        for activity_item in activity_result:
            if activity_item['found']:
                activity_count += 1
    return result_dict

def get_scan_results_v2():
    result_dict = dict()

    # gender ratio count
    query_body = {
        "query":{
            "match_all":{}
            },
        "aggs":{
            "all_interests":{
                "terms":{"field":"gender"}
            }
        }
    }

    search_results = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)["aggregations"]['all_interests']['buckets']
    gender_result = dict()
    for item in search_results:
        gender_result[str(item['key'])] = item['doc_count']
    count = sum(gender_result.values())
    if count==0:
        gender_ratio = {'1':0.5, '2':0.5}
    else:
        gender_ratio = {'1':float(gender_result['1']) / count, '2':float(gender_result['2']) / count}
    result_dict['gender_ratio'] = json.dumps(gender_ratio)

    # verified ratio count
    query_body = {
        "query":{
            "match_all":{}
            },
        "aggs":{
            "all_interests":{
                "terms":{"field":"verified"}
            }
        }
    }

    search_results = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)["aggregations"]['all_interests']['buckets']
    verified_result = dict()
    for item in search_results:
        verified_result[item['key']] = item['doc_count']
    count = sum(verified_result.values())
    if count==0:
        verified_ratio = {'yes':0.5, 'no':0.5}
    else:
        verified_ratio = {'yes':float(verified_result['']) / count, 'no':float(verified_result['unknown'])/count}
    result_dict['verified_ratio'] = json.dumps(verified_ratio)

    # loation top
    query_body = {
        "query":{
            "match_all":{}
            },
        "aggs":{
            "all_interests":{
                "terms":{"field":"location","size":5}
            }
        }
    }

    search_results = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)["aggregations"]['all_interests']['buckets']
    if len(search_results):
        location_top = []
        for item in search_results:
            location_top.append([item['key'],item['doc_count']])
    else:
        location_top = {}
    result_dict['location_top'] = json.dumps(location_top)
    
    # activity geo
    
    query_body = {
        "query":{
            "match_all":{}
            },
        "aggs":{
            "all_interests":{
                "terms":{"field":"activity_geo_aggs","size":50}
            }
        }
    }

    search_results = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)["aggregations"]['all_interests']['buckets']
    if len(search_results):
        activity_geo_top = []
        for item in search_results:
            activity_geo_top.append([item['key'],item['doc_count']])
    else:
        activity_geo_top = {}
    activity_geo_top = sorted(activity_geo_top,key=lambda activity_geo_top:activity_geo_top[1],reverse=True)
    print "activity_geo_top:",activity_geo_top
    result_dict['activity_geo_top'] = json.dumps(activity_geo_top)
    
    # keywords
    query_body = {
        "query":{
            "match_all":{}
            },
        "aggs":{
            "all_interests":{
                "terms":{"field":"keywords_string","size":50}
            }
        }
    }

    search_results = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)["aggregations"]['all_interests']['buckets']
    if len(search_results):
        keywords_top = []
        for item in search_results:
            keywords_top.append([item['key'],item['doc_count']])
    else:
        keywords_top = {}
    result_dict['keywords_top'] = json.dumps(keywords_top)

    # hashtag top
    query_body = {
        "query":{
            "match_all":{}
            },
        "aggs":{
            "all_interests":{
                "terms":{"field":"hashtag","size":50}
            }
        }
    }

    search_results = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)["aggregations"]['all_interests']['buckets']
    if len(search_results):
        hashtag_top = []
        for item in search_results:
            hashtag_top.append([item['key'],item['doc_count']])
    else:
        hashtag_top = {}
    hashtag_top = sorted(hashtag_top,key=lambda hashtag_top:hashtag_top[1],reverse=True)

    result_dict['hashtag_top'] = json.dumps(hashtag_top)

    # topic top
    query_body = {
        "query":{
            "match_all":{}
            },
        "aggs":{
            "all_interests":{
                "terms":{"field":"topic_string","size":50}
            }
        }
    }

    search_results = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)["aggregations"]['all_interests']['buckets']
    if len(search_results):
        topic_top = []
        for item in search_results:
            topic_top.append([item['key'],item['doc_count']])
    else:
        topic_top = {}
    result_dict['topic_top'] = json.dumps(topic_top)

    # domain top
    query_body = {
        "query":{
            "match_all":{}
            },
        "aggs":{
            "all_interests":{
                "terms":{"field":"domain","size":20}
            }
        }
    }

    search_results = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)["aggregations"]['all_interests']['buckets']
    if len(search_results):
        domain_top = []
        for item in search_results:
            domain_top.append([item['key'],item['doc_count']])
    else:
        domain_top = {}
    result_dict['domain_top'] = json.dumps(domain_top)
    result_dict['domain_top_user'] = json.dumps(get_domain_top_user(domain_top))
    result_dict['topic_top_user'] = json.dumps(get_topic_top_user(topic_top))
    
    # online pattern top
    query_body = {
        "query":{
            "match_all":{}
            },
        "aggs":{
            "all_interests":{
                "terms":{"field":"online_pattern_aggs","size":50}
            }
        }
    }

    search_results = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)["aggregations"]['all_interests']['buckets']
    if len(search_results):
        online_pattern_top = []
        for item in search_results:
            online_pattern_top.append([item['key'],item['doc_count']])
    else:
        online_pattern_top = {}
    result_dict['online_pattern_top'] = json.dumps(online_pattern_top)
    
    # activity_count
    no_activity_count = es_user_portrait.count(index=portrait_index_name, doc_type=portrait_index_type, \
            body={'query':{'filtered':{'filter':{'term':{'influence': 0}}}}})['count']
    all_count = es_user_portrait.count(index=portrait_index_name, doc_type=portrait_index_type ,\
            body={'query':{'match_all':{}}})['count']
    result_dict['activity_count'] = 1 - float(no_activity_count) / all_count

    return result_dict

# origin retweeted number top 5 user and mid
def get_retweeted_top():
    top_results = []
    k = 10000
    count = 0
    #run_type
    if RUN_TYPE == 1:
        now_ts = time.time()
    else:
        now_ts = datetime2ts(RUN_TEST_TIME)

    date = ts2datetime(now_ts-DAY)
    index_time = ''.join(date.split('-'))
    
    index_type = 'bci'
    query_body = {
        'query':{
            'match_all':{}
            },
        'size':k,
        'sort':[{'origin_weibo_retweeted_top_number':{'order':'desc'}}]
        }
    try:
        result = es_cluster.search(index='bci_'+index_time, doc_type=index_type, body=query_body)['hits']['hits']
    except:
        return None
    for item in result:
        if count == 100:
            break
        uid = item['_id']
        try:
            exist_result = es_user_portrait.get(index=portrait_index_name, doc_type=portrait_index_type, id=uid)
            try:
                source = exist_result['_source']
                count += 1
                uname = source['uname']
                top_mid = item['_source']['origin_weibo_top_retweeted_id']
                top_retweeted_number = item['_source']['origin_weibo_retweeted_top_number']
                top_results.append([uid, uname, top_mid, top_retweeted_number])
            except:
                continue
        except:
            continue
    top_results = sorted(top_results,key=lambda top_results:top_results[3],reverse=True)
    
    return {'top_retweeted_user':json.dumps(top_results)}

# origin comment number top100 user and mid
def get_comment_top():
    top_results = []
    k = 10000
    count = 0
    #run_type
    if RUN_TYPE == 1:
        now_ts = time.time()
    else:
        now_ts = datetime2ts(RUN_TEST_TIME)
    date = ts2datetime(now_ts - DAY)
    index_time = ''.join(date.split('-'))
    index_type = 'bci'
    query_body = {
            'query':{
                'match_all':{}
                },
            'size':k,
            'sort':[{'origin_weibo_comment_top_number':{'order':'desc'}}]
            }
    try:
        result = es_cluster.search(index='bci_'+index_time, doc_type=index_type, body=query_body)['hits']['hits']
    except:
        return None
    for item in result:
        if count == 100:
            break
        uid = item['_id']
        try:
            exist_result = es_user_portrait.get(index=portrait_index_name, doc_type=portrait_index_type, id=uid)
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
    top_results = sorted(top_results,key=lambda top_results:top_results[3],reverse=True)
    return {'top_comment_user':json.dumps(top_results)}

# get activeness top 100
def get_activeness_top():
    result = []
    query_body = {'query':{'match_all':{}}, 'sort':[{'activeness':{'order': 'desc'}}], 'size':100}
    try:
        es_result = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)['hits']['hits']
    except Exception, e:
        es_result = None
    if es_result:
        max_eval = get_evaluate_max()
        for user_dict in es_result:
            item = user_dict['_source']
            activeness = item['activeness']
            activeness = math.log(activeness/max_eval['activeness'] * 9 + 1 ,10)
            activeness = activeness * 100
            uname = item['uname']
            uid = item['uid']
            result.append([uid, uname, activeness])
    else:
        result = None
    result = sorted(result,key=lambda result:result[2],reverse=True)
    #print "activeness result",result
    return {'top_activeness': json.dumps(result)}

# get importance top 100
def get_importance_top():
    result = []
    query_body = {'query':{'match_all':{}}, 'sort':[{'importance':{'order':'desc'}}], 'size':100}
    try:
        es_result = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)['hits']['hits']
    except Exception, e:
        es_result = None
    if es_result:
        max_eval = get_evaluate_max()
        for user_dict in es_result:
            item = user_dict['_source']
            importance = item['importance']
            importance = math.log(importance/max_eval['importance'] * 9 + 1 ,10)
            importance = importance * 100
            uname = item['uname']
            uid = item['uid']
            result.append([uid, uname, importance])
    else:
        result = None
    result = sorted(result,key=lambda result:result[2],reverse=True)
    return {'top_importance': json.dumps(result)}


def get_evaluate_max():
    max_result = {}
    index_name = 'user_portrait_1222'
    index_type = 'user'
    evaluate_index = ['activeness', 'importance', 'influence']
    for evaluate in evaluate_index:
        query_body = {
            'query':{
                'match_all':{}
                },
            'size':1,
            'sort':[{evaluate: {'order': 'desc'}}]
            }
        try:
            result = es_user_portrait.search(index=index_name, doc_type=index_type, body=query_body)['hits']['hits']
        except Exception, e:
            raise e
        max_evaluate = result[0]['_source'][evaluate]
        max_result[evaluate] = max_evaluate
    #print 'result:', max_result
    return max_result


# get influence top 100
def get_influence_top():
    result = []
    query_body = {'query':{'match_all':{}}, 'sort':[{'influence':{'order':'desc'}}], 'size':100}
    try:
        es_result = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)['hits']['hits']
    except Exception, e:
        es_result = None
    if es_result:
        max_eval = get_evaluate_max()
        
        for user_dict in es_result:
            item = user_dict['_source']
            influence = item['influence']
            influence = math.log(influence/max_eval['influence'] * 9 + 1 ,10)
            influence = influence * 100
            uname = item['uname']
            uid = item['uid']
            result.append([uid, uname, influence])
    else:
        result = None
    result = sorted(result,key=lambda result:result[2],reverse=True)
    return {'top_influence': json.dumps(result)}

# abandon in version: 16-02-28
# get inlfuence vary top
'''
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
        es_result =  es_user_portrait.search(index='vary', doc_type='bci', body=query_body)['hits']['hits']
    except Exception, e:
        raise e
    uid_list = [user_dict['_id'] for user_dict in es_result]
    portrait_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type, body={'ids':uid_list}, _source=True)['docs']
    count = 0
    for i in range(len(portrait_result)):
        if count >=100:
            break
        if portrait_result[i]['found']:
            uid = portrait_result[i]['_source']['uid']
            uname = portrait_result[i]['_source']['uname']
            vary = es_result[i]['_source']['vary']
            result.append([uid, uname, vary])
            count += 1
        else:
            next
    return {'top_influence_vary': json.dumps(result)}
'''

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
    result = es_user_portrait.count(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)['count']
    return {'top_influence_ratio':float(result)/user_count}



# operate information: recomment in count , out count, compute count
def get_operate_information():
    result = dict()
    #run_type
    if RUN_TYPE == 1:
        now_ts = time.time()
    else:
        now_ts = datetime2ts(RUN_TEST_TIME)

    date = ts2datetime(now_ts - DAY)
    delete_date = ''.join(date.split('-'))
    result['in_count'] = len(r_recomment.hkeys('recomment_'+str(date)))
    out_count_list = r_recomment.hget('recommend_delete_list', delete_date)
    if out_count_list:
        result['out_count'] = len(json.loads(out_count_list))
    else:
        result['out_count'] = 0
    compute_list = r_recomment.hkeys('compute')
    
    if compute_list:
        result['compute'] = len(compute_list)
    else:
        result['compute'] = 0
    
    return result


def save_result(results):
    hash_name = 'overview'
    for item in results:
        r_recomment.hset(hash_name, item, results[item])
    return True

def compute_overview():
    results = {}
    results['user_count'] = get_user_count()
    #scan_result = get_scan_results_v2()
    scan_result = get_scan_results()
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
    top_threshold = 900 # it can be changed
    top_influence_ratio = get_influence_top_count(top_threshold, results['user_count'])
    results = dict(results, **top_influence_ratio)
    operate_result = get_operate_information()
    results = dict(results, **operate_result)
    save_result(results)
    


if __name__=='__main__':
    log_ts = time.time()
    log_date = ts2datetime(log_ts)
    print 'cron/overview/cron_overview.py&start&' + log_date

    compute_overview()

    log_ts = time.time()
    log_date = ts2datetime(log_ts)
    print 'cron/overview/cron_overview.py&end&' + log_date

