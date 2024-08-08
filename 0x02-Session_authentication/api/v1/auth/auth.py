#!/usr/bin/env python3
'''authentication module'''
from flask import request
from typing import TypeVar, List
import os


class Auth:
    '''Auth class
        provides different feature for authentication
    '''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''checks if path does not exist in exluded_paths'''
        if not (path and excluded_paths):
            return True

        if path[-1] != "/":
            path += "/"

        for e_path in excluded_paths:
            if e_path == path:
                return False

            if e_path[-1] == '*' and e_path[:-1] in path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        '''return authorization header'''
        if not request:
            return None
        if not request.headers.get("Authorization", None):
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        '''Auth class
        provides different feature for authentication'''
        return None

    def session_cookie(self, request=None):
        '''return a cookie value from a request'''
        if not request:
            return None

        session_name = os.getenv('SESSION_NAME')

        return request.cookies.get(session_name)
