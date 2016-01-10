#!/usr/bin/env python
# coding=utf-8

"""
just test for get an auth
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.curdir)))

from sso.weibo.api import APIClient

# Set your values here
APP_ID = '1851783867'
APP_KEY = 'c1742d1fd7ffcbd8cc582baa49159415'
#CALLBACK_URL = 'http://www.chatting2all.com/redirect/'
CALLBACK_URL = 'http://chat2all.lichenfan.com/weibo_redirect/'


api = APIClient(APP_ID, APP_KEY, redirect_uri=CALLBACK_URL)
print 'Open this url in your browser: %s' % api.get_authorize_url()
code = raw_input('Enter code parameter in your callback url args: ').strip()
access_token = api.request_access_token(code)
api.set_access_token(access_token['access_token'], access_token['expires_in'])
print api.get.user__get_user_info()

