'''Module for viewing other peoples profiles'''

from auth import auth, create_user_object
import db
from db import database
from flask import Blueprint, render_template, redirect, url_for
from datetime import datetime as dt
from follow import currently_following, get_number_of_followers

profile = Blueprint('profile', __name__)

collection = database['posts']

to_date = lambda t: dt.fromtimestamp(t).strftime('%m/%d/%y')

@profile.route('/view/<username>')
def user(username):
	auth_status = auth()
	
	other_user = create_user_object(db.get_user(username, 'username'))
	posts = collection.find({
		'posted_by': other_user.id
	})

	following = False

	if auth_status[0]:
		following = currently_following(auth_status[1].id, other_user.id)

	return render_template('profile.html', signed_in=auth_status[0], user=auth_status[1],
		other_user=other_user, posts=list(posts), to_date=to_date, following=following,
		number_of_followers=get_number_of_followers(other_user.id),
		same_user=other_user.id==auth_status[1].id)