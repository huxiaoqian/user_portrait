# -*- coding: utf-8 -*-

import sys
from elasticsearch import Elasticsearch

from user_portrait.global_utils import ES_CLUSTER_FLOW1 as es

index_destination = "copy_user_portrait" # attention
index_destination_doctype = "user"

def expand_update_action(data):
    _id = data['uid']
    action = {'update': {'_id': _id}}
    xdata = {"doc": data}
    return action, xdata

def update_record_index(uid_list):
    bulk_action = []
    for each in uid_list:
        info = {}
        info['uid'] = str(each)
        info['low_number'] = 0
        xdata = expand_update_action(info)
        bulk_action.extend([xdata[0], xdata[1]])

    es.bulk(bulk_action, index=index_destination, doc_type=index_destination_doctype, timeout=30)

if __name__ == "__main__":
    update_record_index(['1790159797', '1756422621'])
