#!/usr/bin/env python3

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class User(Base):
    """
    User model for the 'users' table.

    This model defines the structure of the 'users' table in the database
    with the following columns:

    - id (INTEGER): The primary key of the table.
    - email (VARCHAR(250)): The email address of the user, which
    cannot be null.
    - hashed_password (VARCHAR(250)): The hashed password of the user,
    which can not be null.
    - session_id (VARCHAR(250)): The session ID associated with the user,
    which can be null.
    - reset_token (VARCHAR(250)): The reset token for the user's password,
    which can be null.

    Attributes:
    id (int): Unique identifier for the user.
    email (str): User's email address.
    hashed_password (str): Hashed password of the user.
    session_id (str): Session ID for user sessions.
    reset_token (str): Token for password reset functionality.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=False)
    reset_token = Column(String(250), nullable=False)
