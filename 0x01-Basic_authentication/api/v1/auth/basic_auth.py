#!/usr/bin/env python3
'''basic authentication module'''
from api.v1.auth.auth import Auth
import base64
from typing import Tuple


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
        except Exception as e:
            return None

        return decode.decode('utf-8')

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
            ) -> Tuple[str, str]:
        '''extract the username and password from base64 decoded string'''

        if not decoded_base64_authorization_header or \
                type(decoded_base64_authorization_header) is not str:
            return None

        if ':' not in decoded_base64_authorization_header:
            return None

        user_credential = decoded_base64_authorization_header.split(':')

        return (user_credential[0], user_credential[1])
