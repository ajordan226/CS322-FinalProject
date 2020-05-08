import re
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'helperFunctions'))
sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
import registrationStuff
import databaseAccessors


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def update_rep(user, reputation):
    if userExists(user):
        info = getUserDocument(user)
        info['reputation']+=reputation

def update_warnings(user, groupName):
    if userExists(user):
        info = getUserDocument(user)
        info['warnings']+=1
    if info['warnings'] == 3:
        update_rep(user, -5)

def update_compliments(user):
    if userExists(user):
        info = getUserDocument(user)
        info['compliments']+=1
