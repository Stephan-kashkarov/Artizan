from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import Person


class login_form(FlaskForm):
	username = StringField('Username:', validators=[DataRequired()])
	password = PasswordField('Password:', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')


class regist_form(FlaskForm):
	username = StringField('Choose a Username:', validators=[DataRequired()])
	email = StringField('Enter an Email:', validators=[DataRequired(), Email()])
	pass1 = PasswordField('Password:', validators=[DataRequired()])
	pass2 = PasswordField('Re-type Password:', validators=[
		DataRequired(), EqualTo('pass1')
	])

	def validate_username(self, username):
		user = Person.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Username already taken')

	def validate_email(self, email):
		user = Person.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Email already taken')


class profile_form(FlaskForm):
	password = PasswordField('Password:', validators=[DataRequired()])
	email = StringField('Change email:')
	bio = StringField('Edit Bio:')


class art_form(FlaskForm):
	title = StringField('Choose a Title:', validators=[DataRequired()])
	date = StringField('Choose a date', validators=[DataRequired()])
	technique = StringField('Choose a technique:', validators=[DataRequired()])
	location = StringField('Choose a location:', validators=[DataRequired()])
	form = StringField('Choose a form:', validators=[DataRequired()])
	type = StringField('Choose a type:', validators=[DataRequired()])
