import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key'
	UPLOADED_PHOTOS_DEST = os.path.realpath('.') + '/static/imgs/art/uploads'
	UPLOADED_PHOTOS_ALLOW = ('.jpg', '.svg', '.png')

	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') \
		or 'sqlite:///' + os.path.join(basedir, 'dev.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
