#!/usr/bin/env python3
'''auth module'''
from db import DB
import bcrypt
from user import User
from sqlalchemy.exc import InvalidRequestError, NoResultFound


def _hash_password(password: str) -> bytes:
    '''takes string password
        returns salted hash password'''
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


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
