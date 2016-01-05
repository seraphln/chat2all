#!/usr/bin/env python
# coding=utf8
#

"""
Python SDK for Tencent QQ

Simple wrapper for qq oauth2(http://opensns.qq.com/)

author: seraphwlq@gmail.com
"""

from utils.const import QQ_DOMAIN
from utils.errors import QQAPIError
from utils.errors import SSOBaseException
from utils.http import SDataDict
from utils.http import encode_params
from utils.http import request

import time
import urlparse


class HttpObject(object):
    def __init__(self, client, method):
        self.client = client
        self.method = method

    def __getattr__(self, attr):
        def wrap(**kwargs):
            if self.client.is_expires():
                raise QQAPIError('100015', 'access token is revoked')

            openid = self.client.get_openid()
            return request(self.method,
                           '%s%s' % (self.client.api_url,
                                     attr.replace('__', '/')),
                           self.client.access_token,
                           oauth_consumer_key=self.client.app_id,
                           format='json', openid=openid, **kwargs)
        return wrap


class APIClient(object):
    """ Api Client """

    def __init__(self, app_id, app_key, redirect_uri=None, response_type='code'):
        self.app_id = app_id
        self.app_key = app_key
        self.redirect_uri = redirect_uri
        self.response_type = response_type
        self.auth_url = 'https://%s/oauth2.0/' % QQ_DOMAIN
        self.api_url = 'https://%s/' % QQ_DOMAIN
        self.access_token = None
        self.openid = None
        self.expires = 0.0
        self.get = HttpObject(self, 'GET')
        self.post = HttpObject(self, 'POST')
        self.upload = HttpObject(self, 'UPLOAD')

    def set_access_token(self, access_token, expires_in):
        self.access_token = str(access_token)
        self.expires = float(expires_in)
        self.openid = None

    def get_authorize_url(self, redirect_uri=None, display=None,
                          response_type='code', endpoint='authorize',
                          scopes=[], state=None):
        """ return the authroize url that should be redirect """
        redirect = redirect_uri if redirect_uri else self.redirect_uri
        if not redirect:
            raise SSOBaseException('Redirect uri is needed.')
      
        state = state if state is not None else 'default_state'
        kwargs = dict(client_id=self.app_id,
                    response_type=response_type,
                    redirect_uri=redirect,
                    scope=','.join(scopes),
                    state=state)
        if display:
            kwargs.update(display=display)
        encoded_params, _ = encode_params('GET', **kwargs)
        return '%s%s?%s' % (self.auth_url, endpoint, encoded_params)

    def get_authorization_url(self, endpoint, **kwargs):
        """ compatible with others """
        kwargs.update(endpoint=endpoint)
        return self.get_authorize_url(**kwargs)

    def request_access_token(self, code, redirect_uri=None,
                             grant_type='authorization_code', endpoint='token'):
        """
        return access token as object:
            {"access_token":"your-access-token","expires_in":12345678}
        expires_in is standard unix-epoch-time
        """
        redirect = redirect_uri if redirect_uri else self.redirect_uri
        if not redirect:
            raise SSOBaseException('Redirect uri is needed.')

        query_dct = {'client_id': self.app_id, 'client_secret': self.app_key,
                     'redirect_uri': redirect, 'code': code,
                     'grant_type': grant_type}
        ret = request('GET', '%s%s' % (self.auth_url, endpoint), **query_dct)
        # ret is a string like this:
        # "access_token=C8F28A60779B94518AF86E1FE8D92312&expires_in=7776000"
        ret = SDataDict(dict((k, v[0]) for k, v in urlparse.parse_qs(ret).items()))
        ret['expires_in'] = float(ret['expires_in']) + time.time()
        return ret

    def get_access_token(self, endpoint, **kwargs):
        """ compatible with others """
        kwargs.update(endpoint=endpoint)
        code = kwargs.pop('code', None)
        access_token =  self.request_access_token(code, **kwargs)
        access_token = SDataDict(access_token)
        access_token['expire_time'] = access_token.expires_in
        access_token['refresh_token'] = ''
        return access_token

    def get_openid(self):
        """ https://graph.qq.com/oauth2.0/me?access_token=YOUR_ACCESS_TOKEN """
        if not self.openid:
            if self.is_expires():
                msg = "You must set a correct access key to request an openid"
                raise SSOBaseException(msg)
            ret = request('GET', '%s%s' % (self.auth_url, 'me'),
                          authorization=self.access_token)
            self.openid = ret.openid
        return self.openid

    def is_expires(self):
        return not self.access_token or time.time() > self.expires

    def __getattr__(self, attr):
        return getattr(self.get, attr)

