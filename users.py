"""Module which is for routes for users"""

from flask import Blueprint, redirect, url_for, request, session, flash
import encryption as enc
from dotenv import load_dotenv
load_dotenv()
import os
from time import time
import db
from db import database

collection = database['users']

users = Blueprint('users', __name__)

@users.route('/create_user', methods=['GET', 'POST'])
def create_user():
	if request.method == 'POST':
		if db.user_exists(request.form['username']):
			flash('User already exsits')

		elif request.form['password'] != request.form['password2']:
			flash('Passwords do not match')

		else:
			collection.insert_one({
				'first_name': request.form['first_name'],
				'last_name': request.form['last_name'],
				'username': request.form['username'],
				'password': enc.encrypt(request.form['password']),
				'date_created': int(time())
			})

			session['USERNAME'] = request.form['username']
			session['PASSWORD'] = request.form['password']

		return redirect(url_for('index'))
	
	else:
		return 'Please use a post request'

@users.route('/login', methods=['GET', 'POST'])
def login():
	if db.authenticate(request.form['username'], request.form['password']):
		session['USERNAME'] = request.form['username']
		session['PASSWORD'] = request.form['password']

	else:
		flash('Incorrect username or password')
	return redirect(url_for('login'))

@users.route('/signout')
def signout():
	session.clear()
	return redirect(url_for('index'))