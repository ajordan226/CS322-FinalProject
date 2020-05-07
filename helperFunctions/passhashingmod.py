"""
This function will return a dictionary in JSON containing the password hash
and salt of a user given password using the PBKDF2 repeated hashing
algorithm and HMAC-SHA-256 as the underlying hashing standard. This
method is resistant to dictionary and rainbow table attacks.

See https://cryptobook.nakov.com/mac-and-key-derivation/pbkdf2
for details
"""
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import os, import binascii
from backports.pbkdf2 import pbkdf2_hmac

from .registrationStuff import userExists

cred = credentials.Certificate("../UserClasses/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

userRef = db.collection(u'Project').document(u'pAKCeGKWGqm1B2MmLMuT').collection(u'Users')

#Creates a key and salt for safe storage in a database
def hash(password):
    salt = os.urandom(8)
    key = pbkdf2_hmac("sha256",password.encode("utf-8"),salt,80000,32)
    return {"key": key, "salt": salt}

#Verifies a login attempt into a registered account
def verifyLogin(user,password):
    if userExists(user):
        userDocument = userRef.document(user.encode("utf-8")).get().to_dict()
        attemptedKey = pbkdf2_hmac("sha256",password.encode("utf-8"),userDocument['salt'],80000,32)
        success = attemptedKey == userDocument['key']
        if (not success):
            print("Incorrect password")
        return success
    else:
        print("An account with that user name does not exist")
        return False
