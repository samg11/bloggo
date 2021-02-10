'''Database Module'''

import encryption as enc
import pymongo
import os

MONGO_CONNECTION_URI = os.getenv("BLOGGO_MONGO_CONNECTION_URI")

cluster = pymongo.MongoClient(MONGO_CONNECTION_URI, authSource="admin")
database = cluster['users']
user_collection = database['users']

def get_user(id, by='_id'):
	return user_collection.find_one({
		by: id
	})

def user_exists(u):
	'''Checks if a user exists in the database'''
	return user_collection.count_documents({ "username":u })

def authenticate(username, password, ret_str=False):
	'''Authenticates user by taking a username and password as parameters'''
	user = user_collection.find_one({ 'username': username })
	if user:
		decrypted_password = enc.decrypt(user['password']).decode()
		if password == decrypted_password:
			return user

	if ret_str:
		return 'Fail'
	return False