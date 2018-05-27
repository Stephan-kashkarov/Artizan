from app import app, db
from app.models import Person

print("\n" + "-"*20 + "Welcome to Collector-3.0" + "-"*20 + "\n")

@app.shell_context_processor
def context():
	return {'db': db, 'Person': Person}
