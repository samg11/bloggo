from flask import Blueprint, redirect, render_template, url_for, request, session, flash
from db import database, get_user
from bson.objectid import ObjectId
from auth import auth, create_user_object

collection = database['follow']

follow = Blueprint('follow', __name__)

def get_number_of_followers(following):
	return collection.count_documents({
		'following': ObjectId(following)
	})

def get_number_of_following(follower):
	return collection.count_documents({
		'follower': ObjectId(follower)
	})

# def get_followers(following):
# 	return [get_user(f['follower']) for f in list(collection.find({
# 		'following': ObjectId(following)
# 	}))]

def get_following(follower):
	return [create_user_object(get_user(f['following'])) for f in list(collection.find({
		'follower': ObjectId(follower)
	}))]

def currently_following(follower, following):
	return collection.count_documents({
		'follower': ObjectId(follower),
		'following': ObjectId(following)
	})

@follow.route('/list/<u>')
def list_followers(u):
	auth_status = auth()

	return render_template('followers.html', signed_in=auth_status[0], user=auth_status[1])

@follow.route('/follow/<id>/<username>')
def follow_user(id, username):
	auth_status = auth()
	if not auth_status[0]:
		flash('You must be logged in to follow someone')
		return redirect(url_for('login'))
	
	if collection.count_documents({
		'follower': ObjectId(auth_status[1].id),
		'following': ObjectId(id)
	}):

		flash(f'You are already following {username}')
		return redirect(url_for('profile.user', username=username))

	collection.insert_one({
		'follower': ObjectId(auth_status[1].id),
		'following': ObjectId(id)
	})

	return redirect(url_for('profile.user', username=username))

@follow.route('/unfollow/<id>/<username>')
def unfollow_user(id, username):
	auth_status = auth()
	if not auth_status[0]:
		flash('You must be logged in to unfollow someone')
		return redirect(url_for('login'))

	follow_doc = {
		'follower': ObjectId(auth_status[1].id),
		'following': ObjectId(id)
	}

	if not collection.count_documents(follow_doc):
		return redirect(url_for('profile.user', username=username))

	collection.delete_one(follow_doc)

	return redirect(url_for('profile.user', username=username))