#!/usr/bin/env python3

""" Basic Authentication module
"""

from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """
    BasicAuth class that inherits from Auth.
    For now, this class is empty and just serves as a placeholder.
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Extracts the Base64 part from the Authorization
        header for Basic Authentication.

        This method checks if the authorization_header is valid,
        starts with "Basic ",
        and extracts the Base64 encoded credentials part of the header.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes a Base64 encoded authorization header to a UTF-8 string.

        Args:
        base64_authorization_header (str): The Base64 encoded
        authorization header to decode.

        Returns:
        str: The decoded UTF-8 string if successful, or None if decoding fails.
        """

        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(
                base64_authorization_header, validate=True)
            return decoded_bytes.decode('utf-8')
        except (TypeError, ValueError, UnicodeEncodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts user email and password from a Base64 decoded
        authorization header.
        """
        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        parts = decoded_base64_authorization_header.split(":", 1)

        if len(parts) != 2:
            return None, None

        email, password = parts
        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Retrieves a User instance based on email and password credentials.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
    Retrieves the User instance for a request using Basic Authentication.

    This method performs the following steps:
    1. Checks if the request is provided.
    2. Extracts the Authorization header from the request.
    3. Extracts the Base64 part from the Authorization header.
    4. Decodes the Base64 string to retrieve user credentials.
    5. Extracts the user email and password from the decoded credentials.
    6. Finds and returns the User instance based on the email and password.

    Returns:
        User: The User instance if credentials are valid and a user is found.
        None: If any of the steps fail or the credentials are invalid.

    Parameters:
        request (Request, optional): The request object containing
        the Authorization header.

    Usage:
        user = auth.current_user(request)
    """
        if request is None:
            return None

        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        extract_b64 = self.extract_base64_authorization_header(auth_header)
        if extract_b64 is None:
            return None

        decode_b64 = self.decode_base64_authorization_header(extract_b64)
        if decode_b64 is None:
            return None

        user_email, user_pwd = self.extract_user_credentials(decode_b64)
        if user_email is None or user_pwd is None:
            return None

        return self.user_object_from_credentials(user_email, user_pwd)
