#!/usr/bin/env python
# coding=utf8
#

"""
http request relative functions
"""


import json
import time
import urllib
import requests

from utils.const import COMMON_ARGS
from utils.const import guess_content_type


class SDataDict(dict):
    """
    a simple abstract data structure,
    for saving the api return values
    """
    def __getattr__(self, key): 
        try:
            return self[key]
        except KeyError:
            return None

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError, k:
            raise AttributeError, k


def encode_params(method, **kwargs):
    """
        Encode parameters.

        if method == UPLOAD:
            do encode_multipart
        else:
            do url_encode
    """

    if method == 'UPLOAD':
        boundary = '----------%s' % hex(int(time.time() * 1000))
        data = []
        for k, v in kwargs.iteritems():
            data.append('--%s' % boundary)
            if hasattr(v, 'read'):
                # file-like object:
                ext = ''
                filename = getattr(v, 'name', '')
                n = filename.rfind('.')
                if n != (-1):
                    ext = filename[n:].lower()
                content = v.read()
                data.append('Content-Disposition: form-data; name="%s"; filename="hidden"' % k)
                data.append('Content-Length: %d' % len(content))
                data.append('Content-Type: %s\r\n' % guess_content_type(ext))
                data.append(content)
            else:
                data.append('Content-Disposition: form-data; name="%s"\r\n' % k)
                data.append(v.encode('utf-8') if isinstance(v, unicode) else v)
        data.append('--%s--\r\n' % boundary)
        return '\r\n'.join(data), boundary
    else:
        args = []
        for k, v in kwargs.iteritems():
            qv = v.encode('utf-8') if isinstance(v, unicode) else str(v)
            args.append('%s=%s' % (k, urllib.quote(qv)))
        return '&'.join(args), None


def request(method, url, authorization=None, request_source='qq', **kwargs):
    """
    a simple proxy for any http requests
    the request_source means which api called this request method
    for example: weibo or qq
    """
    params = None
    if authorization:
        kwargs.update(access_token=authorization)

    # Common args should always as get args
    if method != 'GET':
        params = {}
        for arg in COMMON_ARGS:
            params[arg] = kwargs.get(arg, '')

    params, boundary = encode_params(method, **kwargs)

    http_url = '%s?%s' % (url, params)
    params = None if method == 'GET' else params
    headers = {}
    if boundary:
        headers['Content-Type'] = 'multipart/form-data; boundary=%s' % boundary

    resp = requests.request(method, http_url, data=params,
                            headers=headers, timeout=2)
    body = resp.text
    if body.startswith('callback( '):
        body = body[10:-3]
    try:
        return SDataDict(json.loads(body))
    except:
        return body
