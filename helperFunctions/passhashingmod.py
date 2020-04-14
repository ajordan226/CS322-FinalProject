"""
This function will return a dictionary in JSON containing the password hash
and salt of a user given password using the PBKDF2 repeated hashing
algorithm and HMAC-SHA-256 as the underlying hashing standard. This
method is resistant to dictionary and rainbow table attacks.

See https://cryptobook.nakov.com/mac-and-key-derivation/pbkdf2
for details
"""

import os, import binascii
from backports.pbkdf2 import pbkdf2_hmac

def hash(password):
    salt = os.urandom(8)
    key = pbkdf2_hmac("sha256",password.encode("utf8"),salt,80000,32)
    return {"key": key, "salt": salt}

"""
This function serializes the JSON and stores it in file
"""

def storeInfo(user,passhash,email):
    userInfoJSON = {}
    with open("userinfo.json","r") as f:
        if os.path.getsize(f) == 0:
            pass
        else:
            userInfoJSON = json.load(f)

    userInfoJSON.update({user:{"passhash":passhash,"email":email}})

    with open("userinfo.json","w") as f:
        json.dump(pass_json, write_file)
