# -*- coding: utf-8 -*-

from flask.ext import admin
from flask import current_app
from elasticsearch import Elasticsearch as _Elasticsearch
from elasticsearch.exceptions import NotFoundError
from redis import StrictRedis as _Redis
#from flask.ext.pymongo import PyMongo
#from flask.ext.sqlalchemy import SQLAlchemy
#from flask.ext.mongoengine import MongoEngine

#__all__ = ['mongo', 'db', 'admin', 'mongo_engine']

__all__ = ['admin']

#db = SQLAlchemy()
#mongo = PyMongo()
#mongo_engine = MongoEngine()
admin = admin.Admin(name=u'系统 数据库管理')

class ElasticSearch(object):
    """
    A thin wrapper around pyelasticsearch.ElasticSearch()
    """
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('ELASTICSEARCH_URL', 'http://219.224.135.97:9208/')
        app.extensions['elasticsearch'] = _Elasticsearch(app.config['ELASTICSEARCH_URL'])

    def __getattr__(self, item):
        if 'elasticsearch' not in current_app.extensions.keys():
            raise Exception('not initialised, did you forget to call init_app?')
        return getattr(current_app.extensions['elasticsearch'], item)


# class Redis(object):

#     def __init__(self, app=None):
#         if app is not None:
#             self.init_app(app)

#     def init_app(self, app):
#         app.extensions['redis'] = _Redis.from_url(app.config['REDIS_URL'])

#     def __getattr__(self, item):
#         if 'redis' not in current_app.extensions.keys():
#             raise Exception('not initialised, did you forget to call init_app?')
#         return getattr(current_app.extensions['redis'], item)


es = ElasticSearch()
# redis = Redis()
INDEX_NAME = 'weibo_user'
DOC_TYPE = 'user'

# 自定义查询
def es_get_source(id, es=es, index=INDEX_NAME, doc_type=DOC_TYPE):
    try:
        source = es.get_source(index=index, doc_type=doc_type, id=id)
    except NotFoundError as e:
        source = {}
    except Exception as e:
        # TODO handle exception
        raise e
    return source


def es_mget_source(ids, es=es, index=INDEX_NAME, doc_type=DOC_TYPE):
    try:
        source = es.mget(index=index, doc_type=doc_type, body={'ids': ids})
    except Exception as e:
        raise e
    source = [item['_source'] for item in source['docs'] if item['found'] is True]
    return source
