from flask_wtf import FlaskForm
from wtfroms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import Person

class login_form(FlaskForm):
	username = StringField('Username:', validators=[DataRequired()])
	password = PasswordField('Password:', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me:')
	submit = SubmitField('Sign In')


class regist_form(FlaskForm):
	username = StringField('Choose a Username:', validators=[DataRequired()])
	email = StrindField('Enter an Email:', validators=[DataRequired(), Email()])
	pass1 = PasswordField('Password:', validators=[DataRequired()])
	pass2 = PasswordField('Re-type Password:', validators=[DataRequired(), EqualTo('pass1')])
	submit = SubmitField('Register!')

	def validate_username(self, username):
		user = Person.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Username already taken')

	def validate_email(self, email):
		user = Person.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Email already taken')
