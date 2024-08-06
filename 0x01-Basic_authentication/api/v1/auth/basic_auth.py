#!/usr/bin/env python3
'''basic authentication module'''
from api.v1.auth.auth import Auth
import base64
from typing import Tuple, TypeVar
from models.user import User


class BasicAuth(Auth):
    '''basic authentication class'''

    def extract_base64_authorization_header(
              self, authorization_header: str) -> str:
        '''filters out the base64 part from authorization header'''

        if not authorization_header or type(authorization_header) is not str:
            return None

        data = authorization_header.split()
        if data[0] != 'Basic':
            return None

        return data[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        '''decode base64 encoding of an authorization header'''

        if not base64_authorization_header or\
                type(base64_authorization_header) is not str:
            return None

        try:
            decode = base64.b64decode(base64_authorization_header)
            decode = decode.decode("utf-8")
        except Exception as e:
            return None

        return decode

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
            ) -> Tuple[str, str]:
        '''extract the username and password from base64 decoded string'''

        if not decoded_base64_authorization_header or \
                type(decoded_base64_authorization_header) is not str:
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        idx = decoded_base64_authorization_header.find(':')
        user_credential = decoded_base64_authorization_header

        return (user_credential[:idx], user_credential[idx + 1:])

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        '''getting user object from credential'''

        if not (user_email or user_pwd) or type(user_pwd) is not str\
                or type(user_email) is not str:
            return None

        users = User.search({'email': user_email})

        if users == []:
            return None

        user = list(filter(lambda x: x.is_valid_password(user_pwd), users))

        if user == []:
            return None
        return user[0]

    def current_user(self, request=None) -> TypeVar('User'):
        '''return currently authenticated user'''
        if not request:
            return None

        auth_header = self.authorization_header(request)
        base64_auth_header = self.extract_base64_authorization_header(
            auth_header
        )
        decoded_auth_header = self.decode_base64_authorization_header(
            base64_auth_header
        )
        user_credential = self.extract_user_credentials(decoded_auth_header)

        return self.user_object_from_credentials(
            user_credential[0], user_credential[1]
        )
