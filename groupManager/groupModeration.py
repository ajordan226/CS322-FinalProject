import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'pollingSystem'))
sys.path.append(os.path.join(os.path.dirname(__file__),'..','helperFunction'))

import updateDB
import poll

def full(groupName, voteType):
    result = True
    pollDoc = getPollDocument(groupName, voteType)
    for answer in pollDoc.values():
        result = result and (not answer is None)
    return result


def getWinners(groupName, voteType):
    resultDict = {}
    pollDoc = getPollDocument(groupName, voteType)
    for answer in pollDoc.values():
        resultDict[answer] = resultDict.get(answer,0) + 1
    #counts the results
    maxVal = max(resultDict.values())
    #extracts the maximum value
    tieList = []
    for answer in resultDict.keys():
        if resultDict[answer] == maxVal:
            tieList.append(answer)
    return tieList


def checkPoll(groupName, voteType ,unanimous):
    pollDoc = getPollDocument(groupName, voteType)
    if unanimous:
        result = True
        for answer in pollDoc.values():
            result = result and answer
        return result
    else:
        #initialize an empty dictionary to count results
        tieList = getWinners(groupName, voteType)
        #extracts all
        if len(tieList) == 1:
            return True
        else:
            return False

def vote(user, userVote, groupName, voteType, unanimous):
    pollDoc = getPollDocument(groupName, voteType)
    if pollDoc.has_key(user) and pollDoc[user] is None:
        pollDoc.update({user : userVote})
        if full(groupName, voteType):
            if checkPoll(groupName, voteType, unanimous):
                winner = getWinners(groupName, voteType)[0]
                return winner

"""
def voteInWarning(user,groupName):
    groupProjectDoc = updateDB.getProjectDocument(groupName)
    groupPoll = groupProjectDoc['warningpoll']
    poll.vote(user,groupPoll)
    if poll.full(groupPoll):
        if poll.checkPoll(groupPoll, True):
            warnedUser = (set(groupProjectDoc['members']) - set(groupPoll.keys()))[0]
            updateDB.update_warnings(warnedUser,groupName)
            groupProjectDoc.update({u'warningpoll' : {}})

def voteInKick(user,groupName):
    groupProjectDoc = updateDB.getProjectDocument(groupName)
    groupPoll = groupProjectDoc['groupkickpoll']
    poll.vote(user,groupPoll)
    if poll.full(groupPoll):
        if poll.checkPoll(groupPoll, True):
            kickedUser = (set(groupProjectDoc['members']) - set(groupPoll.keys()))[0]
            updateDB.removeUserFromGroup(kickedUser,groupName)
            groupProjectDoc.update({u'groupkickpoll' : {}})
"""

def voteInElection(user, userVote, groupName):
    electionDoc = db.collection(u'Project').document(groupName).document("suElection").get().to_dict()
    if electionDoc.has_key(user) and pollDoc[user] is None:
        electionDoc.update({user : userVote})
        if full(groupName, voteType):
            if checkPoll(groupName, voteType, unanimous):
                winner = getWinners(groupName, voteType)[0]
                return winner
