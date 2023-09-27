from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import click
import logging

basedir = os.path.abspath(os.path.dirname(__file__))  # Base directory path for database


app = Flask(__name__)  # Init application
app.config['SECRET_KEY'] = 'secret_key'  # Secret key application configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')  # Path to the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Track modifications which need turn off

db = SQLAlchemy(app)  # Init database

logging.basicConfig(filename='record.log', level=logging.INFO, format='%(message)s')


from app import auth
app.register_blueprint(auth.bp)
from app import blog
app.register_blueprint(blog.bp)


from app.models import User  # Import user table


@click.command('create-db')  # Create database with command line by flask --app wsgi create-db
def create_db_command():
    with app.app_context():
        db.create_all()


app.cli.add_command(create_db_command)  # Add command to application
