import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def getUserDocument(user):
    return db.collection(u'User').document(user.encode("utf-8")).get().to_dict()

def getProjectDocument(groupName):
    return db.collection(u'Project').document(groupName.encode("utf-8")).get().to_dict()

def appendToListAttrib(user,attrib,value):
    userDocument = getUserDocument(user)
    if not value in databaseAccessors[attrib]:
        newAttribList = databaseAccessors[attrib].append(value)
        userDocument.update({attrib.encode("utf-8") : newAttribList})

def removeUserFromGroup(userToRemove,groupName):
    groupProjectDoc = getProjectDocument(group)
    if userToRemove in groupProjectDoc['members']:
        newMemberList = groupProjectDoc.remove(userToRemove)
        groupProjectDoc.update({u'members' : newMemberList})
