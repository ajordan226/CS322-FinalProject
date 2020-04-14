import re

def passwordValid(pass):
    return True if (re.match(r'(?=.*[a-z]{1,})(?=.*[A-Z]{1,})(?=.*[0-9]{1,})',pass) and (len(pass) >= 6)) else False

def usernameValid(user):
    return True if (re.match(r'[a-zA-Z](?=.*[a-z]{1,})(?=.*[A-Z]{1,})(?=.*[0-9]{1,})',user) and (len(user) >= 5)) else False
