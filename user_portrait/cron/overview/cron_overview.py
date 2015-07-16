# -*- coding: UTF-8 -*-
import sys
import json
import time
reload(sys)
sys.path.append('../../')
from global_utils import R_RECOMMENTATION as r
from global_utils import es_user_portrait
from time_utils import ts2datetime, datetime2ts


def get_gender_ratio():
    results = {}

    return results

def compute_overview():
    results = {}
    # level1-attr1: number of user in user_portrait
    query_body = {
            'query':{
                'match_all':{}
                }
            }
    count = es_user_portrait.count(index = 'user_portrait', doc_type='user', body=query_body)['count']
    print 'user portrait count:', count
    results['count'] = count
    # level-atr2: gender ratio
    gender_ratio = get_gender_ratio() # {'male':count1, 'female':count2}


if __name__=='__main__':
    compute_overview()
