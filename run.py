from app import app
from db import db

db.init_app(app)

#creates the db with tables before any request if not there
@app.before_first_request
def create_tables():
	db.create_all()