from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login


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
	artist = db.relationship('Artist', backref='account', lazy='dynamic')

	def __repr__(self):
		return '<User {}>'.format(self.username)

	def set_password(self, password):
		self.password_hash = generate_password_hash(str(password))

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)


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

	def __repr__(self):
		return '<{} - Art>'.format(self.title)


class Artist(db.Model):
	__tablename__ = 'artist'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True, unique=True)
	life = db.Column(db.String(100))
	school = db.Column(db.String(100))
	timeframe = db.Column(db.String(100))
	account_id = db.Column(db.Integer, db.ForeignKey('person.id'))
	art = db.relationship('Art', backref='artist', lazy='dynamic')

	def __repr__(self):
		return '<Artist {}>'.format(self.name)
