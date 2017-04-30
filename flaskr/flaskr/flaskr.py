import os
import sqllite3

from flask import Flask, request, session, g, redirect, \
url_for, abort, render_template, flash

app = Flask(__name__)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='develkey',
    USERNAME='admin',
    PASSWORD='default'
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

"""
ENV CONFIG NOTE FROM DOCS
Simply define the environment variable FLASKR_SETTINGS that points to a config file to be loaded.
The silent switch just tells Flask to not complain if no such environment key is set.

In addition to that, you can use the from_object() method on the config object and provide it with
an import name of a module. Flask will then initialize the variable from that module.
Note that in all cases, only variable names that are uppercase are considered.
"""

""" SQLLITE DB CONNECTION
You can create a simple database connection through SQLite and then tell it to use
the sqlite3.Row object to represent rows.This allows the rows to be treated as if they
 were dictionaries instead of tuples.
"""

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv