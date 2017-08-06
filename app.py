# imports
from flask import Flask, render_template, request, session, \
    flash, redirect, url_for, g
import sqlite3

# configuration
DATABASE = 'blog.db'

# create an object for flask app
app = Flask(__name__)

# pulls in app configuration by looking for UPPERCASE variables
# App configuration will be pulled from arg passed it can be from class also or ext package
app.config.from_object(__name__)

# function used to connect to app configuration database
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

if __name__ == "__main__":
    app.run(debug=True)