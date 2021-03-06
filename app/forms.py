"""Container of all flask forms in app"""
from flask_wtf import FlaskForm
from flask_uploads import UploadSet, IMAGES
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import (
	StringField,
	PasswordField,
	BooleanField,
	DateField,
	SubmitField
)
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import Person


class login_form(FlaskForm):
	"""The Login form for the website"""
	username = StringField('Username:', validators=[DataRequired()])
	password = PasswordField('Password:', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')


class regist_form(FlaskForm):
	"""The register form for the website"""
	username = StringField('Choose a Username:', validators=[DataRequired()])
	email = StringField('Enter an Email:', validators=[DataRequired(), Email()])
	pass1 = PasswordField('Password:', validators=[DataRequired()])
	pass2 = PasswordField('Re-type Password:', validators=[
		DataRequired(), EqualTo('pass1')
	])

	def validate_username(self, username):
		"""Validation for username"""
		user = Person.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Username already taken')

	def validate_email(self, email):
		"""Validation for email"""
		user = Person.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Email already taken')

	def validate_password(self, password):
		"""Validation for password"""
		if len(password) < 8:
			raise ValidationError('Password too short')


class profile_form(FlaskForm):
	"""Form for changing profile attributes"""
	password = PasswordField('Password:', validators=[DataRequired()])
	email = StringField('Change email:')
	bio = StringField('Edit Bio:')

# setup for uploads
photos = UploadSet('photos', IMAGES)


class art_form(FlaskForm):
	"""The Art submission form for the website"""
	title = StringField('Choose a Title:', validators=[DataRequired()])
	technique = StringField('Choose a technique:', validators=[DataRequired()])
	location = StringField('Choose a location:', validators=[DataRequired()])
	form = StringField('Choose a form:', validators=[DataRequired()])
	type = StringField('Choose a type:', validators=[DataRequired()])
	photo = FileField(validators=[
		FileAllowed(photos, u'Image only!'),
		FileRequired(u'File was empty!')
	])
