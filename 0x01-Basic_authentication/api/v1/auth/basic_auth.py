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
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
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
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ Create a User object using provided user credentials."""
        if (not isinstance(user_email, str) or
                not isinstance(user_pwd, str)):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        if users and len(users) == 1:
            user = users[0]
            if user.is_valid_password(user_pwd):
                return user

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieve the User instance for a request."""
        authorization_header = request.headers.get('Authorization')
        base64_auth_header = self.extract_base64_authorization_header(
            authorization_header)
        decoded_auth_header = self.decode_base64_authorization_header(
            base64_auth_header)
        user_email, user_pwd = self.extract_user_credentials(
            decoded_auth_header)
        return self.user_object_from_credentials(user_email, user_pwd)
