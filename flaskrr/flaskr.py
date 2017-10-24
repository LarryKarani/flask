import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__) # creates an aplication instance
app.config.from_object(__name__) #load config from this file, flaskr.py

# load default config and override config from an environment variable

app.config.update(dict(

	DATABASE = os.path.join(app.root_path, 'flaskr.dm'),
	SECRET_KEY= '#',
	USERNAME ='admin',
	PASSWORD = 'default')

	)
app.config.from_envvar('FLASKR_SETTINGS', silent = True)

def connect_db():
	"""connects to the specific database"""
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rvf 

def init_db():
	db = get_db()

	with app.open_resourse('schema.sql', mode='r') as f:
		db.cursor().executescript(f.read())


    db.commit()
@app.cli.command('initdb')
def initdb_command():
	"""Initializes the database"""
	init_db()
	print('Initialized the database.')


def get_db():
	"""Opens a new database connection if there is none\
	 yet for the current application contex"""

	 if not hasattr(g, 'sqlite_db'):
	 	g.sqlite_db = connect_db()


	 return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
	"""closes the database again after the request"""

	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()