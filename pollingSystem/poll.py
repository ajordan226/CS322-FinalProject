
def createPoll(groupMembers)
    poll = {}
    for member in groupMembers:
        poll[member] = None
    return poll

def vote(user, userVote, poll):
    poll.has_key(user) and poll[user] is None:
        poll[user] = userVote

def full(poll):
    result = True
    for answer in poll.values():
        result = result and (not answer is None)
    return result

def getWinners(poll):
    resultDict = {}
    for answer in poll.values():
        resultDict[answer] = resultDict.get(answer,0) + 1
    #counts the results
    maxVal = max(resultDict.values())
    #extracts the maximum value
    tieList = []
    for answer in resultDict.keys():
        if resultDict[answer] == maxVal:
            tieList.append(answer)
    return tieList

def checkPoll(poll,unanimous):
    if unanimous:
        result = True
        for answer in poll.values():
            result = result and answer
        return result
    else:
        #initializa an empty dictionary to count results
        tieList = getWinners(poll)
        #extracts all
        if len(tieList) == 1:
            return True
        else:
            return False
