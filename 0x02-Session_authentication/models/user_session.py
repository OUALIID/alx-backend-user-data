#!/usr/bin/env python3
""" user_session module
"""
from models.base import Base


class UserSession(Base):
    """ UserSession class representing a user session."""
    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a new UserSession."""
        super().__init__(*args, **kwargs)
        self.user_id = ""
        self.session_id = ""
    