#!/usr/bin/env python3
"""
SessionDBAuth module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from uuid import uuid4


class SessionDBAuth(SessionExpAuth):
    """ Provides session ID authentication using a database."""

    def create_session(self, user_id=None):
        """ Creates and returns a session ID."""
        session_id = str(uuid4())
        UserSession.create(user_id=user_id, session_id=session_id)
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Returns the associated user ID for the given session ID."""
        if session_id is None:
            return None

        user_session = UserSession.get_by_session_id(session_id)
        if user_session:
            return user_session.user_id
        else:
            None

    def destroy_session(self, request=None):
        """ Destroys the session associated with the request cookie."""
        if request is None:
            return False

        session_id_cookie = request.cookies.get(self.SESSION_NAME)
        if not session_id_cookie:
            return False
        return UserSession.delete_by_session_id(session_id_cookie)
