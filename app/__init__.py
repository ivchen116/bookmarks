# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from logging.handlers import RotatingFileHandler
from flask_moment import Moment

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
moment = Moment(app)
login = LoginManager(app)
login.login_view = 'auth.login'

from .user import user as user_blueprint
from .auth import auth as auth_blueprint
from .admin import admin as admin_blueprint
app.register_blueprint(user_blueprint)
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(admin_blueprint, url_prefix='/admin')

