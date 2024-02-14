#!/usr/bin/env python3
"""
API Authentication Module
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Class for managing API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if authentication is required for a given path"""
        return False

    def authorization_header(self, request=None) -> str:
        """Get the authorization header from the request"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current user from the request"""
        return None

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ """
        if path and excluded_paths is None or len(excluded_paths) == 0:
            return True

        for excluded_path in excluded_paths:
            if path.rstrip('/') == excluded_path.rstrip('/'):
                return False

        return True
