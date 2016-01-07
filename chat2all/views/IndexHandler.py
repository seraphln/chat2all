# coding=utf8
#

import tornado.web

from utils.config import config
from sso.qq.api import APIClient as QQAPIClient


class IndexHandler(tornado.web.RequestHandler):
    ''' '''
    def get(self):
        api = QQAPIClient(config.get('qq_apiid'),
                          config.get('qq_appkey'),
                          redirect_uri=config.get('qq_callback_url'))
        auth_url = api.get_authorization_url("authorize")
        self.render('index.html', auth_url=auth_url)