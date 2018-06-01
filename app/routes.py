from app import app, db
from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, login_required, logout_user
from app.models import Person
from app.forms import login_form, regist_form, profile_form


@app.route("/")
def welcome():
	if current_user.is_anonymous:
		return render_template('index.html')
	else:
		return redirect(url_for('browse'))


@app.route('/login', methods=["POST", "GET"])
def login():
	form = login_form()
	if form.validate_on_submit():
		person = Person.query.filter_by(username=form.username.data).first()
		if person and person.check_password(form.password.data):
			login_user(person, remember=form.remember_me.data)
			return redirect(url_for('browse'))
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


@app.route('/user/<username>')
def profile(username):
	user = Person.query.filter_by(username=username).first()
	return render_template('profile.html', user=user)


@app.route('/user/<username>/edit')
@login_required
def edit_profile(username):
	user = Person.query.filter_by(usernmae=username).first()
	form = profile_form()
	if current_user != user:
		flash("you cannot edit other users profiles")
		return redirect(url_for('browse'))
	else:
		if form.validate_on_submit():
			current_user.email = form.email.data
			current_user.bio = form.bio.data
			db.session.add(current_user)
			db.session.commit()
			return redirect(url_for('profile', username=current_user.username))
		return render_template('edit_profile.html', user=current_user, form=form)


@app.route('/browse')
def browse():
	return render_template('browse.html')


@app.route('/about')
def about():
	return render_template('about.html')
