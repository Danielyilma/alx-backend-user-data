#!/usr/bin/env python3
'''session authentication module'''
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    '''session authentication class'''

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''create a session_id for user_id'''
        if not user_id or type(user_id) is not str:
            return None

        key = user_id + str(uuid.uuid4())
        self.user_id_by_session_id[key] = user_id

        return key
