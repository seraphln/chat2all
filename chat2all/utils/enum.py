#!/usr/bin/env python
# coding=utf8
#


"""
a simple Enum realize


>>> from enum import Enum
>>> enum = Enum(a=1)
>>> print enum(a)
1
"""

class Enum(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            self.__dict__[key] = value

    def __getattr__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        raise AttributeError()
