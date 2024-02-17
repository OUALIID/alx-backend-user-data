#!/usr/bin/env python3
"""
API Authentication Module
"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """Class for managing API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if authentication is required for a given path"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        for excluded_path in excluded_paths:
            if excluded_path.rstrip('*') in path:
                return False
            elif path.rstrip('/') == excluded_path.rstrip('/'):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Get the authorization header from the request"""
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current user from the request"""
        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from a request."""
        session_name = os.getenv("SESSION_NAME")
        if request or session_name is None:
            return None

        return request.cookies.get(session_name)
