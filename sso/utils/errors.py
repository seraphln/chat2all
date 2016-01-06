#!/usr/bin/env python
# coding=utf8
#


"""
included all the errors define
"""


class SSOBaseException(Exception):
    """ Base Exception """
    pass


class QQAPIError(SSOBaseException):
    """ raise APIError if got failed json message """

    def __init__(self, error_code, error):
        self.error_code = error_code
        self.error = error
        super(QQAPIError, self).__init__(self, error)

    def __str__(self):
        return 'QQAPIError: %s: %s' % (self.error_code, self.error)