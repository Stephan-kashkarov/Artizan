from app import app, db
from app.models import Person, Artist, Art, Playlist, Playlist_art
from app.forms import login_form, regist_form, profile_form, art_form
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, login_required, logout_user
from flask_uploads import UploadSet, IMAGES
from json import loads
from random import randint
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage


@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()


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


@app.route('/user/<username>', methods=['GET', 'POST'])
def profile(username):
	user = Person.query.filter_by(username=username).first()
	form = profile_form()
	form1 = art_form()
	showcases = Art.query.filter_by(artist_id="u" + user.id).all()
	playlist = Playlist.query.filter_by(account_id=user.id).all()
	if current_user == user:
		if form.validate_on_submit():
			if form.email.data:
				current_user.email = form.email.data
			if form.bio.data:
				current_user.bio = form.bio.data
			db.session.commit()
			flash('Your profile is updated!')
			return redirect(url_for('profile', username=current_user.username))
		if form1.validate_on_submit():
			if request.files:
				a = Art(
					title=form1.title.data,
					technique=form1.technique.data,
					location=form1.location.data,
					form=form1.form.data,
					user_id='u' + current_user.id
				)
				photos = UploadSet('photos', IMAGES)
				filename = photos.save(
					FileStorage(request.files.get('photo')),
					'useruploads',
					str(form1.title.data + str(current_user.id)) + '.jpg'
				)
				file_url = photos.url(filename)
				a.img_url = file_url
				a.date = datetime.now()
				db.session.add(a)
				db.session.commit()
				flash('img was uploaded to database')
			else:
				flash("img dosent exist")
			return redirect(url_for('profile', username=current_user.username))
		else:
			return render_template(
				'profile.html',
				user=user,
				showcases=showcases,
				playlists=playlist,
				form=form,
				form1=form1
			)
	else:
		return render_template(
			'profile.html',
			user=user,
			showcases=showcases,
			playlists=playlist,
			form=form,
			form1=form1
		)


@app.route('/browse')
def browse():
	spotlight = Artist.query.get(randint(1, db.session.query(Artist).count() - 1))
	spotlight_list = Art.query.filter_by(artist_id=spotlight.id).all()[:5]
	return render_template(
		'browse.html',
		spotlight=spotlight,
		spotlight_list=spotlight_list
	)


@app.route('/browse/artist/<id>')
def artist(id):
	return render_template('artist.html', artist=Artist.query.get(id))


@app.route('/browse/art/<id>')
def art(id):
	return render_template('art.html', art=Art.query.get(id))


@app.route('/about')
def about():
	return render_template('about.html')


@app.route('/json', methods=['POST'])
def json():
	data = request.data.decode("utf-8")
	data = loads(data)
	if data['key'] == app.config['SECRET_KEY']:
		data = data['data']
		for i in data:
			u = Artist(
				name=i['name'],
				life=i['life'],
				school=i['school'],
				timeframe=i['timeframe']
			)
			db.session.add(u)
			u = Artist.query.filter_by(name=i['name']).first()
			for j in i['art']:
				a = Art(
					title=j['title'],
					date=j['date'],
					technique=j['technique'],
					location=j['location'],
					url=j['url'],
					form=j['form'],
					type=j['painting_type'],
					img_url=j['img'],
					artist_id=u.id
				)
				db.session.add(a)
		db.session.commit()
		return "Thanks for the data"
	else:
		return "Please provide Auth"


@app.route('/jsonart', methods=['POST'])
@login_required
def jsonart():
	data = request.data.decode("utf-8")
	data = loads(data)
	if data['key'] == 'SECRET_KEY':
		data = data['data']
		for i in data['art']:
			a = Art(
				title=i['title'],
				date=i['date'],
				technique=i['technique'],
				location=i['location'],
				url=i['url'],
				form=i['form'],
				type=i['painting_type'],
				img_url=i['img'],
				artist_id=current_user.id
			)
		db.session.add(a)
		db.session.commit()
		return "Thanks for the data"
	else:
		return "Please provide Auth"
