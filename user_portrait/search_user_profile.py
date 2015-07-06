# -*- coding: UTF-8 -*-
'''
the common function of searching user profile
'''
from global_utils import es_user_profile as es

# search uname by uid
def search_uid2uname(uid):
    results = es.search()
    return uname


# 自定义查询
def es_get_source(id, es, index, doc_type):
    try:
        source = es.get_source(index=index, doc_type=doc_type, id=id)
    except NotFoundError as e:
        source = {}
    except Exception as e:
        # TODO handle exception
        raise e
    return source


def es_mget_source(ids, es, index, doc_type):
    try:
        source = es.mget(index=index, doc_type=doc_type, body={'ids': ids})
    except Exception as e:
        raise e
    source = [item['_source'] for item in source['docs'] if item['found'] is True]
    return source
