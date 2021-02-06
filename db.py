'''Database Module'''

import encryption as enc
import pymongo
import os

MONGO_CONNECTION_URI = os.getenv("BLOGGO_MONGO_CONNECTION_URI")

cluster = pymongo.MongoClient(MONGO_CONNECTION_URI)
database = cluster['users']
collection = database['users']

def user_exists(u):
	'''Checks if a user exists in the database'''
	return collection.count_documents({ "username":u })

def authenticate(username, password):
	'''Authenticates user by taking a username and password as parameters'''
	user = collection.find_one({ 'username': username })
	decrypted_password = enc.decrypt(user['password']).decode()
	if password == decrypted_password:
		return user
	
	else:
		return False