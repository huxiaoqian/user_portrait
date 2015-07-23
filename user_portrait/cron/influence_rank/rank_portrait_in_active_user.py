# -*- coding = utf-8 -*-

import sys
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

reload(sys)
sys.path.append('./../../')
from global_utils import ES_CLUSTER_FLOW1

es = ES_CLUSTER_FLOW1
index_name = "20130901"

def search_k(es, index_name, index_type, start, size=100):
    query_body = {
        "query":{
            "match_all": {}
            },
        "size": size,
        "from": start,
        "sort": [{"user_index": {"order": "desc"}}]
    }

    result = es.search(index=index_name, doc_type=index_type, body=query_body)['hits']['hits']

    search_list = []
    for item in result:
        search_list.append(item['_source'])

    return search_list

def search_portrait_user_in_activity(es, number, active_index, active_type, portrait_index, portrait_type):

    return_list = []
    index_exist = es.indices.exists(index=active_index)
    if not index_exist:
        print "no active_index exist"
        sys.exit(0)

    count_s = 0
    count_c = 0
    start = 0
    search_list = []
    while 1:
        user_list = search_k(es, active_index, active_type, start, size=100)
        start += 100
        for item in user_list:
            uid = item.get('user', '0') # obtain uid, notice "uid" or "user"
            search_list.append(uid)

        search_result = es.mget(index=portrait_index, doc_type=portrait_type, body={"ids": search_list}, _source=True)["docs"]

        for item in search_result:
            if item["found"]:
                return_list.append(user_list[search_result.index(item)])
                count_c += 1

                if count_c >= number:
                    return return_list


if __name__ == "__main__":
    print search_portrait_user_in_activity(es, 2, "20130901", "bci", "user_index_profile", "manage")
