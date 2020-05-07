class Poll:
    def __init__(self, group, pollType, unanimous):
        self.pollType = pollType
        self.unanimous = unanimous
        self.poll = {}
        for x in group:
            self.poll[x] = None

    def vote(user, userVote):
        if self.poll.has_key(user) and self.poll[user] is None:
            self.poll[user] = userVote

    def checkPoll():
        if self.unanimous:
            result = True
            for answer in self.poll.values():
                result = result and answer
            return result
        else:
            #initializa an empty dictionary to count results
            resultDict = {}
            for answer in self.poll.values():
                resultDict[answer] = resultDict.get(answer,0) + 1
            #counts the results
            maxVal = max(resultDict.values())
            #extracts the maximum value
            tieList = []
            for answer in resultDict.keys():
                if resultDict[answer] == maxVal:
                    tieList.append(answer)
            #extracts all
            if len(tieList) == 1:
                return True, tieList
            else:
                return False, tieList
