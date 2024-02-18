#!/usr/bin/env python3
""" user_session module
"""
from models.base import Base


class UserSession(Base):
    """ UserSession class representing a user session."""

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a new UserSession."""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')

    @classmethod
    def create(cls, user_id, session_id):
        """Create a new UserSession instance and save it to the database."""
        new_session = cls(user_id=user_id, session_id=session_id)
        new_session.save()
        return new_session
