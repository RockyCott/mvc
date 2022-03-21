from sqlalchemy.orm import backref
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.cli import with_appcontext
import click
#from run import app

db_user = 'postgres'
db_key = '2191726'
db_url = 'localhost'
db_name = 'mvc'
full_url = f'postgresql://{db_user}:{db_key}@{db_url}/{db_name}'


db = SQLAlchemy()
#initializing db object
def db_init(app):
    db.init_app(app)

    #configuring flask-migrate
    migrate = Migrate(compare_type=True) 
    migrate.init_app(app, db)

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()