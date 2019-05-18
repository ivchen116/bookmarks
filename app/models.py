# -*- coding: utf-8 -*-
from datetime import datetime
import time

from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login

class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	bookmarks = db.relationship('Bookmark', backref='author', lazy='dynamic')

	def __init__(self, **kwargs):
		super(User, self).__init__(**kwargs)
		if self.role is None:
			if self.email == app.config['ADMINMAIL']:
				self.role = Role.query.filter_by(permissions=0xff).first()
			if self.role is None:
				self.role = Role.query.filter_by(default=True).first()

	def operation(self, permissions):
		return self.role is not None and \
			(self.role.permissions & permissions) == permissions

	def is_administrator(self):
		return self.operation(Permission.ADMINISTER)
    
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)
	
	def __repr__(self):
		return '<User {}>'.format(self.username)    

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    users = db.relationship('User', backref = 'role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % (self.name)

class AnonymousUser(AnonymousUserMixin):
    def operation(self, permissions):
        return False

    def is_administrator(self):
        return False

login.anonymous_user = AnonymousUser

		
class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80
	

class Bookmark(db.Model):
	__tablename__ = 'bookmarks'
	id = db.Column(db.Integer, primary_key=True)
	given_url = db.Column(db.String(256), index=True)
	netloc = db.Column(db.String(128))
	given_title = db.Column(db.String(256))
	disabled = db.Column(db.Boolean, default=False)
	archived = db.Column(db.Boolean, default=False)
	
	image_url = db.Column(db.String(256))
	resolved_url = db.Column(db.String(256), index=True)
	resolved_title = db.Column(db.String(256))
	
	time_added = db.Column(db.DateTime, default=datetime.utcnow)
	time_updated = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	
	def to_dict(self):
		data = {
			'id': self.id,
			'url': self.link.url,
			'title': self.title,
			'netloc': self.netloc,
			'resolved_url': self.resolved_url,
			'resolved_title': self.resolved_title,
			'image_url': self.image_url,
			'time_added': int(time.mktime(self.time_added.timetuple())),
			'time_updated': int(time.mktime(self.time_updated.timetuple())),
			'archived': self.archived
		}

		return data
	
	def __repr__(self):
		return '<Bookmark {}>'.format(self.id)
		
		