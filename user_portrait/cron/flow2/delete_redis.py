# -*- coding:utf-8 -*-
# 删除7天前的过期的redis数据：ip/activity/@;hashtag/sensitive_words;

import redis
import time
reload(sys)
sys.path.append("../../")
from time_utils import ts2datetime, datetime2ts
from global_utils import R_CLUSTER_FLOW2 as r_cluster

#删除

