"""Definition of the internals of the database."""
from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib


@login.user_loader
def load_user(id):
	"""User loader for flask login."""
	return Person.query.get(int(id))


class Person(UserMixin, db.Model):
	"""User table - renamed to Person to avoid sql injection attacks."""

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
		"""Tells the class how to reperesnt itself."""
		return '<User {}>'.format(self.username)

	def set_password(self, password):
		"""Runs the passwords through a hash and appends."""
		self.password_hash = generate_password_hash(str(password))

	def check_password(self, password):
		"""Checks a password against the hash."""
		return check_password_hash(self.password_hash, password)

	def avatar(self, size):
		"""Returns avatar of user."""
		digest = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()
		self.profile_pic = \
			'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
				digest, size
			)
		return self.profile_pic


class Art(db.Model):
	"""Art table - Contains an artwork."""

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
	user_id = db.Column(db.Integer, db.ForeignKey('person.id'))
	playlists = db.relationship('Playlist_art', backref='art', lazy='dynamic')

	def __repr__(self):
		"""Tells the class how to reperesnt itself."""
		return '<{} - Art>'.format(self.title)


class Artist(db.Model):
	"""Artist table - Contains an artist."""

	__tablename__ = 'artist'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True, unique=True)
	life = db.Column(db.String(100))
	school = db.Column(db.String(100))
	timeframe = db.Column(db.String(100))
	art = db.relationship('Art', backref='artist', lazy='dynamic')

	def __repr__(self):
		"""Tells the class how to reperesnt itself."""
		return '<Artist {}>'.format(self.name)


class Playlist(db.Model):
	"""Playlist table - containst a playlist."""

	__tablename__ = 'playlist'

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100))
	desc = db.Column(db.String(100))
	account_id = db.Column(db.Integer, db.ForeignKey('person.id'))
	arts = db.relationship('Playlist_art', backref='playlist', lazy='dynamic')


class Playlist_art(db.Model):
	"""Link table between playlist and art."""

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
