from flask import Blueprint, redirect, url_for, render_template, request, flash, session
from db import database, authenticate, user_exists
from auth import auth

collection = database['users']

settings = Blueprint('settings', __name__)

@settings.route('/')
def index():
	auth_status = auth()
	if not auth_status[0]:
		return redirect(url_for('index'))

	return render_template('settings.html', signed_in=auth_status[0], user=auth_status[1])

@settings.route('/change_username', methods=['GET', 'POST'])
def change_username():
	auth_status = auth()

	if not auth_status[0]:
		return redirect(url_for('index'))

	if request.method == 'GET':
		return redirect(url_for('settings.index'))

	if user_exists(request.form['username']):
		flash(f'Username: {request.form["username"]} is already in use')
		return redirect(url_for('settings.index'))

	if not authenticate(auth_status[1].username, request.form['password']):
		flash('Incorrect current password')
		return redirect(url_for('settings.index'))

	collection.update_one(
		{'_id': auth_status[1].id},
		{ '$set': {
			'username': request.form['username']
		}}
		)

	session['USERNAME'] = request.form['username']

	flash(f'Username changed from {auth_status[1].username} to {request.form["username"]}')
	return redirect(url_for('settings.index'))

@settings.route('/change_password', methods=['GET', 'POST'])
def change_password():
	auth_status = auth()
	if not auth_status[0]:
		return redirect(url_for('index'))

	if request.method == 'GET':
		return redirect(url_for('settings.index'))

	return redirect(url_for('settings.index'))