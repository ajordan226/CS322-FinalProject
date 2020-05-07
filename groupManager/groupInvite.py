import sys, os
import random
import string

print(sys.path)

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'helperFunctions'))

import emailsender

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from .registrationStuff import userExists

cred = credentials.Certificate("../UserClasses/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def inviteUser(sender, receiver, groupName):
    #### Initializes random string as invite passcode
    letters = string.ascii_lowercase
    randStr = ""

    for i in range(8):
        randStr = randStr + random.choice(letters)
    #####

    userRef = db.collection(u'Project').document(u'pAKCeGKWGqm1B2MmLMuT').collection(u'Users')
    userDocument = userRef.document(receiver.encode("utf-8")).get().to_dict()
    emailsender.sendMail(userDocument['email'],"Invite to " + groupName, "Hello you have recieved an invite to " + groupName +". Enter the following code to enter: " + randStr)
    userRef.update({ (groupName+"InviteCode").encode("utf-8") : randStr})
