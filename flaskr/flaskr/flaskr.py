import os
import sqlite3

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


# Init sqlite db, wrapped as Flask command below as initdb_command
def init_db():
    db = get_db()

    with app.open_resource('schema.sql', mode='r') as f:
    	db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

"""
ON ABOVE INIT AND INIT COMMAND
The open_resource() method of the application object is a convenient helper function that will open a 
resource that the application provides. This function opens a file from the resource location (the flaskr/flaskr folder)
 and allows you to read from it. It is used in this example to execute a script on the database connection.

The connection object provided by SQLite can give you a cursor object. On that cursor, there is a method to 
execute a complete script. Finally, you only have to commit the changes. SQLite3 and other transactional 
databases will not commit unless you explicitly tell it to.

Now, it is possible to create a database with the flask script:

flask initdb
Initialized the database.
"""

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


# VIEWS

# HOME - gets posted entries
@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)


# ADD A POST
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


# LOGOUT
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))



