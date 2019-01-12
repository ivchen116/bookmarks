# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from . import user
from .forms import BookmarkForm
from ..models import User, Bookmark, Permission


@user.route('/')
@user.route('/index')
def index():
	page = request.args.get('page', 1, type=int)
	pagination = Bookmark.query.filter_by(disabled=False).order_by(Bookmark.timestamp.desc()).paginate(
		page, per_page=app.config['POSTS_PER_PAGE'],
		error_out=False
	)
    # bookmarks = pagination.items
	bookmarks = [bookmark for bookmark in pagination.items if bookmark.disabled==False]
	return render_template('user/index.html',
							title = '首页',
							bookmarks=bookmarks,
							pagination=pagination)
	
@user.route('/user/<username>')
@login_required
def users(username):
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username=username).first_or_404()
	pagination = user.bookmarks.order_by(Bookmark.timestamp.desc()).paginate(
		page, per_page=app.config['POSTS_PER_PAGE'],
		error_out=False
	)
	bookmarks = pagination.items
	return render_template('user/user.html', title="用户中心", user=user, bookmarks=bookmarks, pagination=pagination)

@user.route('/write', methods=['GET','POST'])
@login_required
def write():
	form = BookmarkForm()
	if form.validate_on_submit():
		bookmark = Bookmark(title=form.title.data, href=form.href.data, author=current_user)
		db.session.add(bookmark)
		db.session.commit()
		flash('Your post is now live!')
		return redirect(url_for('user.index'))
	return render_template("user/write.html", title='发布', form=form)

@user.route('/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit(id):
	bookmark = Bookmark.query.get_or_404(id)
	if current_user != bookmark.author and \
		not current_user.operation(Permission.ADMINISTER):
		abort(403)
	form = BookmarkForm()
	if form.validate_on_submit():
		bookmark.title = form.title.data
		bookmark.href = form.href.data
		db.session.add(bookmark)
		db.session.commit()
		flash('Update sucess')
		return redirect(url_for('user.edit', id=id))
	form.title.data = bookmark.title
	form.href.data = bookmark.href
	return render_template('user/edit.html',
                           form=form,
                           bookmark=bookmark,
                           title='编辑')

