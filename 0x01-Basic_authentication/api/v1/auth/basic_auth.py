#!/usr/bin/env python3

""" Basic Authentication module
"""

from api.v1.auth.auth import Auth
import base64


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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str) -> str:

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
