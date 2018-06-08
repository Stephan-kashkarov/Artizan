"""The initialization file for the whole program.

To run the server:
- go to terminal
- navigate to the parent folder of this file
- do the command set FLASK_APP=runserver.py
- do the command flask run
- go to 127.0.0.1:5000 in Chrome(preferbly)
- enjoy
"""

from app import app, db
from app.models import Person, Artist, Art, Playlist, Playlist_art


@app.shell_context_processor
def context():
	"""Context for Flask shell .

	This allows for quick tesing of my database
	in the flask shell rather then having to import
	every model in the database
	"""
	return {
		'db': db,
		'Person': Person,
		'Artist': Artist,
		'Art': Art,
		'Playlist': Playlist,
		'Playlist_art': Playlist_art
	}
