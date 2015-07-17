# -*- coding: UTF-8 -*-
'''
update attribute of user portrait one week
update attr: text attribute
update freq: one week
'''
import sys
import time
import json
from save_utils import update_week
reload(sys)
sys.path.append('../../')
from global_utils import es_user_portrait as es

def update_atttribute_week():
    status = False
    bulk_action = []
    status = update_week(bulk_action)
    return status


if __name__=='__main__':
    status = update_attribute_week()
    print 'update week status:', status
