#!/usr/bin/env python
# coding=utf8
#


"""
chat2all user model
use MongoEngine as the backend
"""

from datetime import datetime

from mongoengine import Document
from mongoengine import DictField
from mongoengine import EmailField
from mongoengine import StringField
from mongoengine import BooleanField
from mongoengine import DateTimeField

from utils.hasher import check_password, make_password


class User(Document):
    """
    User model
    defined the basic columns
    """
    meta = {
        'allow_inheritance': True,
        'indexes': [
            {'fields': ['username'], 'unique': True, 'sparse': True}
        ]
    }

    email = EmailField(unique=True)
    username = StringField(unique=True)
    password = StringField()
    create_on = DateTimeField()
    modify_on = DateTimeField()
    last_login = DateTimeField()
    is_superuser = BooleanField(default=False)

    def __unicode__(self):
        return self.username

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def set_password(self, raw_password):
        """Sets the user's password - always use this rather than directly
        assigning to :attr:`~mongoengine.django.auth.User.password` as the
        password is hashed before storage.
        """
        self.password = make_password(raw_password)
        self.save()
        return self

    def check_password(self, raw_password):
        """Checks the user's password against a provided password - always use
        this rather than directly comparing to
        :attr:`~mongoengine.django.auth.User.password` as the password is
        hashed before storage.
        """
        return check_password(raw_password, self.password)

    @classmethod
    def create_user(cls, username, password, email=None):
        """Create (and save) a new user with the given username, password and
        email address.
        """
        now = datetime.now()

        if email is not None:
            try:
                email_name, domain_part = email.strip().split('@', 1)
            except ValueError:
                pass
            else:
                email = '@'.join([email_name, domain_part.lower()])

        user = cls(username=username, email=email, date_joined=now)
        user.set_password(password)
        user.save()
        return user


class UserProfile(Document):
    """
    User Profile Info
    """
    nick_name = StringField()
    sex = StringField()
    desc = StringField()
    avatar = StringField()
    third_info = DictField()
