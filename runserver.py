from app import app, db
from app.models import Person, Artist, Art, Playlist, Playlist_art


@app.shell_context_processor
def context():
	return {
		'db': db,
		'Person': Person,
		'Artist': Artist,
		'Art': Art,
		'Playlist': Playlist,
		'Playlist_art': Playlist_art
	}
