#!/usr/bin/env python3
'''session expiration date'''
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    '''session expiration date'''

    def __init__(self) -> str:
        '''initilize a session expiration date'''
        try:
            self.session_duration = int(os.getenv(
                'SESSION_DURATION'
            ))
        except Exception as e:
            self.session_duration = 0
        super().__init__()

    def create_session(self, user_id=None):
        '''create a session id for a user'''
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }

        return session_id

    def user_id_for_session_id(self, session_id=None):
        '''override the parent class'''
        if not session_id:
            return None

        session = self.user_id_by_session_id.get(session_id)
        if not session:
            return None

        if self.session_duration <= 0:
            return session.get("user_id")

        if 'created_at' not in session.keys():
            return None

        ss_duration = timedelta(seconds=self.session_duration)
        if session.get('created_at') + ss_duration < datetime.now():
            return None
        return session.get("user_id")
