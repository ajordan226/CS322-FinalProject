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
