""""
Password salting and hashing example

Written by Jim Eddy
Modified by Daniel Eror
"""

import hashlib
import os
from base64 import b64encode


# import os  # << hint


def hash_pw(plain_text) -> str:
    salt = b64encode(os.urandom(30)).decode('utf-8')  # generates a 40-character random salt and decodes it to plaintext
    hashable = salt + plain_text  # concatenate salt and plain_text
    hashable = hashable.encode('utf-8')  # convert to bytes
    this_hash = hashlib.sha1(hashable).hexdigest()  # hash w/ SHA-1 and hexdigest
    return salt + this_hash  # prepend hash and return


def authenticate(stored, plain_text, salt_length=40) -> bool:
    salt = stored[:salt_length]  # extract salt from stored value
    stored_hash = stored[salt_length:]  # extract hash from stored value
    hashable = salt + plain_text  # concatenate hash and plain text
    hashable = hashable.encode('utf-8')  # convert to bytes
    this_hash = hashlib.sha1(hashable).hexdigest()  # hash and digest
    return this_hash == stored_hash  # compare
