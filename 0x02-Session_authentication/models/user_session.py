#!/usr/bin/env python3
""" user_session module
"""
from models.base import Base


class UserSession(Base):
    """ """
    def __init__(self, *args: list, **kwargs: dict):
        """ """
        super().__init__(*args, **kwargs)
        self.user_id = ""
        self.session_id = ""
    