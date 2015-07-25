# -*- coding: UTF-8 -*-
import sys
import time
import json
import math
from cron_group import get_attr_bci
reload(sys)
sys.path.append('../../')
from time_utils import ts2datetime, datetime2ts


def get_attr_influence(uid_list):
    result = {}
    weight = [0.3, 0.4, 0.2, 0.1]
    bci_dict = get_attr_bci(uid_list)
    print bci_dict
    influence = weight[0]*(0.3*math.log(1+bci_dict['origin_weibo_retweeted_top_number'])+0.3*math.log(1+bci_dict['origin_weibo_comment_top_number'])+\
            0.2*math.log(1+bci_dict['retweeted_weibo_retweeted_top_number'])+0.2*math.log(1+bci_dict['retweeted_weibo_comment_top_number'])) + \
            weight[1]*(0.3*math.log(1+bci_dict['origin_weibo_retweeted_average_number'])+0.3*math.log(1+bci_dict['origin_weibo_comment_average_number']) + \
            0.2*math.log(1+bci_dict['retweeted_weibo_retweeted_average_number'])+0.2*math.log(1+bci_dict['retweeted_weibo_comment_average_number'])) + \
            weight[2]*math.log(1+bci_dict['fans_number']) + weight[3]*math.log(1+bci_dict['total_weibo_number'])
    influence = 300 * influence

    result['influence'] = influence
    return result # result = {'influence': count}

if __name__ == "__main__":
    uid_list = ['2010832710', '3482838791', '3697357313', '2496434537',\
               '1642591402', '2074370833', '1640601392', '1773489534',\
               '2722498861', '2803301701']
    print get_attr_influence(uid_list)

