# -*- coding: utf-8 -*-

from flask.ext import admin
#from flask.ext.pymongo import PyMongo
#from flask.ext.sqlalchemy import SQLAlchemy
#from flask.ext.mongoengine import MongoEngine

#__all__ = ['mongo', 'db', 'admin', 'mongo_engine']

__all__ = ['admin']

#db = SQLAlchemy()
#mongo = PyMongo()
#mongo_engine = MongoEngine()
admin = admin.Admin(name=u'系统 数据库管理')

