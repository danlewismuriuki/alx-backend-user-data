#!/usr/bin/env python3
from db import DB
import bcrypt
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid
# from db import DB

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


def _generate_uuid(id: str) -> str:
    """
    function should return a string representation of a new UUID.
    Use the uuid module.
    """
    new_id = str(uuid.uuid4())
    return new_id


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Registers a user in the database
        Returns: User Object
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hash_passw = _hash_password(password)
            user = self._db.add_user(email, hash_passw)

            return user
        else:
            raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        hashed_password_bytes = user.hashed_password.encode('utf-8')

        if bcrypt.checkpw(password.encode('utf-8'),
                          hashed_password_bytes):
            return True
        else:
            return False
