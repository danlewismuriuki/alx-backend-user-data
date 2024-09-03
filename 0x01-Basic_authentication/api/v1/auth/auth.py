#!/usr/bin/env python3
"""
Module to define the Auth class for managing API authentication.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Class to manage the API authentication."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Public method to check if authentication is required."""
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            # if the path has a * at the end
            if excluded_path.endswith('*'):
                # the code before the *
                if path.startswith(excluded_path[:-1]):
                    return False

            elif excluded_path.endswith('/'):
                if path == excluded_path:
                    return False
            else:
                if path == excluded_path + '/':
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """Public method to get the authorization header from a request."""
        if request is None:
            return None

        if 'Authorization' not in request.headers:
            return None

        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """Public method to get the current user from a request."""
        return None
