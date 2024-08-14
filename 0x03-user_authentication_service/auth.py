#!/usr/bin/env python3
'''auth module'''
from db import DB
import bcrypt
import uuid
from user import User
from sqlalchemy.exc import InvalidRequestError, NoResultFound


def _hash_password(password: str) -> bytes:
    '''takes string password
        returns salted hash password'''
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    '''genrate uuid using uuid module
        return string representation of uuid'''
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''addes user to database if their is no user found with this email'''

        try:
            self._db.find_user_by(email=email)
            raise ValueError("User <user's email> already exists")
        except (InvalidRequestError or NoResultFound):
            hashed_pwd = _hash_password(password)
            new_user = self._db.add_user(email, hashed_pwd)

        return new_user

    def valid_login(self, email: str, passwd: str) -> bool:
        '''validate login credentials'''
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(passwd.encode(), user.hashed_password):
                return True
        except Exception:
            pass
        return False

    def create_session(self, email: str) -> int:
        '''create a session for a user'''
        try:
            user = self._db.find_user_by(email=email)
            user.session_id = _generate_uuid()
            return user.session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        '''getting user using their session id'''

        if not session_id:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        '''delete user session from database'''
        if not user_id:
            return None

        try:
            self._db.update_user(user_id, session_id=None)
        except Exception:
            pass
