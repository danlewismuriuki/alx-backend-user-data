#!/usr/bin/env python3
"""Module to define the SessionAuth class for session-based
    authentication.

This module defines the SessionAuth class, which inherits from
    the Auth base class.
Currently, this class is a placeholder and does not implement
    any authentication logic.
It serves as the initial step towards creating a new authentication
    mechanism based on sessions.

The SessionAuth class is expected to implement session-based
    authentication methods in future updates.
"""
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """Class for session-based authentication.

    Inherits from the Auth base class. This class currently does not implement
    any authentication methods but serves as a placeholder for future
        development
    of session-based authentication mechanisms.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a new session for a given user and returns the session ID.
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves the user ID associated with a given session ID.

        Args:
            session_id (str): The session ID for which to retrieve the user ID.

        Returns:
            str: The user ID if session_id is valid, else None.
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None

        user_id = self.user_id_by_session_id.get(session_id)

        return user_id

    def current_user(self, request=None):
        """
    Retrieves the User instance associated with the
    session ID from a request cookie.

    This method takes a request object, retrieves the
    session ID from the request's
    cookies using the session_cookie method, then finds
    the corresponding user ID
    using the user_id_for_session_id method. Finally, it
    retrieves the User instance
    from the database using the user ID.

    Args:
        request (flask.Request, optional): The HTTP request
        object from which to retrieve the session cookie.

    Returns:
        User: The User instance associated with the session ID
        if it exists, otherwise None.
    """
        session_id = self.session_cookie(request)
        if session_id is None:
            return None

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None

        user = User.get(user_id)
        return user
