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
        if session_id and isinstance(session_id, str):
            user_sessions = UserSession().search({"session_id": session_id})
            if user_sessions:
                session_data = user_sessions[0]
                created_at = session_data.created_at
                if self.session_duration > 0:
                    expiry_time = created_at + timedelta(
                            seconds=self.session_duration)
                    if expiry_time < datetime.now():
                        return None
                return session_data.user_id
        return None

    def destroy_session(self, request=None):
        """Destroys the session associated with the request cookie."""
        session_id = self.session_cookie(request)
    
        if session_id:
            user_sessions = UserSession().search({"session_id": session_id})
            if user_sessions:
                try:
                    user_sessions[0].delete()
                    return True
                except Exception:
                    return None
        return None
