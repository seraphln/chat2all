#!/usr/bin/env python
# coding=utf8
#


"""
constant variables for sso
"""

from sso.utils.enum import Enum


QQ_DOMAIN = 'graph.qq.com'


CONTENT_TYPES = {'.png': 'image/png',
                 '.gif': 'image/gif',
                 '.jpg': 'image/jpeg',
                 '.jpeg': 'image/jpeg',
                 '.jpe': 'image/jpeg'}


HTTP_ENUM = Enum(HTTP_GET=0,
                 HTTP_POST=1,
                 HTTP_UPLOAD=2)

COMMON_ARGS = ('access_token', 'oauth_consumer_key', 'openid', 'format')

def guess_content_type(ext):
    """
    get the content type with given ext
    if given ext not in CONTENT_TYPES dict,
    given a default type: application/octet-stream
    """

    return CONTENT_TYPES.get(ext, 'application/octet-stream')

