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
        return False

    def authorization_header(self, request=None) -> str:
        """Public method to get the authorization header from a request."""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Public method to get the current user from a request."""
        return None
