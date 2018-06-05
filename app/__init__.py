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

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

from app import routes, models
