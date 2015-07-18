# -*- coding: utf-8 -*-

import math
import sys
from user_portrait.dogapi_utils import resp2item_search
from user_portrait.global_utils import get_client

def index_mid(mid):
    client = get_client()

    source_weibo = client.get('/showBatch', ids=mid)['statuses'][0]
    items = resp2item_search(source_weibo, 8)

    return items
