# -*- coding: UTF-8 -*-
import sys
import time
import json
from cron_group import get_attr_bci
reload(sys)
sys.path.append('../../')
from time_utils import ts2datetime, datetime2ts

def basic_influence_info(uid_list):


def get_attr_influence(uid_list):
    result = {}
    bci_dict = get_attr_bci(uid_list)
    
    return result # result = {'influence': count}


if __name__ == '__main__':
    get_attr_influence(uid_list)
