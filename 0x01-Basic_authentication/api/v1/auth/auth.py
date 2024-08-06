#!/usr/bin/env python3
'''authentication module'''
from flask import request
from typing import TypeVar, List


class Auth:
    '''Auth class
        provides different feature for authentication
    '''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''Auth class
        provides different feature for authentication'''
        return False

    def authorization_header(self, request=None) -> str:
        '''Auth class
        provides different feature for authentication'''
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''Auth class
        provides different feature for authentication'''
        return None
