# -*- coding: utf-8 -*-
import sys
import csv
import time
from user_portrait.global_utils import R_RECOMMENTATION as r
from user_portrait.time_utils import ts2datetime

# test use csv
'''
def recommentation_in(input_ts):
    date = ts2datetime(input_ts)
    results = []
    # read from csv
    try:
        csvfile = open(RECOMMENTATION_FILE_PATH + '/in_' + str(date) + '.csv', 'rb')
    except:
        print 'csvfile is not exists'
        return 'the recommentaion has not been computed'
    reader = csv.reader(csvfile)
    for line in reader:
        results.append(line)
    # read from redis
    return results
'''

def recommentation_in(input_ts):
    date = ts2datetime(input_ts)
    results = []
    # read from redis
    hash_name = 'recomment_'+str(date)
    results = r.hgetall(hashname)
    # search from user_profile to rich th show information
    return results


if __name__=='__main__':
    test_ts = 1378569600
    recommentation_in(test_ts)

