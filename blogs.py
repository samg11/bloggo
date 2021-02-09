from flask import Blueprint, redirect, render_template, url_for, request, session, flash
from datetime import datetime as dt
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

	to_date = lambda t: dt.fromtimestamp(t).strftime('%m/%d/%y')

	posts = collection.find({
		'posted_by': auth_status[1].id
	})
	return render_template('myblogs.html', signed_in=auth_status[0], user=auth_status[1], posts=list(posts), time=int(time()), to_date=to_date)

@blogs.route('/post', methods=['GET', 'POST'])
def post():
	auth_status = auth()
	if not auth_status[0]:
		flash('You must be logged in to create a blog post')
		return redirect(url_for('login'))

	elif request.method == 'GET':
		return render_template('postblog.html', signed_in=auth_status[0], user=auth_status[1],
			content=request.args.get('content') if request.args.get('content') else '',
			title=request.args.get('title') if request.args.get('title') else '',
			description=request.args.get('description') if request.args.get('description') else '')
	
	else:

		if len(request.form['description']) > 241 or len(request.form['content']) > 5001:
			if len(request.form['description']) > 241:
				flash('Description is too long')

			if len(request.form['content']) > 5001:
				flash('Content is too long')

			return redirect(url_for('blogs.post',
				content=request.form['content'],
				title=request.form['title'],
				description=request.form['description']))

		title_already_exists = collection.count_documents({
			'posted_by': auth_status[1].id,
			'title': request.form['title'],
		}) != 0

		if title_already_exists:
			flash('You already have a blog post with that title, please change it')

			return redirect(url_for('blogs.post',
				content=request.form['content'],
				description=request.form['description']))

		if not request.form['title'].strip() or not request.form['description'].strip() or not request.form['content'].strip():
			flash('You cannot have an empty input field.')
			return redirect(url_for('blogs.post',
				title=request.form['title'],
				content=request.form['content'],
				description=request.form['description']))

		collection.insert_one({
			'posted_by': auth_status[1].id,
			'time': int(time()),
			'title': request.form['title'],
			'description': request.form['description'],
			'content': request.form['content']
		})

		return redirect(url_for('blogs.myblogs',
				content=request.form['content'],
				title=request.form['title'],
				description=request.form['description']))

@blogs.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
	auth_status = auth()

	if not auth_status[0]:
		flash('You must be logged in to update a blog post')
		return redirect(url_for('login'))

	current_post = collection.find_one({
		'_id': ObjectId(id)
	})
	
	posted_by = current_post['posted_by']

	if ObjectId(auth_status[1].id) != posted_by:
		return redirect(url_for('index'))

	if not(request.form['title'].strip() and request.form['description'].strip() and request.form['content'].strip()):
		flash('You cannot have an empty input field.')
		return redirect(url_for('blogs.myblogs'))

	collection.update_one({
		'_id': current_post['_id'],
		'posted_by': ObjectId(auth_status[1].id)
	},{ "$set": {
		'posted_by': auth_status[1].id,
		'time': current_post['time'],
		'title': current_post['title'],
		'description': request.form['description'],
		'content': request.form['content']
	}})

	flash('Post Updated Successfully!')
	return redirect(url_for('blogs.myblogs'))

@blogs.route('/delete/<id>')
def delete(id):
	auth_status = auth()

	if not auth_status[0]:
		flash('You must be logged in to delete a blog post')
		return redirect(url_for('login'))

	posted_by = collection.find_one({
		'_id': ObjectId(id)
	})['posted_by']

	if ObjectId(auth_status[1].id) != posted_by:
		return redirect(url_for('index'))

	collection.delete_one({
		'_id': ObjectId(id)
	})

	flash('Blog Post Deleted!')
	return redirect(url_for('blogs.myblogs'))

@blogs.route('/view/<id>')
def show_blog(id):
	auth_status = auth()
	
	post = collection.find_one({
		'_id':ObjectId(id)
	})
	posted_by = db.get_user(post['posted_by'])

	return render_template('show_blog.html', signed_in=auth_status[0], user=auth_status[1],
		post=post,
		posted_by=posted_by,
		name=f'{posted_by["first_name"]} {posted_by["last_name"]}',
		date=dt.fromtimestamp(post['time']).strftime('%m/%d/%y') 
		)
