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
        for excluded_path in excluded_paths:
            if '*' in excluded_path and path.startswith(
                    excluded_path.rstrip('*')):
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
