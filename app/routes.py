from app import app
from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, login_required, logout_user
from app.models import Person
from app.forms import login_form, regist_form


@app.route("/")
def welcome():
	return render_template('index.html')


@app.route('/login', methods=["POST", "GET"])
def login():
	form = login_form()
	if form.validate_on_submit():
		person = Person.query.filter_by(username=form.username.data)
		if person and person.check_password(form.password.data):
			login_user(person, remember=form.remember_me.data)
			return redirect(url_for('home'))
		else:
			flash("invalid username or password")
			return redirect(url_for('login'))

	return render_template('login.html', form=form)


@app.route('/register', methods=["POST", "GET"])
def register():
	form = regist_form()
	if form.validate_on_submit():
		user = Person(username=form.username.data, email=form.email.data)
		user.set_password(form.pass2.data)
		db.session.add(user)
		db.session.commit()
		flash('You are now a regestered user')
		return redirect(url_for('login'))
	return render_template('regester.html', form=form)


@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('welcome'))


@app.route('/home')
def home():
	return "home"


@app.route('/browse')
@login_required
def browse():
	return "browse"


@app.route('/about')
def about():
	return "about"
