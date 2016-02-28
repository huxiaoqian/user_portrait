# -*- coding: UTF-8 -*-
'''
update attribute of user portrait one month
update attr: character/domain/importance
update freq: one month
'''
import sys
import time
import json
from save_utils import save_user_results
from weibo_api_v3 import read_flow_text_sentiment, read_flow_text
from cron_text_attribute import domain_en2ch, get_fansnum_max
from evaluate_index import get_importance

#compute user domain
from domain.test_domain_v2 import domain_classfiy
#compute user character
from character.test_ch_sentiment import classfiy_sentiment
from character.test_ch_topic import classify_topic

sys.path.append('../../')
from global_utils import update_month_redis, UPDATE_MONTH_REDIS_KEY
from parameter import CHARACTER_TIME_GAP, DAY, WEIBO_API_INPUT_TYPE
from time_utils import ts2datetime, datetime2ts

#use to update attribute every week for character, domain
#write in version: 16-02-28
#this file run after the file: scan_es2redis_month.py function:scan_es2redis_month()
def update_attribute_month_v2():
    bulk_action = []
    count = 0
    user_list = []
    user_info_list = {}
    #get fansnum max
    fansnum_max = get_fansnum_max()
    start_ts = time.time()
    while True:
        r_user_info = update_month_redis.rpop(UPDATE_MONTH_REDIS_KEY)
        if r_user_info:
            r_user_info = json.loads(r_user_info)
            uid = r_user_info.keys()[0]
            count += 1
            user_info_list[uid] = r_user_info[uid]
        else:
            break
        if count % 1000 == 0:
            uid_list = user_info_list.keys()
            #acquire bulk user weibo data
            if WEIBO_API_INPUT_TYPE == 0:
                user_keywords_dict, user_weibo_dict = read_flow_text_sentiment(uid_list)
            else:
                user_keywords_dict, user_weibo_dict = read_flow_text(uid_list)
            #compute attribute--domain, character, importance
            #get user domain
            domain_results = domain_classfiy(uid_list, user_keywords_dict)
            domain_results_dict = domain_results[0]
            domain_results_label = domain_results[1]
            #get user character
            now_ts = time.time()
            #test
            now_ts = datetime2ts('2013-09-08')
            character_end_time = ts2datetime(now_ts - DAY)
            character_start_time = ts2datetime(now_ts - DAY * CHARACTER_TIME_GAP)
            character_sentiment_result_dict = classify_sentiment(uid_list, user_weibo_dict, character_start_time, character_end_time, WEIBO_API_INPUT_TYPE)
            character_text_result_dict = classify_topic(uid_list, user_keywords_dict)
            bulk_action = []
            for uid in uid_list:
                results = {}
                results['uid'] = uid
                #add user domain attribute
                user_domain_dict = domain_results_dict[uid]
                user_label_dict = domain_results_label[uid]
                results['domain_v3'] = json.dumps(user_domain_dict)
                results['domain'] = domain_en2ch(user_label_dict)

                #add user character_sentiment attribute
                character_sentiment = character_sentiment_result_dict[uid]
                results['character_sentiment'] = character_sentiment

                #add user character_text attribute
                character_text = character_text_result_dict[uid]
                results['character_text'] = character_text
                #get user importance
                user_topic_string = user_info_list[uid]['topic_string']
                user_fansnum = user_info_list[uid]['fansnum']
                results['importnace'] = get_importance(results['domain'], user_topic_string, user_fansnum, fansnum_max)
                #bulk action                                
                action = {'update':{'_id': uid}}
                bulk_action.extend([action, {'doc': results}])
            es_user_portrait.bulk(bulk_action, index=portrait_index_name, doc_type=portrait_index_type)
            end_ts = time.time()
            print '%s sec count 1000' % (end_ts - start_ts)
            start_ts = end_ts
    
    print 'count:', count
    
if __name__=='__main__':
    status = update_attribute_month_v2()
    print 'update week status:', status
