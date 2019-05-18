# -*- coding: utf-8 -*-
import requests
from BeautifulSoup import BeautifulSoup
from threading import Thread
from app import db

def async_update_link(app, bookmark):
    with app.app_context():
		try:
			r = requests.get(bookmark.given_url, timeout=1)
			r.encoding = 'utf-8'
			soup = BeautifulSoup(r.text)
			if soup.title is not None:
				bookmark.resolved_url = r.url
				bookmark.resolved_title = soup.title.text
				db.session.add(bookmark)
				db.session.commit()
				print 'title ' + soup.title.text
			else:
				print 'title not exist'
		except Exception,err:
			print 'load url: ' + bookmark.given_url + ' err: ' + err

def update_link(app, bookmark):
    Thread(target=async_update_link, args=(app, bookmark)).start()