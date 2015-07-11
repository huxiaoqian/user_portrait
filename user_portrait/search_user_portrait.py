# -*- coding: UTF-8 -*-
'''
the common function of searching user portrait
'''
from elasticsearch.exceptions import NotFoundError
from global_utils import es_user_portrait as es


INDEX_NAME = 'user_portrait'
DOC_TYPE = 'user'

# 自定义查询
def search_portrait_by_id(id):
    try:
        source = es.get_source(index=INDEX_NAME, doc_type=DOC_TYPE, id=id)
    except NotFoundError as e:
        source = {}
    except Exception as e:
        # TODO handle exception
        raise e
    return source


if __name__ == '__main__':
    uid = '1770831781'
    search_portrait_by_id(uid)
