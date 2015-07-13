# -*- coding: UTF-8 -*-
'''
test save in a redis not in the cluster_redis
'''
import sys
import csv
import json
import time
import redis
from config import Day
reload(sys)
sys.path.append('../../')
from time_utils import ts2datetime, datetime2ts
from global_config import R_BEGIN_TIME
from global_utils import R_DICT

r_begin_ts = datetime2ts(R_BEGIN_TIME)

# two weeks retweet relation write to one db
# need add delete module
def get_db_num(timestamp):
    date = ts2datetime(timestamp)
    date_ts = datetime2ts(date)
    day_gap = ((date_ts - r_begin_ts) / Day) % (14 * 15)
    db_number = day_gap / 14
    print 'db_number:', db_number

    return db_number
    

# save redis as 'retweet_'+ str(uid):{r_uid1:count1, r_uid2:count2....}
def save_ruid(uid, r_uid, timestamp):
    db_number = get_db_num(timestamp)
    r = R_DICT[str(db_number)]
    r.hincrby('retweet_'+str(uid), str(r_uid), 1)
    r.hincrby('be_retweet_'+str(r_uid), str(uid), 1)

if __name__=='__main__':
    # test
    date1 = '2013-09-02'
    ts1 = datetime2ts(date1)
    date2 = '2013-09-15'
    ts2 = datetime2ts(date2)
    db_number = get_db_num(ts2)
    print 'r:', R_DICT[str(db_number)]
