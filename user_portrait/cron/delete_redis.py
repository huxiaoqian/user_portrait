# -*- coding:utf-8 -*-
# 删除7天前的过期的redis数据：ip/activity/@;hashtag/sensitive_words;

import redis
import time
reload(sys)
sys.path.append("../../")
from time_utils import ts2datetime, datetime2ts
from global_utils import R_CLUSTER_FLOW2 as r_cluster
from global_utils import R_RECOMMENTATION as r
from global_utils import EXPIRE_TIME

now_ts = time.time()
delete_ts = datetime2ts(ts2datetime(now_ts-EXPIRE_TIME))  #待删除的时间戳
delete_date = ts2datetime(now_ts-EXPIRE_TIME)

#delete @
r_cluster.delete("at_"+str(delete_ts))

#delete ip
r_cluster.delete('new_ip_'+str(delete_ts))

#delete activity
r_cluster.delete('activity_'+str(delete_ts))

#delete hashtag
r_cluster.delete('hashtag_'+str(delete_ts))

#delete sensitive words
r_cluster.delete('sensitive_'+str(delete_ts))

#delete recommendation
r.delete('recomment_'+str(delete_date))


