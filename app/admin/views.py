# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from . import admin
from ..decorators import admin_required
from ..models import User, Bookmark


@admin.route('/')
@login_required
@admin_required
def index():
    return render_template('admin/admin.html', title='Admin Panel')
	
	
@admin.route('/bookmarks')
@login_required
@admin_required
def bookmarks():
	page = request.args.get('page', 1, type=int)
	pagination = Bookmark.query.order_by(Bookmark.timestamp.desc()).paginate(
		page, per_page=app.config['POSTS_PER_PAGE'],
		error_out=False
	)
    # posts = pagination.items
	bookmarks = [bookmark for bookmark in pagination.items]
	return render_template('admin/admin_bookmarks.html',
							title = 'Bookmarks Manage',
							bookmarks=bookmarks,
							pagination=pagination)
	
@admin.route('/users')	
@login_required
@admin_required
def users():
	users = User.query.order_by(User.id.desc()).all()
	return render_template('admin/admin_users.html', title='User List', users=users)
	
@admin.route('/delete_bookmark/<int:id>')
@login_required
@admin_required
def delete_bookmark(id):
	bookmark = Bookmark.query.get_or_404(id)
	bookmark.disabled = True
	db.session.add(bookmark)
	db.session.commit()
	return redirect(url_for('admin.bookmarks'))
	
@admin.route('/recover_bookmark/<int:id>')
@login_required
@admin_required
def recover_bookmark(id):
	bookmark = Bookmark.query.get_or_404(id)
	bookmark.disabled = False
	db.session.add(bookmark)
	db.session.commit()
	return redirect(url_for('admin.bookmarks'))
	