from flask import session
from db import authenticate

class User:
	def __init__(self, id, first_name, last_name, username):
		self.id         = id
		self.first_name = first_name
		self.last_name  = last_name
		self.full_name  = f'{ first_name } {  last_name }'
		self.username   = username

def create_user_object(u):
	return User(u['_id'], u['first_name'], u['last_name'], u['username'])

def auth():
	if session.get('USERNAME') and session.get('PASSWORD'):
		user = authenticate(session.get('USERNAME'), session.get('PASSWORD'))
		signed_in = bool(user)
		
		if signed_in:
			return [signed_in, create_user_object(user)]
		
	return [False, False]