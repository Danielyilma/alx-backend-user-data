#!/usr/bin/env python3
'''auth module'''
from sqlalchemy.exc import InvalidRequestError, NoResultFound
from user import User
from db import DB
import bcrypt
import uuid


def _hash_password(password: str) -> bytes:
    '''takes string password
        returns salted hash password'''
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    '''genrate uuid using uuid module
        return string representation of uuid'''
    return str(uuid.uuid4())
