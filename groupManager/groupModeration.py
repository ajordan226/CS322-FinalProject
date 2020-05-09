import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'pollingSystem'))
sys.path.append(os.path.join(os.path.dirname(__file__),'..'))

import updateDB
import poll

def startGroupPoll(groupName,voteType,excludedVoter = ""):
    groupProjectDoc = updateDB.getProjectDocument(groupName)
    voters = []
    if excludedVoter.strip():
        voters = groupProjectDoc['members'].remove(personToKick)
    else:
        voters = groupProjectDoc['members']
    groupPoll = poll.createPoll(voters)
    groupProjectDoc.update({(voteType + "poll").encode("utf-8") : groupPoll})

def voteInPoll(user,voteType):
    groupProjectDoc = updateDB.getProjectDocument(groupName)
    groupPoll = groupProjectDoc[(voteType+"poll")]
    poll.vote(user,groupPoll)
    if poll.full(groupPoll):
        pass #we might need to split this function up or just use if else
             #blocks to cover each case in this function
