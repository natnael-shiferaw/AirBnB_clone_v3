#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import hashlib


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """
        Initializes a user object.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments. It may contain
                'password' as a key.

        Notes:
            If 'password' is provided in kwargs, it will be hashed using
            MD5 before being stored in the object.
    """
        if kwargs:
            plaintext_password = kwargs.pop('password', None)
            if plaintext_password:
                # Hash the password using MD5
                hash_generator = hashlib.md5()
                hash_generator.update(plaintext_password.encode("utf-8"))
                hashed_password = hash_generator.hexdigest()
                kwargs['password'] = hashed_password
        super().__init__(*args, **kwargs)
