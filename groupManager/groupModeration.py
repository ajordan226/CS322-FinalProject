import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'pollingSystem'))
sys.path.append(os.path.join(os.path.dirname(__file__),'..','helperFunction'))

import updateDB
import poll

def startGroupPoll(groupName,voteType,excludedVoter = ""):
    groupProjectDoc = updateDB.getProjectDocument(groupName)
    voters = []
    if excludedVoter.strip():
        voters = groupProjectDoc['members'].remove(excludedVoter)
    else:
        voters = groupProjectDoc['members']
    groupPoll = poll.createPoll(voters)
    groupProjectDoc.update({(voteType + "poll").encode("utf-8") : groupPoll})


#BLUEPRINT FOR VOTING FUNCTIONS FOR LATER SPECIFICATION
#def voteInPoll(user,voteType,groupName):
#    groupProjectDoc = updateDB.getProjectDocument(groupName)
#    groupPoll = groupProjectDoc[(voteType+"poll")]
#    poll.vote(user,groupPoll)
#    if poll.full(groupPoll):
#        pass #we might need to split this function up or just use if else
#             #blocks to cover each case in this function

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

def startSUElection(groupName,electionType):
    groupProjectDoc = updateDB.getProjectDocument(groupName)
    groupMembers = groupProjectDoc['members']
    vipVoters = []
    for member in groupMembers:
        info = updateDB.getUserDocument(member)
        if info['VIP']:
            vipVoters.append(member)
    electionPoll = poll.createPoll(vipVoters)
    groupProjectDoc['suElection'] = electionPoll

def voteInElection(user,groupName):
    groupProjectDoc = updateDB.getProjectDocument(groupName)
    groupPoll = groupProjectDoc['suElection']
    poll.vote(user,groupPoll)
    if poll.full(groupPoll):
        if poll.checkPoll(groupPoll,False):
            newSU = poll.getWinners(poll)[0]
            userDocument = updateDB.getUserDocument(newSU)
            userDocument['SU'] = True
