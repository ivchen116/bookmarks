# -*- coding: utf-8 -*-
import requests
import HTMLParser
from BeautifulSoup import BeautifulSoup
from threading import Thread
from app import db

import requests_patch

def async_update_link(app, bookmark):
    with app.app_context():
		try:
			r = requests.get(bookmark.given_url, timeout=1)
			soup = BeautifulSoup(r.text)
			if soup.title is not None:
				bookmark.resolved_url = r.url
				html_parser = HTMLParser.HTMLParser()
				bookmark.resolved_title = html_parser.unescape(soup.title.text)
				db.session.add(bookmark)
				db.session.commit()
			else:
				print 'title not exist'
		except Exception,err:
			print 'load url: ' + bookmark.given_url + ' err: ' + err

def update_link(app, bookmark):
    Thread(target=async_update_link, args=(app, bookmark)).start()