# -*- coding: utf-8 -*-

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from extensions import admin
#from global_config import MYSQL_HOST, MYSQL_USER, MYSQL_DB, MONGODB_HOST, MONGODB_PORT, MASTER_TIMELINE_54API_WEIBO_DB
#from case.index.views import mod as indexModule
from user_portrait.index.views import mod as indexModule
from user_portrait.attribute.views import mod as attributeModule


def create_app():
    app = Flask(__name__)

    # Create modules
    app.register_blueprint(indexModule)

    # the debug toolbar is only enabled in debug mode
    app.config['DEBUG'] = True

    app.config['ADMINS'] = frozenset(['youremail@yourdomain.com'])
    app.config['SECRET_KEY'] = 'SecretKeyForSessionSigning'
    
    '''
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://%s:@%s/%s?charset=utf8' % (MYSQL_USER, MYSQL_HOST, MYSQL_DB)
    app.config['SQLALCHEMY_ECHO'] = False
    '''
    app.config['DATABASE_CONNECT_OPTIONS'] = {}

    app.config['THREADS_PER_PAGE'] = 8

    app.config['CSRF_ENABLED'] = True
    app.config['CSRF_SESSION_KEY'] = 'somethingimpossibletoguess'

    # Enable the toolbar?
    app.config['DEBUG_TB_ENABLED'] = app.debug
    # Should intercept redirects?
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
    # Enable the profiler on all requests, default to false
    app.config['DEBUG_TB_PROFILER_ENABLED'] = True
    # Enable the template editor, default to false
    app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True
    # debug toolbar
    # toolbar = DebugToolbarExtension(app)
    
    '''
    app.config['MONGO_HOST'] = MONGODB_HOST
    app.config['MONGO_PORT'] = MONGODB_PORT

    app.config['MONGODB_SETTINGS'] = {
        'db': MASTER_TIMELINE_54API_WEIBO_DB,
        'host': MONGODB_HOST,
        'port': MONGODB_PORT
    }

    # Create mysql database
    db.init_app(app)
    with app.test_request_context():
        db.create_all()

    # Create mongo_engine
    mongo_engine.init_app(app)

    admin.init_app(app)
    """
    # Create mysql database admin, visit via url: http://HOST:PORT/admin/
    for m in model.__all__:
        m = getattr(model, m)
        n = m._name()
        admin.add_view(SQLModelView(m, db.session, name=n))

    for m in mongodb_model.__all__:
        admin.add_view(MongoDBView(m))
    """

    # init mongo
    mongo.init_app(app)
    '''
    return app
   
