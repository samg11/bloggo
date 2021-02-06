from flask import session
from db import authenticate

class User:
	def __init__(self, id, first_name, last_name, username):
		self.id         = id
		self.first_name = first_name
		self.last_name  = last_name
		self.full_name  = f'{ first_name } {  last_name }'
		self.username   = username

def auth():
	if session.get('USERNAME') and session.get('PASSWORD'):
		user = authenticate(session.get('USERNAME'), session.get('PASSWORD'))
		signed_in = bool(user)
		
		if signed_in:
			return [signed_in, User(user['_id'], user['first_name'], user['last_name'], user['username'])]
		
	return [False, False]