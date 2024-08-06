#!/usr/bin/env python3
'''basic authentication module'''
from api.v1.auth.auth import Auth


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
