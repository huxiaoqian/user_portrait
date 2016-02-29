# -*- coding: utf-8 -*-

import redis
from elasticsearch import Elasticsearch
from rediscluster import RedisCluster
from global_config import ZMQ_VENT_PORT_FLOW1, ZMQ_CTRL_VENT_PORT_FLOW1, ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_HOST_FLOW1, BIN_FILE_PATH
from global_config import REDIS_CLUSTER_HOST_FLOW1, REDIS_CLUSTER_PORT_FLOW1,\
                          REDIS_CLUSTER_HOST_FLOW2, REDIS_CLUSTER_PORT_FLOW2,\
                          REDIS_HOST, REDIS_PORT
from global_config import WEIBO_API_HOST, WEIBO_API_PORT
from global_config import USER_PROFILE_ES_HOST, USER_PROFILE_ES_PORT, ES_CLUSTER_HOST_FLOW1,\
                          USER_PORTRAIT_ES_HOST, USER_PORTRAIT_ES_PORT,\
                          FLOW_TEXT_ES_HOST, FLOW_TEXT_ES_PORT
from global_config import UNAME2UID_HOST, UNAME2UID_PORT
from global_config import RETWEET_REDIS_HOST, RETWEET_REDIS_PORT
from global_config import COMMENT_REDIS_HOST, COMMENT_REDIS_PORT

#uname2uid redis
uname2uid_redis = redis.StrictRedis(host=UNAME2UID_HOST, port=UNAME2UID_PORT)

def _default_cluster_redis(host=REDIS_CLUSTER_HOST_FLOW1, port=REDIS_CLUSTER_PORT_FLOW1):
    startup_nodes = [{'host':host, 'port':port}]
    weibo_redis = RedisCluster(startup_nodes = startup_nodes)
    return weibo_redis

R_CLUSTER_FLOW1 = _default_cluster_redis(host=REDIS_CLUSTER_HOST_FLOW1, port=REDIS_CLUSTER_PORT_FLOW1)
R_CLUSTER_FLOW2 = _default_cluster_redis(host=REDIS_CLUSTER_HOST_FLOW2, port=REDIS_CLUSTER_PORT_FLOW2)

def _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=1):
    return redis.StrictRedis(host, port, db)

redis_host_list = ["1", "2"]
#use to save retweet/be_retweet
retweet_r_1 = _default_redis(host=RETWEET_REDIS_HOST,port=RETWEET_REDIS_PORT, db=1)
retweet_r_2 = _default_redis(host=RETWEET_REDIS_HOST, port=RETWEET_REDIS_PORT, db=2)
retweet_redis_dict = {'1':retweet_r_1, '2':retweet_r_2}
#use to save comment/be_comment
comment_r_1 = _default_redis(host=COMMENT_REDIS_HOST, port=COMMENT_REDIS_PORT, db=1)
comment_r_2 = _default_redis(host=COMMENT_REDIS_HOST, port=COMMENT_REDIS_PORT, db=2)
comment_redis_dict = {'1':comment_r_1, '2':comment_r_2}



R_0 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
R_1 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=1)
R_2 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=2)
R_3 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=3)
R_4 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=4)
R_5 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=5)
R_6 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=6)
R_7 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=7)
R_8 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=8)
R_9 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=9)
R_10 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=10)
R_11 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=11)
R_12 = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=12)

R_DICT = {'0':R_0, '1':R_1, '2':R_2, '3':R_3, '4':R_4, '5':R_5, '6':R_6, '7':R_7,\
          '8':R_8, '9':R_9, '10':R_10, '11':R_11, '12':R_12}


# use to write group task
# two type data----group task;  group task members
# type1 list: group_task  index   group_task_basic_information
# type2 list: group_task_name index group_task_members
R_GROUP = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=14)
group_detect_queue_name = 'group_detect_task'
group_analysis_queue_name = 'group_analysis_task'

# social sensing redis
R_SOCIAL_SENSING = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=14)

