#!/usr/bin/env python3
'''session authentication module'''
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    '''session authentication class'''

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''create a session_id for user_id'''
        if not user_id or type(user_id) is not str:
            return None

        key = str(uuid.uuid4())
        self.user_id_by_session_id[key] = user_id

        return key

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''retrieve the user id by session_id from
        user_id_by_session_id'''
        if not session_id or type(session_id) is not str:
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        '''return authenticated user'''
        user_id = self.user_id_for_session_id(self.session_cookie(request))

        if not user_id:
            return None

        return User.get(user_id)

    def destroy_session(self, request=None):
        '''destroy session id for a user'''
        if not request:
            return False

        session_id = self.session_cookie(request)

        if not session_id:
            return False

        if not self.user_id_for_session_id(session_id):
            return False

        del self.user_id_by_session_id[session_id]
        return True
