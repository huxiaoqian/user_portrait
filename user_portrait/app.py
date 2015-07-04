# -*- coding: utf-8 -*-

from flask import Flask
from werkzeug.utils import import_string

from user_portrait._settings import DevConfig
from user_portrait.extensions import es, redis
from user_portrait.jinja import gender, tsfmt

bps = [
    'user_portrait.profile.home:bp',
    'user_portrait.profile.search:bp',
    'user_portrait.profile.user:bp',
]


def create_app(config=DevConfig):
    app = Flask(__name__, static_folder=config.STATIC_FOLDER)
    app.config.from_object(config)
    register_blueprints(app)
    register_extensions(app)
    register_jinja_funcs(app)
    return app


def register_blueprints(app):
    for bp in bps:
        app.register_blueprint(import_string(bp))


def register_extensions(app):
    es.init_app(app)
    redis.init_app(app)


def register_jinja_funcs(app):
    funcs = dict(gender=gender,
                 tsfmt=tsfmt)
    app.jinja_env.globals.update(funcs)
