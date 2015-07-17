# -*- coding: utf-8 -*-

import os
from elasticsearch import Elasticsearch
es = Elasticsearch("219.224.135.93")

file_path = "/home/ubuntu8/yuankun/blacklist/"
fan_list = set()

file_list = os.listdir(file_path)
print "total file is ", len(file_list)
for each in file_list:
    print each
    with open (os.path.join(file_path,each), "rb") as f:
        for line in f:
            item = line.strip().split(",")
            for name in item:
                fan_list.add(name)

print len(fan_list)

def search_top_k(index_name, doctype):
    query_body = {
        "query": {"match_all": {}
            },
        "sort": [{"user_index": {"order": "desc"}}],
        "size": 10000
    }

    result = es.search(index=index_name, doc_type=doctype, body=query_body)["hits"]["hits"]

    uid_set = set()
    for item in result:
        uid_set.add(item["_id"])

    return uid_set

excel_file = "/home/ubuntu8/yuankun/20150708.xls"

import xlrd

data = xlrd.open_workbook(excel_file)
table = data.sheets()[0]

col_value = table.col_values(1)
abc = set()
for item in col_value[1:]:
    abc.add(str(int(item)))
print col_value[1]
print len(col_value)

print len(abc.intersection(fan_list))
"""
top_k = search_top_k("20130902", "bci")
intersection = top_k.intersection(fan_list)
print intersection
print len(intersection)

"""
