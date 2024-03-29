#!/usr/bin/env python3
"""
SessionAuth module
"""
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """Session authentication class."""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a new session for the given user ID."""
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns the user ID associated with the provided session ID."""
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returns a User instance based on a cookie value."""
        if self.session_cookie(request) is None:
            return None

        if self.user_id_for_session_id(
                self.session_cookie(request)) is None:
            return None

        return User.get(self.user_id_for_session_id(
                self.session_cookie(request)))

    def destroy_session(self, request=None):
        """Deletes the user session / logout."""
        if request is None:
            return False

        session_id_cookie = self.session_cookie(request)
        if session_id_cookie is None:
            return False

        user_id = self.user_id_for_session_id(session_id_cookie)
        if user_id is None:
            return False

        del self.user_id_by_session_id[session_id_cookie]

        return True
