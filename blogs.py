from flask import Blueprint, redirect, render_template, url_for, request, session, flash
from datetime import datetime
from auth import auth
import db
from db import database
from time import time
from bson.objectid import ObjectId

collection = database['posts']

blogs = Blueprint('blogs', __name__)
@blogs.route('/')
def myblogs():
	auth_status = auth()
	if not auth_status[0]:
		return redirect(url_for('index'))
	posts = collection.find({
		'posted_by': auth_status[1].id
	})
	return render_template('myblogs.html', signed_in=auth_status[0], user=auth_status[1], posts=posts, time=int(time()))

@blogs.route('/post', methods=['GET', 'POST'])
def post():
	auth_status = auth()
	if not auth_status[0]:
		flash('You must be logged in to create a blog post')
		return redirect(url_for('login'))

	elif request.method == 'GET':
		return render_template('postblog.html', signed_in=auth_status[0], user=auth_status[1])
	
	else:
		collection.insert_one({
			'posted_by': auth_status[1].id,
			'time': int(time()),
			'title': request.form['title'],
			'content': request.form['content']
		})

		return redirect(url_for('blogs.myblogs'))

@blogs.route('/<id>')
def show_blog(id):
	auth_status = auth()
	
	post = collection.find_one({
		'_id':ObjectId(id)
	})
	print(post)
	posted_by = db.get_user(post['posted_by'])

	return render_template('show_blog.html', signed_in=auth_status[0], user=auth_status[1],
		post=post,
		posted_by=posted_by,
		name=f'{posted_by["first_name"]} {posted_by["last_name"]}',
		date=datetime.fromtimestamp(post['time']).strftime('%d/%m/%y') 
		)

