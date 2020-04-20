from ordinary_user import OrdinaryUser

class SuperUser(OrdinaryUser):
    """One founding SU who initializes the system. 
    One democratic SU who is voted by VIPs"""

    def __init__(self, name, email, interest, credential, reference):
        """Initialize attributes to describe a Super User."""
        super().__init__(name, email, interest, credential, reference)
        self.UserLevel = 'SuperUser'