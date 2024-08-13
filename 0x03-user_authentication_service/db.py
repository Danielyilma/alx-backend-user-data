#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError, NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        '''adding user to the database and return User object'''
        user = User()
        user.email = email
        user.hashed_password = hashed_password
        self._session.add(user)
        self._session.commit()

        return user

    def find_user_by(self, **kwargs: dict) -> User:
        '''find user by attribute'''

        def check_attribute(attr: str):
            ''' checks the attribute is valid
                if valid
                    return user found by that attribute
            '''
            if attr not in User.__dict__:
                raise InvalidRequestError("Wrong attribute")

            return self._session.query(User).filter(
                getattr(User, attr) == kwargs[attr]
            ).first()

        result = list(map(check_attribute, kwargs))[0]

        if not result:
            raise NoResultFound("no result")
        return result
