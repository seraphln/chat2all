
#!/usr/bin/env python
# coding=utf8
#

"""
Python SDK for Weibo

Simple wrapper for weibo oauth2

author: seraphwlq@gmail.com
"""

import time

from utils.http import request
from utils.http import SDataDict
from utils.http import encode_params
from utils.const import WEIBO_DOMAIN
from utils.const import WEIBO_VERSION
from utils.errors import WeiboAPIError
from utils.errors import SSOBaseException


class HttpObject(object):

    def __init__(self, client, method):
        self.client = client
        self.method = method

    def __getattr__(self, attr):
        def wrap(**kwargs):
            if self.client.is_expires():
                raise WeiboAPIError('21327', 'expired_token')

            return request(self.method,
                           '%s%s.json' % (self.client.api_url,
                                          attr.replace('__', '/')),
                           self.client.access_token,
                           **kwargs)
        return wrap


class APIClient(object):
    """ API client using synchronized invocation """

    def __init__(self, app_key, app_secret, redirect_uri=None, response_type='code'):
        self.client_id = app_key
        self.client_secret = app_secret
        self.redirect_uri = redirect_uri
        self.response_type = response_type
        self.auth_url = 'http://%s/oauth2/' % WEIBO_DOMAIN 
        self.api_url = 'https://%s/%s/' % (WEIBO_DOMAIN, WEIBO_VERSION)
        self.api_url = 'http://%s/' % WEIBO_DOMAIN
        self.access_token = None
        self.expires = 0.0
        self.get = HttpObject(self, 'GET')
        self.post = HttpObject(self, 'POST')
        self.upload = HttpObject(self, 'UPLOAD')

    def set_access_token(self, access_token, expires_in):
        self.access_token = str(access_token)
        self.expires = float(expires_in)

    def get_authorize_url(self, redirect_uri=None, display='default'):
        """ return the authroize url that should be redirect """
        redirect = redirect_uri if redirect_uri else self.redirect_uri
        if not redirect:
            raise WeiboAPIError('21305', 'Parameter absent: redirect_uri', 'OAuth2 request')
        kwargs = dict(client_id=self.client_id,
                      response_type='code',
                      display=display,
                      redirect_uri=redirect)
        encoded_params, _ = encode_params('GET', **kwargs)
        print encoded_params
        return '%s%s?%s' % (self.auth_url, 'authorize', encoded_params)

    def request_access_token(self, code, redirect_uri=None):
        """
            return access token as object: 
                {"access_token":"your-access-token","expires_in":12345678}
                expires_in is standard unix-epoch-time
        """
        redirect = redirect_uri if redirect_uri else self.redirect_uri
        if not redirect:
            raise WeiboAPIError('21305', 'Parameter absent: redirect_uri')
        r = request('GET', '%s%s' % (self.auth_url, 'access_token'),
                    client_id=self.client_id, client_secret=self.client_secret,
                    redirect_uri=redirect, code=code, grant_type='authorization_code')

        r.expires_in += int(time.time())
        return r

    def is_expires(self):
        return not self.access_token or time.time() > self.expires

    def __getattr__(self, attr):
        return getattr(self.get, attr)
