# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from urlparse import urlparse
from datetime import datetime

from app import app, db
from . import user
from .forms import BookmarkForm
from ..models import User, Bookmark, Permission
from ..util import url_resolve

@user.route('/')
@login_required
def index():
	return render_template('user/index.html', title = '在读', table='queue')

@user.route('/archive')
@login_required
def archive():
	return render_template('user/index.html', title = '已读', table='archive')
	
@user.route('/favorite')
@login_required
def favorite():
	return render_template('user/index.html', title = '精华', table = 'favorite')
	
@user.route('/tags')
@login_required
def tags():
	return render_template('user/index.html', title = '标签', table='tags')



