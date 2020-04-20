class OrdinaryUser():
    """All self registered users who are approved by SU. Need login"""

    def __init__(self, name, email, interest, credential, reference):
        """Initialize attributes to describe an Ordinary User."""
        self.name = name
        self.email = email
        self.interest = interest
        self.credential = credential
        self.reference = reference
        self.UserLevel = 'OrdinaryUser'
        self.reputation_score = 0
        self.compliments = 0
        self.warnings = 0

    def get_name(self):
        return self.name
    
    def get_user_level(self):
        return self.UserLevel

    def get_rep_score(self):
        return self.reputation_score

    def set_rep_score(self, reputation_score):
        self.reputation_score+=reputation_score

    def get_compliment(self):
        return self.compliments

    def set_compliments(self, compliments):
        self.compliments += compliments

    def get_warnings(self):
        return self.warnings

    def set_warnings(self, warnings):
        self.warnings += warnings
        