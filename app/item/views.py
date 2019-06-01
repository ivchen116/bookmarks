# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from urlparse import urlparse
from datetime import datetime

from app import app, db
from . import item
from ..models import User, Bookmark
from ..util import url_resolve

@item.route('/add', methods=['GET', 'POST'])
@login_required
def add():
	if request.method == 'POST':
		url = request.form.get('url')
		title = request.form.get('name')
	else:
		url = request.args.get('url')
		title = request.args.get('title')
	
	if url is None:
		return jsonify({
			'status': 0
		})
	up = urlparse(url)
	if up.scheme not in ['http', 'https'] or up.netloc is None:
		return jsonify({
			'status': 0
		})
	
	bookmark = current_user.bookmarks.filter_by(given_url=url).first()
	if bookmark:
		bookmark.time_updated = datetime.utcnow()
		bookmark.archived = False
		bookmark.disabled = False
	else:
		bookmark = Bookmark(author=current_user, given_url=url, 
					given_title = title, netloc = up.netloc)
	
	db.session.add(bookmark)
	db.session.commit()
	
	url_resolve.update_link(app, bookmark)
		
	return jsonify({
		'status': 1
	})
	
@item.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
	if request.method == 'POST':
		itemid = request.form.get('id')
	else:
		itemid = request.args.get('id')
		url = request.args.get('url')
	
	if itemid is None or not itemid.isdigit():
		return jsonify({
			'status': 0
		})
	
	bookmark = Bookmark.query.get(itemid)
	
	if bookmark is None or current_user != bookmark.author or bookmark.disabled:
		return jsonify({
			'status': 0
		})
	
	bookmark.disabled = True
	db.session.add(bookmark)
	db.session.commit()
	
	#resolve title/url
	url_resolve.update_link(app, bookmark)
	
	return jsonify({
		'status': 1
	})
	
@item.route('/archive', methods=['GET', 'POST'])
@login_required
def archive():
	if request.method == 'POST':
		itemid = request.form.get('id')
		done = request.form.get('done')
	else:
		itemid = request.args.get('id')
		done = request.args.get('done')

	if itemid is None or done is None:
		return jsonify({
			'status': 0
		})
	
	archive = True
	if done == '0':
		archive = False
	elif done == '1':
		archive = True
	else:
		return jsonify({
			'status': 0
		})
	
	bookmark = Bookmark.query.get(itemid)
	
	if bookmark is None or current_user != bookmark.author or bookmark.disabled:
		return jsonify({
			'status': 0
		})
	
	if archive != bookmark.archived:
		bookmark.archived = archive
		db.session.add(bookmark)
		db.session.commit()
	
	return jsonify({
		'status': 1
	})
	
@item.route('/favorite', methods=['GET', 'POST'])
@login_required
def favorite():
	if request.method == 'POST':
		itemid = request.form.get('id')
		mark = request.form.get('favorite')
	else:
		itemid = request.args.get('id')
		mark = request.args.get('favorite')

	if itemid is None or mark is None:
		return jsonify({
			'status': 0
		})
	
	favorite = True
	if mark == '0':
		favorite = False
	elif mark == '1':
		favorite = True
	else:
		return jsonify({
			'status': 0
		})
	
	bookmark = Bookmark.query.get(itemid)
	
	if bookmark is None or current_user != bookmark.author or bookmark.disabled:
		return jsonify({
			'status': 0
		})
	
	if favorite != bookmark.favorite:
		bookmark.favorite = favorite
		db.session.add(bookmark)
		db.session.commit()
	
	return jsonify({
		'status': 1
	})
	
@item.route('/get', methods=['GET', 'POST'])
@login_required
def get():
	if request.method == 'POST':
		offset = request.form.get('offset')
		count = request.form.get('count')
		state = request.form.get('state')
	else:
		offset = request.args.get('offset')
		count = request.args.get('count')
		state = request.args.get('state')
	
	if offset is None or not offset.isdigit():
		return jsonify({
			'status': 0
		})
		
	if count is None or not count.isdigit():
		return jsonify({
			'status': 0
		})
	
	param = []
	param.append(Bookmark.disabled == False)

	if state == 'queue':
		param.append(Bookmark.archived == False)
	elif state == 'archive':
		param.append(Bookmark.archived == True)
	elif state == 'favorite':
		param.append(Bookmark.favorite == True)
	else:
		return jsonify({
			'status': 0
		})
	
	bookmarks = current_user.bookmarks.filter(*param).order_by(
				Bookmark.time_updated.desc()).limit(count).offset(offset)

	data = {
				'lists': [item.to_dict() for item in bookmarks],
				'status': 1
			}
	return jsonify(data)