#!/usr/bin/env python
# coding=utf8
#


"""
constant variables for chat2all
"""


QQ_DOMAIN = 'graph.qq.com'


CONTENT_TYPES = {'.png': 'image/png',
                 '.gif': 'image/gif',
                 '.jpg': 'image/jpeg',
                 '.jpeg': 'image/jpeg',
                 '.jpe': 'image/jpeg'}


COMMON_ARGS = ('access_token', 'oauth_consumer_key', 'openid', 'format')

API_METHODS = ('POST', 'PATCH', 'PUT', 'GET', 'DELETE', 'PUT')

def guess_content_type(ext):
    """
    get the content type with given ext
    if given ext not in CONTENT_TYPES dict,
    given a default type: application/octet-stream
    """

    return CONTENT_TYPES.get(ext, 'application/octet-stream')

