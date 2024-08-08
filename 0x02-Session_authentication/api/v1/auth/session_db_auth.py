#!/user/bin/env python3
'''permanent storage for session'''
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    '''session storsge'''
    def create_session(self, user_id=None):
        '''create a session for a user'''
        session_id = super().create_session(user_id)

        if not session_id:
            return None

        u_session = UserSession(user_id=user_id,
                                session_id=session_id)
        u_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        '''override the parent class'''
        users = UserSession.search({"session_id": session_id})
        if not users:
            return None

        return users[0].user_id

    def destroy_session(self, request=None):
        '''destroy session'''
        if not request:
            return False

        session_id = self.session_cookie(request)

        if not session_id:
            return False

        users = UserSession.search({"session_id": session_id})
        if not users:
            return None

        users[0].remove()

        return True
