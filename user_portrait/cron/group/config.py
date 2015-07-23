# -*- coding: UTF-8 -*-
#activeness weight dict used by evaluate_index.py
activeness_weight_dict = {'activity_time':0.3, 'activity_geo':0.2, 'statusnum':0.5}
#importance weight dict
importance_weight_dict = {'count':0.2, 'be_retweeted_out':0.3, 'be_retweeted_count_out': 0.1,'domain':0.2, 'topic':0.2}
#topic weight dict
topic_weight_dict = {'政治':0.3, '军事':0.15, '社会':0.15, '环境':0.05, \
                      '医药':0.05, '经济':0.05, '交通':0.05, '教育':0.05, \
                      '计算机':0.05, '艺术':0.05, '体育':0.05}
#domain weight dict
domain_weight_dict = {'文化':0.3, '媒体':0.3, '财经':0.1, '教育':0.1, \
                      '科技':0.05, '娱乐':0.05, '时尚':0.05, '体育':0.05}
#tightness weight dict
tightness_weight_dict = {'density':0.4, 'retweet_weibo_count':0.3, 'retweet_user_count':0.3}
