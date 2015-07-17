# -*- coding = utf-8 -*-

import math
import datetime
import time
import sys
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
reload(sys)
sys.path.append('./../../')
from global_utils import ES_CLUSTER_FLOW1


es = ES_CLUSTER_FLOW1
index_name = "vary"
doctype = "bci"

def generate_date(former_date, later_date="21000101"):
    date_list = []
    date_list.append(former_date)
    former_struct = datetime.date(int(former_date[0:4]), int(former_date[4:6]), int(former_date[6:]))
    later_struct = datetime.date(int(later_date[0:4]), int(later_date[4:6]), int(later_date[6:]))
    former_timestamp = time.mktime(former_struct.timetuple())
    later_timestamp = time.mktime(later_struct.timetuple())
    i=0

    next_timestamp = former_timestamp
    while 1:
        next_timestamp += 86400
        if next_timestamp <= later_timestamp:
            date_list.append(time.strftime('%Y%m%d',time.localtime(next_timestamp)))
            i += 1
            if i == 7:
                break
        else:
            break

    return date_list


def search_history_index(uid, index_name, doctype, start_date, end_date):
    # date.formate: 20130901
    date_list = generate_date(start_date, end_date)
    try:
        result = es.get(index=index_name, doc_type=doctype, id=uid, _source=True)['_source']
    except NotFoundError:
        return NotFound
    return result

if __name__ == "__main__":
    print search_history_index('1990921871', index_name, doctype, '20130901', '20130904')
