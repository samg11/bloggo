"""The views module is responsible for setting up the main routes and pages"""

# imports
import users, blogs, profile, search, follow, settings
from auth import auth
import os
from flask import Flask, render_template, redirect, url_for, flash
from jinja_markdown import MarkdownExtension
from dotenv import load_dotenv
from follow import get_following
from datetime import datetime as dt
load_dotenv()


app = Flask(__name__)
app.register_blueprint(users.users,       url_prefix='/users')
app.register_blueprint(blogs.blogs,       url_prefix='/blogs')
app.register_blueprint(profile.profile,   url_prefix='/profile')
app.register_blueprint(search.search,     url_prefix='/search')
app.register_blueprint(follow.follow,     url_prefix='/follow')
app.register_blueprint(settings.settings, url_prefix='/settings')

app.secret_key = os.getenv('BLOGGO_SECRET_KEY')

app.jinja_env.add_extension(MarkdownExtension)

to_date = lambda t: dt.fromtimestamp(t).strftime('%m/%d/%y')

@app.route('/')
def index():
	auth_status = auth()

	users_following = False
	if auth_status[0]:
		users_following = get_following(auth_status[1].id)

	return render_template('index.html', signed_in=auth_status[0], user=auth_status[1],
		users_following=users_following, to_date=to_date)

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

@app.route('/code')
@app.route('/opensource')
@app.route('/sourcecode')
def code():
	return redirect('https://github.com/samg11/bloggo')

app.jinja_env.cache = {}

if __name__ == '__main__':
	app.run(debug=True)
