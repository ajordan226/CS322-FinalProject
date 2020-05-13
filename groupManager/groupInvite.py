import sys, os
import random
import string

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'helperFunctions'))
sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
import emailsender
import updateDB


import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("../UserClasses/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def inviteUser(sender, receiver, groupName):
    userDocument = updateDB.getUserDocument(receiver)
    if sender in userDocument['whitelist']:
        groupProjectDoc = updateDB.getProjectDocument(groupName)
        newMemberList = groupProjectDoc["members"].append(receiver)
        groupProjectDoc.update({u'members' : newMemberList})
        emailsender.sendMail(userDocument['email'],"Invite to " + groupName, "Hello you have recieved an invite to " + groupName + ". This was a whitelisted user so you have immediete access")
        userDocument.update({ (groupName+"InviteCode") : randStr})

    #### Initializes random string as invite passcode
    elif not sender in userDocument['blacklist']:
        letters = string.ascii_lowercase #gets set of lowercase ascii characters
        randStr = ""
        for i in range(8):
            randStr = randStr + random.choice(letters) #iterativly append random ascii chars to a string
        #####
        emailsender.sendMail(userDocument['email'],"Invite to " + groupName, "Hello you have recieved an invite to " + groupName +". Enter the following code to enter: " + randStr)
        userDocument.update({ (groupName+"InviteCode") : randStr})
    else:
        pass

def acceptInvite(user, groupName, inviteCode):
    userDocument = updateDB.getUserDocument(user)
    if inviteCode == userDocument[groupName+"InviteCode"]:
        groupProjectDoc = updateDB.getProjectDocument(groupName)
        newMemberList = groupProjectDoc["members"].append(user)
        groupProjectDoc.update({u'members' : newMemberList})
        return True
    else:
        return False

def addWhiteList(user,userToAdd):
    updateDB.appendToListAttrib(user,"whitelist",userToAdd)


def addBlackList(user,userToAdd):
    updateDB.appendToListAttrib(user,"blacklist",userToAdd)
