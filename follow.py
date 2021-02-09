from flask import Blueprint, redirect, render_template, url_for, request, session, flash
from db import database
from bson.objectid import ObjectId
from auth import auth

collection = database['follow']

follow = Blueprint('follow', __name__)

def get_number_of_followers(following):
	return collection.count_documents({
		'following': ObjectId(following)
	})

def get_following(follower):
	return collection.find({
		'follower': ObjectId(follower)
	})

def currently_following(follower, following):
	return collection.count_documents({
		'follower': ObjectId(follower),
		'following': ObjectId(following)
	})

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