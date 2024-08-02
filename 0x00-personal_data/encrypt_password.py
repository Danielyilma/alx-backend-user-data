#!/usr/bin/env python3
'''hashing user password'''
import bcrypt


def hash_password(password: str) -> any:
    '''functio hash password using bcript hashpw'''
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode(), salt)


def is_valid(hashed_password: bytes, password: str) -> any:
    '''validate if a password match its hash'''
    return bcrypt.checkpw(password.encode(), hashed_password)
