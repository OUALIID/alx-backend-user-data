#!/usr/bin/env python3
"""
API Authentication Module
"""
from api.v1.auth.auth import Auth
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
