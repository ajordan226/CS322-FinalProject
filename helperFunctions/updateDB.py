import re
import firebase_admin
import random
import string

from firebase_admin import credentials
from firebase_admin import firestore

from helperFunctions.registrationStuff import passwordValid
from helperFunctions.passhashingmod import hash
from helperFunctions.emailsender import sendMail


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

#Verifies a login attempt into a registered account
def verifyLogin(user,password):
    if userExists(user):
        userDocument = getUserDocument(user)
        attemptedKey = pbkdf2_hmac("sha256",password,userDocument['salt'],80000,32)
        success = attemptedKey == userDocument['key']
        if (not success):
            print("Incorrect password")
        return success
    else:
        print("An account with that user name does not exist")
        return False

def createPotentialUser(user, realname, email, credentials, reference):
    db.collection(u'PendingUser').document(user).set({'name' : realname, 'email' : email, 'cred' : credentials, 'ref' : reference, 'tries' : 0})

def registerPotentialUser(user):
    info = db.collection(u'PendingUser').document(user).get().to_dict()
    letters = string.ascii_lowercase #gets set of lowercase ascii characters
    randStr = ""
    for i in range(8):
        randStr = randStr + random.choice(letters) #iterativly append random ascii chars to a string
    #####
    hashedPass = hash(randStr)
    db.collection(u'User').document(user).set({'name' : info['name'], 'email' : info['email'], 'cred' : info['cred'], 'ref' : info['ref'], 'key' : hashedPass['key'], 'salt': hashedPass['salt']})
    sendMail(info['email'],"Congrats on getting registered","Your temporary password is {passw} please login to change it.".format(passw = randStr))
    db.collection(u'PendingUser').document(user).delete()

def createGroup(user,groupName):
    db.collection(u'Project').document(groupName).set({'members' : [user], 'name' : groupName})

    db.collection(u'Project').document(groupName).collection('f').document('forum').set({'count' : 0})

def startGroupPoll(groupName,voteType,excludedVoter = ""):
    pollReference = db.collection(u'Project').document(groupName).document(voteType + "poll")
    groupProjectDoc = getProjectDocument(groupName)
    groupMembers = groupProjectDoc['members']
    voters = []
    if excludedVoter.strip():
        voters = groupProjectDoc['members'].remove(excludedVoter)
    else:
        voters = groupProjectDoc['members']
    for voter in voters:
        if pollType == "election":
            info = getUserDocument(voter)
            if info['VIP']:
                pollReference.update({voter : None})
        else:
            pollReference.update({voter : None})

def getUserDocument(user):
    return db.collection(u'User').document(user).get().to_dict()

def getProjectDocument(groupName):
    return db.collection(u'Project').document(groupName).get().to_dict()

def getPollDocument(groupName, voteType):
    return db.collecion(u'Project').document(groupName).document(voteType+'poll')

def changePass(user,newPass, newPassConfirm):
    userDocument = getUserDocument(user)
    if not passwordValid(newPass):
        print("Password must be mixed case at least 6 characters, be mixed case, and have a number")
        return False
    elif newPass != newPassConfirm:
        print("Passwords do not match")
        return False
    else:
        newPassHash = hash(newPass)
        userDocument.update({'key' : newPassHash['key']})
        userDocument.update({'salt' : newPassHash['salt']})
        return True

def isBlacklisted(user):
    return db.collection(u'Blacklist').document(user).get().exists

def appendToListAttrib(user,attrib,value):
    userDocument = getUserDocument(user)
    if value not in userDocument[attrib]:
        newAttribList = userDocument[attrib].append(value)
        userDocument.update({attrib : newAttribList})

def removeUserFromGroup(userToRemove,groupName):
    groupProjectDoc = getProjectDocument(groupName)
    if userToRemove in groupProjectDoc['members']:
        newMemberList = groupProjectDoc.remove(userToRemove)
        groupProjectDoc.update({u'members' : newMemberList})

def isMember(user,groupName):
    groupProjectDoc = getProjectDocument(groupName)
    return user in groupProjectDoc['members']

def getMembers(groupName):
    groupProjectDoc = getProjectDocument(groupName)
    return groupProjectDoc['members']

def banUser(userToRemove):
    userDocument = getUserDocument(userToRemove)
    db.collection(u'Blacklist').document(userToRemove).set({u'email' : userDocument['email'], u'realname' : userDocument['realname']})
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

def disbandGroup(groupName):
    getProjectDocument(groupName).delete()
    #destruction of GUI stuff

def userExists(user):
    return db.collection(u'User').document(user).get().exists

bad_words = ["poop","butt","pee","github","bitbucket","gitlab"]

#[user,msg]

def addMessage(user, groupName, message):
    forumPosts = db.collection(groupName).document('forum').get().to_dict()
    newCount = forumPosts['count'] + 1
    msgList = message.split
    for i in range(len(msgList)):
        if msgList[i] in bad_words:
            msgList[i] = "FeelsBad"
    db.collection(u'Project').document(groupName).collection('f').document('forum').update({'post'+newCount : [user," ".join(msgList)]})

#[[usr1,msg1],[us]]

def getMessages(groupName):
    forumPosts = db.collection(u'Project').document(groupName).collection('f').document('forum').get().to_dict()
    count = forumPosts['count']
    postList = []
    for i in range(1,count+1):
        postList.append(forumPosts['post'+i])
    return forumPosts
