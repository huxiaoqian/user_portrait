# -*- coding: utf-8 -*-

class DevConfig:

    DEBUG = True
    SECRET_KEY = '2too3gle8leotao'
    STATIC_FOLDER = 'static'
    REDIS_URL = 'redis://localhost:6379/8'


class ProdConfig(DevConfig):

    DEBUG = False
    ELASTICSEARCH_URL = 'http://219.224.135.97:9200'
    REDIS_URL = 'redis://219.224.135.97:6379/8'
