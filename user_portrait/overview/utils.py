# -*- coding: UTF-8 -*-
import sys
import json
from user_portrait.global_utils import R_RECOMMENTATION as r

hash_name = 'overview'

def get_attr(date):
    results = {}
    overview_result = r.hgetall(hash_name)
    #print 'overview_result:', overview_result
    for item in overview_result:
        value = overview_result[item]
        if isinstance(value, str):
            value = json.loads(value)
        results[item] = value
    #print 'overview result:', results
    return results


