"""The initialization for the app folder."""
from config import Config
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import (
	configure_uploads,
	patch_request_class,
	IMAGES, UploadSet
)

"""Creates an instance of Flask app and
	initializes all dependencies that I am using
"""
app = Flask(__name__)  # Creates an instance of a flask app
app.config.from_object(Config)  # Generatess config from config.py
bootstrap = Bootstrap(app)  # activates flask bootstrap
db = SQLAlchemy(app)  # initializes database
migrate = Migrate(app, db)  # initializes flask migrate
login = LoginManager(app)  # links login manager to app
login.login_view = 'login'  # setup for Login Manager
photos = UploadSet('photos', IMAGES)  # upload settings
configure_uploads(app, photos)  # more upload settings
patch_request_class(app)  # the rest of the upload settings

""" runs routes.py and generates models.py """
from app import routes, models
