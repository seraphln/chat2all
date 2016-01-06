#!/usr/bin/env python
# coding=utf-8

"""
just test for get an auth
"""


from sso.qq.api import APIClient

# Set your values here
APP_ID = '101284802'
APP_KEY = '2bc6db4840f7708c860a026efd91fc41'
CALLBACK_URL = 'http://www.chatting2all.com/redirect/'

api = APIClient(APP_ID, APP_KEY, redirect_uri=CALLBACK_URL)
print 'Open this url in your browser: %s' % api.get_authorization_url("authorize")
code = raw_input('Enter code parameter in your callback url args: ').strip()
access_token = api.request_access_token(code)
api.set_access_token(access_token['access_token'], access_token['expires_in'])
import ipdb;ipdb.set_trace()
print api.get.user__get_user_info()
