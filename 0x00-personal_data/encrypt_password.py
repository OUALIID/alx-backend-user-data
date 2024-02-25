#!/usr/bin/env python3
"""
Personal data
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt."""
    return bcrypt.hashpw(password.encode(),
                         bcrypt.gensalt())
