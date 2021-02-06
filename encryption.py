"""Module used for encryption and decryption"""

from cryptography.fernet import Fernet
from dotenv import load_dotenv
load_dotenv()
import os

def encrypt(string):
	"""Function used for encryption"""
	if type(string) == bytes:
		encoded = string

	else:
		encoded = string.encode()

	f = Fernet(os.getenv('BLOGGO_ENCRYPTION_KEY'))

	return f.encrypt(encoded)

def decrypt(string):
	"""Function used for decryption"""
	if type(string) == bytes:
		encoded = string

	else:
		encoded = string.encode()

	f = Fernet(os.getenv('BLOGGO_ENCRYPTION_KEY'))
	decrypted = f.decrypt(encoded)

	return decrypted