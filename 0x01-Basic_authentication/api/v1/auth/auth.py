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
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        for excluded_path in excluded_paths:
            if path.rstrip('/') == excluded_path.rstrip('/'):
                return False
            if excluded_path.endswith('*') and path.startswith(excluded_path[:-1]):
                return False
            elif path == excluded_path:
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
