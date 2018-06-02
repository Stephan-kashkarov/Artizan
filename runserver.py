from app import app, db
from app.models import Person, Artist, Art


@app.shell_context_processor
def context():
	return {'db': db, 'Person': Person, 'Artist': Artist, 'Art': Art}
