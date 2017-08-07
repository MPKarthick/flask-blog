# imports
from flask import Flask, render_template, request, session, \
    flash, redirect, url_for, g
import sqlite3
from functools import wraps


# configuration
DATABASE = 'blog.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = 'hard_to_guess'


# create an object for flask app
app = Flask(__name__)

# pulls in app configuration by looking for UPPERCASE variables
# App configuration will be pulled from arg passed it can be from class also or ext package
app.config.from_object(__name__)

# function used to connect to app configuration database
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.route('/', methods = ['GET','POST'])
def login():
    # return render_template('login.html')
    error = None
    status_code = 200
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or \
            request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials. Please try Again'
            status_code = 401
        else:
            session['logged_in'] = True
            flash("Login Successful...!")
            return redirect(url_for('main'))
    return render_template('login.html', error = error), status_code

def login_required(test):
    @wraps(test)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return test(*args,**kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))
    return wrap

@app.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form['title']
    post = request.form['post']
    if not title or not post:
        flash("All fields are required. Please try again.")
        return redirect(url_for('main'))
    else:
        g.db = connect_db()
        g.db.execute('insert into posts (title, post) values (?, ?)',[request.form['title'], request.form['post']])
        g.db.commit()
        g.db.close()
        flash('New entry was successfully posted!')
        return redirect(url_for('main'))

@app.route('/delete',methods=['POST'])
@login_required
def delete():
    title = request.form['title']
    if not title:
        flash("Please provide title value")
        return redirect(url_for('main'))
    else:
        g.db = connect_db()
        g.db.execute('delete from posts where title = ?',[request.form['title']])
        g.db.commit()
        g.db.close()
        flash('New entry was successfully posted!')
        return redirect(url_for('main'))

@app.route('/main')
@login_required
def main():
    g.db = connect_db()
    cur = g.db.execute('select * from posts')
    posts = [[dict(title=row[0], post=row[1]) for row in cur.fetchall()]]
    g.db.close()
    # print(posts)
    return render_template('main.html', posts = posts)

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    flash('You are logged out')
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=False)