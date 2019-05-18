# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from urlparse import urlparse
from datetime import datetime

from app import app, db
from . import item
from ..models import User, Bookmark, Link


@item.route('/add', methods=['GET', 'POST'])
@login_required
def add():
	url = request.args.get('url')
	title = request.args.get('title')
	
	if url is None:
		return jsonify({
			'status': 0
		})
	
	newlink = False
	link = Link.query.filter_by(url=url).first()
	if link is None:
		link = Link(url=url, netloc = urlparse(url).netloc)
		db.session.add(link)
		newlink = True
	
	#bookmark
	if newlink is False:
		bookmark = Bookmark.query.filter_by(link_id=link.id).first() #重复只更新时间
		if bookmark is None:
			bookmark = Bookmark(author=current_user, link=link)
		else :
			bookmark.timestamp = datetime.utcnow()
	else :
		bookmark = Bookmark(author=current_user, link=link)
		
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
	
	finish = True
	if state == 'queue':
		finish = False
	elif state == 'archive':
		finish = True
	else:
		return jsonify({
			'status': 0
		})
	
	bookmarks = current_user.bookmarks.filter_by(finish=finish).order_by(
				Bookmark.timestamp.desc()).limit(count).offset(offset)

	data = {
				'lists': [item.to_dict() for item in bookmarks],
				'status': 1
			}
	return jsonify(data)