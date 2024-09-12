#!/usr/bin/env python3
from db import DB
import bcrypt
from user import User
from sqlalchemy.orm.exc import NoResultFound
# from sqlalchemy.exc import InvalidRequestError
import uuid
from typing import Union

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


def _generate_uuid() -> str:
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

    def create_session(self, email: str) -> str:
        """
        Creates a new session for the user identified by email.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        if user:
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id

    def get_user_from_session_id(self, session_id) -> Union[User, None]:
        """
        Returns the User object associated with a given session_id, or None if
        session_id is None or no user is associated with the session_id.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except Exception:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """Updates the corresponding user's session ID to None"""
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None

        self._db.update_user(user.id, session_id=None)

        return None

    def get_reset_password_token(self, email: str) -> str:
        """ implement the Auth.get_reset_password_token method.
        It take an email string argument and returns a string.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        new_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=new_token)
        return new_token
