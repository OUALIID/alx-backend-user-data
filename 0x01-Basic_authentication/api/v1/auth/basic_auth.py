#!/usr/bin/env python3
"""
API Authentication Module
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import base64


class BasicAuth(Auth):
    """BasicAuth class that inherits from Auth."""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """A method that returns the Base64 of the Authorization header."""
        if (authorization_header is None or
                not isinstance(authorization_header, str)):
            return None

        if authorization_header.startswith("Basic "):
            return authorization_header[6:]
        else:
            return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """A method that decodes Base64 Authorization header."""
        if (base64_authorization_header is None or
                not isinstance(base64_authorization_header, str)):
            return None
        try:
            return base64.b64decode(
                base64_authorization_header).decode('utf-8')
        except base64.binascii.Error:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Extract username and password from user credentials string."""
        if (not isinstance(
                decoded_base64_authorization_header, str) or ':' not in
                decoded_base64_authorization_header):
            return None, None
        email, password = decoded_base64_authorization_header.split(":", 1)
        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str):
        """Create a User object using provided user credentials."""
        if not all(isinstance(arg, str)for arg in (user_email, user_pwd)):
            return None

        user = User.search({'email': user_email})
        if user and user[0].is_valid_password(user_pwd):
            return user[0]

        return None
