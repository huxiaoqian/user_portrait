# -*- coding:utf-8 -*-

import math
import json

def influence_weibo_cal(total_number, average_number, top_number,brust):
    influence_weibo = 0.4*math.log(int(total_number)+1) + 0.2*math.log(int(average_number)+1) +0.15*math.log(int(top_number)+1) + 0.15*math.log(10*brust[0]+1) +0.1*math.log(10*brust[1]+1)
    return influence_weibo

def user_index_cal(origin_weibo_list, retweeted_weibo_list, user_fansnum, influence_origin_weibo_retweeted, influence_origin_weibo_comment, influence_retweeted_weibo_retweeted, influence_retweeted_weibo_comment):
    user_index = 300*(0.2*(0.6*math.log(len(origin_weibo_list)+1)+0.3*math.log(len(retweeted_weibo_list)+1)+0.1*math.log(int(user_fansnum)+1))+0.8*(0.3*influence_origin_weibo_retweeted+0.3*influence_origin_weibo_comment+0.2*influence_retweeted_weibo_retweeted+0.2*influence_retweeted_weibo_comment))
    return user_index
