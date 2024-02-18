#!/usr/bin/env python3
"""
SessionDBAuth module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import timedelta, datetime

class SessionDBAuth(SessionExpAuth):
    """ Provides session ID authentication using a database."""

    def create_session(self, user_id=None):
        """Creates a new UserSession instance and returns the session ID."""
        session_id = super().create_session(user_id)
        if isinstance(session_id, str):
            new_session = UserSession(user_id=user_id, session_id=session_id)
            new_session.save()
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """Returns the associated user ID for the given session ID."""
        if not session_id and not isinstance(session_id, str):
            return None

        instance = super().user_id_for_session_id(session_id)
        if instance is None:
            return None
        try:
            user_session = UserSession().search({"session_id": session_id})
        except Exception:
            return None
        if user_session is None or user_session == []:
            return None
        return user_session[0].user_id

    def destroy_session(self, request=None):
        """Destroys the session associated with the request cookie."""
        session_id = self.session_cookie(request)
        user_sessions = UserSession().search({"session_id": session_id})
        if user_sessions:
            user_sessions[0].delete()
            return True
        return False
