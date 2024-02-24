#!/usr/bin/env python3
"""Hashes a password using bcrypt.
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """A function that returns a string representation of a new UUID."""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user in the authentication system."""
        try:
            self._db.find_user_by(email=email)
            raise ValueError
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """Check if login credentials are valid."""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Create a new session for the user."""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        user.session_id = _generate_uuid()
        return user.session_id

    def get_user_from_session_id(self, session_id: str):
        """Retrieve a user based on the session ID."""
        try:
            self._db.find_user_by(session_id=session_id)
            return User
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int):
        """Destroy the session for the user."""
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
        except NoResultFound:
            raise Exception

    def get_reset_password_token(self, email: str) -> str:
        """Generates a reset password token for the user."""
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            user.reset_token = token
            return token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str):
        """Update user's password using the reset token."""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(
                user.id, hashed_password=_hash_password(password),
                reset_token=None)
        except Exception:
            raise ValueError
