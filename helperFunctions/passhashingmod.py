"""
This function will return a dictionary in JSON containing the password hash
and salt of a user given password using the PBKDF2 repeated hashing
algorithm and HMAC-SHA-256 as the underlying hashing standard. This
method is resistant to dictionary and rainbow table attacks.

See https://cryptobook.nakov.com/mac-and-key-derivation/pbkdf2
for details
"""
import os 
import binascii
from backports.pbkdf2 import pbkdf2_hmac

#Creates a key and salt for safe storage in a database
def hash(password):
    salt = os.urandom(8)
    key = pbkdf2_hmac("sha256",password.encode("utf-8"),salt,80000,32)
    return {"key": key, "salt": salt}
