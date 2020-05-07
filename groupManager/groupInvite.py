import sys, os
import random
import string

print(sys.path)

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'helperFunctions'))

import emailsender

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("../UserClasses/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def inviteUser(sender, receiver, groupName):
    #### Initializes random string as invite passcode
    letters = string.ascii_lowercase #gets set of lowercase ascii characters
    randStr = ""

    for i in range(8):
        randStr = randStr + random.choice(letters) #iterativly append random ascii chars to a string
    #####
    userRef = db.collection(u'Project').document(u'pAKCeGKWGqm1B2MmLMuT').collection(u'Users')
    userDocument = userRef.document(receiver.encode("utf-8")).get().to_dict()
    emailsender.sendMail(userDocument['email'],"Invite to " + groupName, "Hello you have recieved an invite to " + groupName +". Enter the following code to enter: " + randStr)
    userDocument.update({ (groupName+"InviteCode").encode("utf-8") : randStr})

def acceptInvite(user, groupName, inviteCode):
    userRef = db.collection(u'Project').document(u'pAKCeGKWGqm1B2MmLMuT').collection(u'Users')
    userDocument = userRef.document(user.encode("utf-8")).get().to_dict()
    if inviteCode == userDocument[groupName+"InviteCode"]:
        groupProjectDoc = db.collection(u'Project).document(groupName.encode("utf-8")).get().to_dict()
        newMemberList = groupProjectDoc["members"].append(user)
        groupProjectDoc.update({u'members' : newMemberList})
        return True
    else:
        return False
