from ordinary_user import OrdinaryUser

class VIP(OrdinaryUser):
    """Ordinary Users whose reputation scores exceed a threshold set by Super User"""

    def __init__(self, name, email, interest, credential, reference):
        """Initialize attributes to describe a VIP."""
        super().__init__(name, email, interest, credential, reference)
        self.UserLevel = 'VIP'
        
    