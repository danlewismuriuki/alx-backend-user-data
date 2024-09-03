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
