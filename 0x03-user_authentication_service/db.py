#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


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
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email (str): The user's email address.
            hashed_password (str): The user's hashed password.

        Returns:
            User: The created User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by arbitrary keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments to filter the users table.

        Returns:
            User: The first User object that matches the criteria.

        Raises:
            NoResultFound: If no user is found with the provided criteria.
            InvalidRequestError: If the query arguments are invalid.
        """

        # Attempt to query the User table using filter_by with
        # the provided keyword arguments
        if not kwargs:
            return InvalidRequestError

        column_name = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in column_name:
                raise InvalidRequestError

        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound

        return user

    def update_user(self, user_id, **kwargs) -> None:
        """
    Update a user's attributes in the database.

    This method allows updating multiple attributes of a user in the database.
    It uses the `find_user_by` method to locate the user by their `user_id`,
    and then updates the user's attributes based on the provided keyword
        arguments.

    If any provided keyword argument does not correspond to an existing column
    in the `User` table, a `ValueError` is raised.

    Args:
        user_id (int): The unique identifier of the user to update.
        **kwargs: Arbitrary keyword arguments representing the attributes
            to be updated
                  and their new values. For example,
                    `email="new_email@example.com"`.

    Raises:
        ValueError: If any of the provided `kwargs` keys do not match
            any column name in
                    the `User` table.
                    """
        user = self .find_user_by(id=user_id)

        column_names = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in column_names:
                return ValueError

        for key, value in kwargs.items():
            setattr(user, key, value)

        self._session.commit()
