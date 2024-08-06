#!/usr/bin/env python3
'''authentication module'''
from flask import request
from typing import TypeVar, List


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

        if path not in excluded_paths:
            return True
        return False

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
