from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib


@login.user_loader
def load_user(id):
	return Person.query.get(int(id))


class Person(UserMixin, db.Model):
	__tablename__ = 'person'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	bio = db.Column(db.String(250))
	joined = db.Column(db.DateTime, default=datetime.utcnow)
	last_seen = db.Column(db.DateTime, default=datetime.utcnow)
	art = db.relationship('Art', backref='account', lazy='dynamic')
	playlist = db.relationship('Playlist', backref='account', lazy='dynamic')

	def __repr__(self):
		return '<User {}>'.format(self.username)

	def set_password(self, password):
		self.password_hash = generate_password_hash(str(password))

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def avatar(self, size):
		digest = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()
		self.profile_pic = \
			'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
				digest, size
			)
		return self.profile_pic


class Art(db.Model):
	__tablename__ = 'art'

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100))
	date = db.Column(db.String(100))
	technique = db.Column(db.String(100))
	location = db.Column(db.String(100))
	url = db.Column(db.String(100))
	form = db.Column(db.String(100))
	type = db.Column(db.String(100))
	img_url = db.Column(db.String(100))
	artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
	playlists = db.relationship('Playlist_art', backref='art', lazy='dynamic')

	def __repr__(self):
		return '<{} - Art>'.format(self.title)


class Artist(db.Model):
	__tablename__ = 'artist'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True, unique=True)
	life = db.Column(db.String(100))
	school = db.Column(db.String(100))
	timeframe = db.Column(db.String(100))
	art = db.relationship('Art', backref='artist', lazy='dynamic')

	def __repr__(self):
		return '<Artist {}>'.format(self.name)


class Playlist(db.Model):
	__tablename__ = 'playlist'

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100))
	account_id = db.Column(db.Integer, db.ForeignKey('person.id'))
	arts = db.relationship('Playlist_art', backref='playlist', lazy='dynamic')


class Playlist_art(db.Model):
	__tablename__ = 'playlist_art'

	playlist_id = db.Column(
		db.Integer,
		db.ForeignKey('playlist.id'),
		primary_key=True
	)
	art_id = db.Column(
		db.Integer,
		db.ForeignKey('art.id'),
		primary_key=True
	)
