# -*- coding: utf-8 -*-
import requests
from BeautifulSoup import BeautifulSoup
from threading import Thread
from ..models import Link
from app import db

def get_async_link(app, url):
    with app.app_context():
		try:
			link = Link.query.filter_by(url=url).first()
			if link is None or link.title is not None:
				print 'not need read url..'
				return
			r = requests.get(url, timeout=1)
			r.encoding = 'utf-8'
			soup = BeautifulSoup(r.text)
			if soup.title is not None:
				link.title = soup.title.text
				db.session.add(link)
				db.session.commit()
		except Exception,err:
			print 'load url: ' + link.url + ' err: ' + err

def get_link(app, url):
    Thread(target=get_async_link, args=(app, url)).start()