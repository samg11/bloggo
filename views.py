"""The views module is responsible for setting up the main routes and pages"""

# imports
import users, blogs
from auth import auth
import os
from flask import Flask, render_template, redirect, url_for
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
app.register_blueprint(users.users, url_prefix='/users')
app.register_blueprint(blogs.blogs, url_prefix='/blogs')

app.secret_key = os.getenv('BLOGGO_SECRET_KEY')


@app.route('/')
def index():
	auth_status = auth()
	return render_template('index.html', signed_in=auth_status[0], user=auth_status[1])


@app.route('/login')
def login():
	auth_status = auth()
	if auth_status[0]:
		return redirect(url_for('index'))
	return render_template('signin.html', signed_in=auth_status[0], user=auth_status[1])


@app.route('/signup')
def signup():
	auth_status = auth()
	if auth_status[0]:
		return redirect(url_for('index'))
	return render_template('signup.html', signed_in=auth_status[0], user=auth_status[1])

if __name__ == '__main__':
	app.run(debug=True)
