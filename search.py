from flask import Blueprint, request, render_template
from db import database
from auth import auth, create_user_object
from datetime import datetime as dt

collection = database['users']

search = Blueprint('search', __name__)

@search.route('/')
def search_users():
	auth_status = auth()

	to_date = lambda t: dt.fromtimestamp(t).strftime('%m/%d/%y')

	query = request.args.get('q')

	results = collection.find({
		"username": { 
			'$regex': query
		}
	})

	return render_template('search.html', signed_in=auth_status[0], user=auth_status[1],
		results=[create_user_object(result) for result in list(results)],
		to_date=to_date,
		query=query
	)