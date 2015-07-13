# -*- coding: UTF-8 -*-
'''
the common function of searching user profile
'''
from global_utils import es_user_profile as es

# search uname by uid
def search_uid2uname(uid):
    results = es.search()
    return uname
