# -*- coding: utf-8 -*-

import time
import sys
from elasticsearch import Elasticsearch

reload(sys)
sys.path.append('./../../')
from global_utils import ES_CLUSTER_FLOW1

es = ES_CLUSTER_FLOW1
index_type = "bci"

def search_rank(index_name, start_point, size, index_type="bci"):
    query_body={
        "query": {
            "match_all": {}
            },
        "sort": [{"user_index": {"order": "desc"}}],
        "from": start_point,
        "size": size

    }

    result = es.search(index=index_name, doc_type=index_type, body=query_body, _source=False)['hits']['hits']

    return result

def update_index_action(data, attribute, attribute_value):

    """
    attribute: new updated attribute
        rank: the user_index rank of the user_id
    """

    _id = data["user"]
    action = {"update": {"_id": _id}}
    xdata = {"doc": {attribute: attribute_value}}
    return action, xdata

if __name__ == "__main__":

    """
    update all user in a day
    """

    index_name = "20130903"
    user_rank = 0
    bulk_action = []
    n_range = range(0,300000,10000)
    tb = time.time()

    for left_range in n_range:
        result = search_rank(index_name, left_range, 10000)

        for item in result:
            update_info = {}
            user_rank += 1
            update_info["user"] = item["_id"]
            update_info["rank"] = user_rank

            x = update_index_action(update_info, "rank", user_rank)
            bulk_action.extend((x[0], x[1]))

            if user_rank % 1000 == 0:
                while 1:
                    try:
                        es.bulk(bulk_action, index=index_name, doc_type="bci", timeout=30)
                        bulk_action = []
                        break
                    except Exception, r:
                        print Exception, " :", r
                        es = Elasticsearch("219.224.135.93:9200", timeout=60)
                print user_rank

            if user_rank % 10000 == 0:
                ts = time.time()
                print "%s : %s" %(user_rank, ts - tb)
                tb = ts

    if bulk_action:
        es.bulk(bulk_action, index=index_name, doc_type="bci", timeout=30)
    print "finish !"

