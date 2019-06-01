# -*- coding: utf-8 -*-
import requests
import HTMLParser
from BeautifulSoup import BeautifulSoup
from threading import Thread
from app import db

import requests_patch

def get_title(text):
	soup = BeautifulSoup(text)
	if soup.title and soup.title.text != '':
		return soup.title.text
	
	if (soup.h1 and soup.h1.text != ''):
		return soup.h1.text
		
	if (soup.h2 and soup.h2.text != ''):
		return soup.h2.text
		
	return None

def async_update_link(app, bookmark):
    with app.app_context():
		try:
			headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
			}
			r = requests.get(bookmark.given_url, headers=headers, timeout=3)
			title = get_title(r.text)
			if title is not None:
				if len(title) > 128:
					title = title[:124]
				bookmark.resolved_url = r.url
				html_parser = HTMLParser.HTMLParser()
				bookmark.resolved_title = html_parser.unescape(title)
				db.session.merge(bookmark)
				db.session.commit()
			else:
				print 'title not exist'
		except Exception,err:
			print 'load url: ' + bookmark.given_url + ' err: ' + err

def update_link(app, bookmark):
    Thread(target=async_update_link, args=(app, bookmark)).start()
