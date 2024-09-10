#!/usr/bin/env python3
import bcrypt
"""define a _hash_password method that takes in a password
    string arguments and returns bytes.
"""


def _hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt and returns the hashed password as a string.
    """
    salt = bcrypt.gensalt()

    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed.decode('utf-8')