# use to recomment 
#two types hash
#type1:{recomment_2013-09-01:{uid:status, uid:status}} status:0 not in  status:1 have in
#type2:{compute:{uid:[in_date,status], uid:[in_date, status]}} status:0 not compute status:1 computing 
R_RECOMMENTATION = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=15)

R_RECOMMENTATION_OUT = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=15)
# type: hash----{recommend_delete_list, 20130901, list}
# type: hash----{decide_delete_list, 20130901, list}

R_ADMIN = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=15)
# type: hash ----{admin, username, password}

#use to write portrait user list to redis as queue for update_day and update_week
update_day_redis = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=5)
UPDATE_DAY_REDIS_KEY = 'update_day'
update_week_redis  = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=5)
UPDATE_WEEK_REDIS_KEY = 'update_week'
update_month_redis = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=5)
UPDATE_MONTH_REDIS_KEY = 'update_month'

# elasticsearch initialize, one for user_profile, one for user_portrait
es_user_profile = Elasticsearch(USER_PORTRAIT_ES_HOST, timeout = 600)
es_user_portrait = Elasticsearch(USER_PORTRAIT_ES_HOST, timeout = 6000)
es_flow_text = Elasticsearch(FLOW_TEXT_ES_HOST, timeout=600)
es_group_result = Elasticsearch(USER_PORTRAIT_ES_HOST, time_out=600)
es_retweet = Elasticsearch(USER_PORTRAIT_ES_HOST, timeout = 600)
es_comment = Elasticsearch(USER_PORTRAIT_ES_HOST, timeout = 600)
es_copy_portrait = Elasticsearch(USER_PORTRAIT_ES_HOST, timeout = 600)
es_tag = Elasticsearch(USER_PORTRAIT_ES_HOST, timeout=600)

# elasticsearch index_name and index_type
profile_index_name = 'weibo_user'  # user profile es
profile_index_type = 'user'
portrait_index_name = 'user_portrait_1222' # user portrait
portrait_index_type = 'user'
flow_text_index_name_pre = 'flow_text_' # flow text: 'flow_text_2013-09-01'
flow_text_index_type = 'text'
# week retweet/be_retweet relation es
retweet_index_name_pre = '1225_retweet_' # retweet: 'retweet_1' or 'retweet_2'
retweet_index_type = 'user'
be_retweet_index_name_pre = '1225_be_retweet_' #be_retweet: 'be_retweet_1'/'be_retweet_2'
be_retweet_index_type = 'user'
# week comment/be_comment relation es
comment_index_name_pre = '1225_comment_'
comment_index_type = 'user'
be_comment_index_name_pre = '1225_be_comment_'
be_comment_index_type = 'user'
# es for activeness history, influence history and pagerank
copy_portrait_index_name = 'this_is_a_copy_user_portrait'
copy_portrait_index_type = 'manage'
# es for group detect and analysis
group_index_name = 'group_manage'
group_index_type = 'group'

# es for tag
tag_index_name = 'custom_attribute'
tag_index_type = 'attribute'
#use to load balck words of weibo keywords
BLACK_WORDS_PATH = '/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/text_attribute/black.txt'

def load_black_words():
    black_words = set([line.strip('\r\n') for line in file(BLACK_WORDS_PATH)])
    return black_words

black_words = load_black_words()


def _default_es_cluster_flow1(host=ES_CLUSTER_HOST_FLOW1):
    es = Elasticsearch(host, timeout=60, retry_on_timeout=True, max_retries=6)
    return es

ES_CLUSTER_FLOW1 = _default_es_cluster_flow1(host=ES_CLUSTER_HOST_FLOW1)

def get_client(api_host=WEIBO_API_HOST, api_port=WEIBO_API_PORT):
    return Client(api_host, api_port)

ES_DAILY_RANK = _default_es_cluster_flow1(host=ES_CLUSTER_HOST_FLOW1)


