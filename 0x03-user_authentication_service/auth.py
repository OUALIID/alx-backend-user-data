#!/usr/bin/env python3
"""
Hashes a password using bcrypt.
"""
import bcrypt


def _hash_password(self, password= str) -> bytes:
    """Hashes a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'),
                         bcrypt.gensalt())
