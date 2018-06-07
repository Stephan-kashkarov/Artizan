from app import app, db, login
from app.models import Person, Artist, Art, Playlist, Playlist_art
from app.forms import (
	login_form,
	regist_form,
	profile_form,
	art_form,
	playlist_form
)
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, login_required, logout_user
from flask_uploads import UploadSet, IMAGES
from json import loads
from random import randint
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage


# user loader
@login.user_loader
def load_user(id):
	return Person.query.get(int(id))


# last seen tracker
@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()


# home route
@app.route("/")
def welcome():
	if current_user.is_anonymous:
		return render_template('index.html')
	else:
		return redirect(url_for('profile', username=current_user.username))


# Login route
@app.route('/login', methods=["POST", "GET"])
def login():
	form = login_form()
	if form.validate_on_submit():
		person = Person.query.filter_by(username=form.username.data).first_or_404()
		if person and person.check_password(form.password.data):
			login_user(person, remember=form.remember_me.data)
			return redirect(url_for('browse'))
		else:
			flash("invalid username or password")
			return redirect(url_for('login'))

	return render_template('login.html', form=form)


# regester route
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
	user = Person.query.filter_by(username=username).first_or_404()
	if not user:
		return '404'
	form = profile_form()
	form2 = playlist_form()
	form1 = art_form()
	showcases = Art.query.filter_by(user_id=user.id).all()
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
	return render_template(
		'profile.html',
		user=user,
		showcases=showcases,
		playlists=playlist,
		form=form,
		form1=form1,
		form2=form2
	)


@app.route('/Make_showcase', methods=["POST"])
def Make_showcase():
	form1 = art_form()
	if request.files:
		a = Art(
			title=form1.title.data,
			technique=form1.technique.data,
			location=form1.location.data,
			form=form1.form.data,
			user_id=current_user.id
		)
		photos = UploadSet('photos', IMAGES)
		filename = photos.save(
			FileStorage(request.files.get('photo')),
			'useruploads',
			str(form1.title.data + str(current_user.id)) + '.jpg'
		)
		a.img_url = 'imgs/art/uploads/' + filename
		print(a.img_url)
		a.date = datetime.now()
		db.session.add(a)
		db.session.commit()
		flash('img was uploaded to database')
	else:
		flash("img dosent exist")
	return redirect(url_for('profile', username=current_user.username))


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
	artist = Artist.query.get(id)
	showcases = Art.query.filter_by(artist_id=artist.id).all()
	return render_template(
		'artist.html',
		artist=artist,
		showcases=showcases
	)


@app.route('/browse/art/<id>')
def art(id):
	if current_user.is_authenticated:
		playlists = Playlist.query.filter_by(account_id=current_user.id).all()
	else:
		playlists = None
	return render_template(
		'art.html',
		artwork=Art.query.get(id),
		playlists=playlists
	)


@app.route('/browse/playlist/<id>')
def playlist(id):
	playlist = Playlist.query.get(id)
	track_ids = Playlist_art.query.filter_by(playlist_id=playlist.id).all()
	print(track_ids)
	tracks = []
	for i in track_ids:
		tracks.append(
			Art.query.filter_by(id=i.art_id).first()
		)
	print(tracks)
	return render_template(
		'playlist.html',
		playlist=playlist,
		tracks=tracks
	)


@app.route('/search/<term>')
def search(term):
	users = db.session.query(Person).filter(
		Person.username.like("%" + str(term) + "%")
	).order_by(Person.username.asc()).all()
	arts = db.session.query(Art).filter(
		Art.title.like("%" + str(term) + "%")
	).order_by(Art.title.asc()).all()
	artists = db.session.query(Artist).filter(
		Artist.name.like("%" + str(term) + "%")
	).order_by(Artist.name.asc()).all()
	print('-' * 18 + 'Search results' + '-' * 18)
	print('the search term:', term)
	print('Contents of users:', users)
	print('Contents of artists:', artists)
	print('Contents of art:', art)
	print('-' * 50)
	return render_template(
		'search.html',
		user=users,
		arts=arts,
		artists=artists,
		term=term
	)


@app.route('/Make_playlist', methods=["POST"])
def Make_playlist():
	data = request.json
	print(data)
	p = Playlist(
		title=data['title'],
		desc=data['desc'],
		account_id=current_user.id
	)
	db.session.add(p)
	db.session.commit()
	flash('Playlist Created')
	return str(p.id)


@app.route('/get_playlist/<name>', methods=['POST'])
def get_playlist(name):
	playlist = Playlist.query.filter_by(title=name).first_or_404()
	return str(playlist.id)


@app.route('/add_to_playlist/<playlist_id>/<art_id>', methods=['POST'])
def add_to_playlist(playlist_id, art_id):
	a = Playlist_art(
		playlist_id=playlist_id,
		art_id=art_id
	)

	db.session.add(a)
	db.session.commit()
	return 'Succsess'


@app.route('/remove_from_playlist/<playlist_id>/<art_id>', methods=['POST'])
def remove_from_playlist(playlist_id, art_id):
	a = Playlist_art.query.filter_by(
		playlist_id=playlist_id,
		art_id=art_id
	).first_or_404()

	db.session.delete(a)
	db.session.commit()
	return 'Removed' + str(art_id) + 'from' + str(playlist_id)


@app.route('/delete_playlist/<playlist_id>', methods=['POST'])
def delete_playlist(playlist_id):
	playlist = Playlist.query.get(playlist_id)
	for i in Playlist_art.query.filter_by(playlist_id=playlist_id).all():
		db.session.delete(i)

	db.session.delete(playlist)
	db.session.commit()
	return 'Succsess deleted playlist' + str(playlist_id)


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
			u = Artist.query.filter_by(name=i['name']).first_or_404()
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
