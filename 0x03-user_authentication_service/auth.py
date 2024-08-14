#!/usr/bin/env python3
'''auth module'''
import bcrypt


def _hash_password(password: str) -> bytes:
    '''takes string password
        returns salted hash password'''
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
