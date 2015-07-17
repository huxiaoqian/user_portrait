# -*- coding: UTF-8 -*-
'''
use to update the attribute of user portrait
update frequence: one day
update attribute: activeness, importance, influence
'''
import sys
import json
import time
from save_utils import update_day
reload(sys)
sys.path.append('../../')
from global_utils import es_user_portrait as es

def update_attribute_day():
    #scan the user_portrait and bulk action to update
    status = False
    bulk_action = []
    status = update_day(bulk_action)
    return status


if __name__=='__main__':
    status = update_attribute_day()
    print 'update attribute week status:', status
