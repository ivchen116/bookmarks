# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from urlparse import urlparse
from datetime import datetime

from app import app, db
from . import item
from ..models import User, Bookmark


@item.route('/add', methods=['GET', 'POST'])
@login_required
def add():
	url = request.args.get('url')
	title = request.args.get('title')
	
	if url is None:
		return jsonify({
			'status': 0
		})
	
	bookmark = current_user.bookmarks.filter_by(given_url=url).first()
	if bookmark:
		bookmark.time_updated = datetime.utcnow()
	else:
		bookmark = Bookmark(author=current_user, given_url=url, 
					given_title=title, netloc = urlparse(url).netloc)
		
	db.session.add(bookmark)
	db.session.commit()
		
	return jsonify({
		'status': 1
	})
	
@item.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
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
	
	return jsonify({
		'status': 1
	})
	
@item.route('/finish', methods=['GET', 'POST'])
@login_required
def finish():
	itemid = request.args.get('id')
	done = request.args.get('done')

	if itemid is None or done is None:
		return jsonify({
			'status': 0
		})
	
	finish = True
	if done == '0':
		finish = False
	elif done == '1':
		finish = True
	else:
		return jsonify({
			'status': 0
		})
	
	bookmark = Bookmark.query.get(itemid)
	
	if bookmark is None or current_user != bookmark.author or bookmark.disabled:
		return jsonify({
			'status': 0
		})
	
	if finish != bookmark.finish:
		bookmark.finish = finish
		db.session.add(bookmark)
		db.session.commit()
	
	return jsonify({
		'status': 1
	})
	
@item.route('/get', methods=['GET', 'POST'])
@login_required
def get():
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
	
	archived = True
	if state == 'queue':
		archived = False
	elif state == 'archive':
		archived = True
	else:
		return jsonify({
			'status': 0
		})
	
	bookmarks = current_user.bookmarks.filter_by(archived=archived).order_by(
				Bookmark.time_updated.desc()).limit(count).offset(offset)

	data = {
				'lists': [item.to_dict() for item in bookmarks],
				'status': 1
			}
	return jsonify(data)