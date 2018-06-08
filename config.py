"""Configuration for flask app."""
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
	"""Object containing all of the config data for the app"""
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key'
	UPLOADED_PHOTOS_DEST = os.path.realpath('.') + '/app/static/imgs/art/uploads'
	UPLOADED_PHOTOS_ALLOW = ('.jpg')

	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') \
		or 'sqlite:///' + os.path.join(basedir, 'dev.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
