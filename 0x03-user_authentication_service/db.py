#!/usr/bin/env python3
"""DB module
    handle database interaction 
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError, NoResultFound

from user import Base, User
from typing import Any, Dict


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        '''adding user to the database and
            return User object
        '''
        user = User(email=email, hashed_password=hashed_password)

        try:
            self._session.add(user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            user = None

        return user

    def find_user_by(self, **kwargs: Dict[str, Any]) -> User:
        '''find user by attribute
        '''

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

        user = list(map(check_attribute, kwargs))[0]

        if not user:
            raise NoResultFound("no result")
        return user

    def update_user(self, user_id: int, **kwargs: Dict[str, Any]) -> None:
        '''update user attributes from kwargs by user_id
            if the attribute are wrong  ValueError will be raises
        '''
        try:
            user = self.find_user_by(id=user_id)
        except Exception:
            return None

        for key in kwargs:
            if key not in user.__dict__:
                raise ValueError("attribute not found")
            setattr(user, key, kwargs[key])
        self._session.commit()
