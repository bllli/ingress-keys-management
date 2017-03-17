# -*- coding: utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap, WebCDN, ConditionalCDN
import logging

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
csrf = CSRFProtect()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def log(user, message):
    logger = logging.getLogger("werkzeug")
    logger.warning('%s | %s | %s' % (user.username, user.role.name, message))

JQUERY_VERSION = '2.0.3'
HTML5SHIV_VERSION = '3.7'
RESPONDJS_VERSION = '1.3.0'
BOOTSTRAP_VERSION = '3.0.3'


def change_cdn_domestic(tar_app):
    static = tar_app.extensions['bootstrap']['cdns']['static']
    local = tar_app.extensions['bootstrap']['cdns']['local']

    def change_one(tar_lib, tar_ver, fallback):
        tar_js = ConditionalCDN('BOOTSTRAP_SERVE_LOCAL', fallback,
                                WebCDN('//cdn.bootcss.com/' + tar_lib + '/' + tar_ver + '/'))
        tar_app.extensions['bootstrap']['cdns'][tar_lib] = tar_js

    libs = {'jquery': {'ver': JQUERY_VERSION, 'fallback': local},
            'bootstrap': {'ver': BOOTSTRAP_VERSION, 'fallback': local},
            'html5shiv': {'ver': HTML5SHIV_VERSION, 'fallback': static},
            'respond.js': {'ver': RESPONDJS_VERSION, 'fallback': static}}
    for lib, par in libs.items():
        change_one(lib, par['ver'], par['fallback'])

# flask-bootstrap国内化 感谢http://blog.sina.com.cn/s/blog_626968300102wkbm.html


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    change_cdn_domestic(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .portal import portal as portal_blueprint
    app.register_blueprint(portal_blueprint, url_prefix='/portal')

    from .wechat import keybot as wechat_blueprint
    app.register_blueprint(wechat_blueprint, url_prefix='/wechat')

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    return app
