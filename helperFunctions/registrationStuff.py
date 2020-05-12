import re
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


#Predicate which returns true if a password is at least 6 characters long, mixed case, and has a number
def passwordValid(password):
    return True if (re.match(r'(?=.*[a-z]{1,})(?=.*[A-Z]{1,})(?=.*[0-9]{1,})',password) and (len(password) >= 6)) else False

#Predicate which returns true if a username is alphanumeric and is of size 5
def usernameValid(user):
    return True if (re.match(r'[a-zA-Z](?=.*[a-z]{0,})(?=.*[A-Z]{0,})(?=.*[0-9]{0,})',str(user)) and (len(user) >= 5)) else False

#Predicate which returns true if two strings separated by an @ is detected (is like an email)
def emailValid(email):
    return True if (re.match(r'\S+@\S+')) else False

#Predicate which returns true if the referredUser exists
def userExists(user):
    return db.collection(u'User').document(user).get().exists

#Verifies each field of the registration page before sending to the superuser for examination

