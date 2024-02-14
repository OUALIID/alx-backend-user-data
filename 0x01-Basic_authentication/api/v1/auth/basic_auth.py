#!/usr/bin/env python3
"""
API Authentication Module
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """BasicAuth class that inherits from Auth."""
    def extract_base64_authorization_header(
        self, authorization_header: str) -> str:
        """A method that returns the Base64 of the Authorization header."""
        if authorization_header is None or not isinstance(
            authorization_header, str):
            return None

        if authorization_header.startswith("Basic "):
            return authorization_header[6:]
        else:
            return None
