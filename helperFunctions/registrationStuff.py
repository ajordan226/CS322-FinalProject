import re
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("../serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


#Predicate which returns true if a password is at least 6 characters long, mixed case, and has a number
def passwordValid(pass):
    return True if (re.match(r'(?=.*[a-z]{1,})(?=.*[A-Z]{1,})(?=.*[0-9]{1,})',pass) and (len(pass) >= 6)) else False

#Predicate which returns true if a username is alphanumeric and is of size 5
def usernameValid(user):
    return True if (re.match(r'[a-zA-Z](?=.*[a-z]{0,})(?=.*[A-Z]{0,})(?=.*[0-9]{0,})',user) and (len(user) >= 5)) else False

#Predicate which returns true if two strings separated by an @ is detected (is like an email)
def emailValid(email):
    return True if (re.match(r'\S+@\S+')) else False

#Predicate which returns true if the referredUser exists
def userExists(user):
    return db.collection(u'User').document(user.encode("utf-8")).get().exists

#Verifies each field of the registration page before sending to the superuser for examination
def register(username,realname,email,credentials,reference):
    if usernameValid(user):
        if (userExists(user)):
            if (not realname.strip()):
                if (not credentials.strip()):
                    if (not userExists(reference)):
                        pass #Once a superuser is defined we send them this information before it is written to the DB.
                    else:
                        print("Reference does not exist")
                else:
                    print("Credentials field is empty")
            else:
                print("Name field is empty")
        else:
            print("Username already exists")
    else:
        print("A username must be alphanumeric only")
