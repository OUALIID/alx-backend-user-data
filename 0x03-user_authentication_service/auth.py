#!/usr/bin/env python3
"""Hashes a password using bcrypt.
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user in the authentication system."""
        if self._db.find_user_by(email=email):
            raise ValueError
        else:
            return self._db.add_user(email, _hash_password(password))
