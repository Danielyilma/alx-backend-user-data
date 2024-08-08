#!/usr/bin/env python3
'''user session model'''
from models.base import Base


class UserSession(Base):
    '''class to store user session in a permanent storage'''

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a UserSession instance
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
