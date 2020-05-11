import re
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from registrationStuff import userExists


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def getUserDocument(user):
    return db.collection(u'User').document(user.encode("utf-8")).get().to_dict()

def getProjectDocument(groupName):
    return db.collection(u'Project').document(groupName.encode("utf-8")).get().to_dict()

def isBlacklisted(user):
    return return db.collection(u'Blacklist').document(user.encode("utf-8")).get().exists

def appendToListAttrib(user,attrib,value):
    userDocument = getUserDocument(user)
    if value not in userDocument[attrib]:
        newAttribList = userDocument[attrib].append(value)
        userDocument.update({attrib.encode("utf-8") : newAttribList})

def removeUserFromGroup(userToRemove,groupName):
    groupProjectDoc = getProjectDocument(groupName)
    if userToRemove in groupProjectDoc['members']:
        newMemberList = groupProjectDoc.remove(userToRemove)
        groupProjectDoc.update({u'members' : newMemberList})

def banUser(userToRemove):
    userDocument = getUserDocument(userToRemove)
    db.collection(u'Blacklist').document(userToRemove.encode("utf-8")).set({u'email' : userDocument['email'], u'realname' : userDocument['realname']})
    userDocument.delete()

def update_rep(user, reputation):
    if userExists(user):
        info = getUserDocument(user)
        info['reputation']+=reputation

def update_warnings(user, groupName):
    if userExists(user):
        info = getUserDocument(user)
        info['warnings']+=1
    if info['warnings'] % 3 == 0:
        update_rep(user, -5)
        removeUserFromGroup(user, groupName)
        if info['reputation'] < 0:
            banUser(user)
        elif info['reputation'] < 25:
            info['VIP'] = False

def update_compliments(user):
    if userExists(user):
        info = getUserDocument(user)
        info['compliments']+=1
    if info['compliments'] % 3 == 0:
        update_rep(user, 5)
        if info['reputation'] >= 30:
            info['VIP'] = True

def disbandGroup(groupName)
    getProjectDocument(groupName).delete()
    #destruction of GUI stuff
