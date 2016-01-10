# coding=utf8
#


import json
import tornado.web
from datetime import datetime

from models.users import User
from utils.config import config
from utils.contrib import make_error_response
from utils.contrib import make_success_response
from sso.qq.api import APIClient as QQAPIClient


class QQLoginHandler(tornado.web.RequestHandler):
    """ QQ联合登录 """
    def get(self):
        api = QQAPIClient(config.get('qq_apiid'),
                          config.get('qq_appkey'),
                          redirect_uri=config.get('qq_callback_url'))
        code = self.request.query_arguments.get('code')[0]
        print code
        access_token = api.request_access_token(code)
        api.set_access_token(access_token['access_token'],
                             access_token['expires_in'])
        user_info = api.get.user__get_user_info()
        openid = api.get_openid()

        now = datetime.utcnow()
        user = User.objects.filter(third_info__third_type='qq',
                                 third_info__openid=openid).first()
        if not user:
            user = User(create_on=now, modify_on=now, last_login=now)
        else:
            user.modify_on = now
            user.last_login = now

        user.username = openid
        user.nick_name = user_info.get('nickname', '')
        user.email = '%s@qq.com' % openid
        gender = 'm' if user_info.get('gender') == u'男' else 'f'
        user.gender = gender
        user.avatar = user_info.get('figureurl_qq_2', '')
        user.third_info = {'third_type': 'qq', 'info': dict(user_info), 'openid': openid}
        user.save()

        # set user cookie
        self.set_secure_cookie(config.get('uname'), openid)
        self.write(json.dumps(make_success_response(user_info)))


class WeiboLoginHandler(tornado.web.RequestHandler):
    """ Weibo联合登录 """
    def get(self):
        self.render('dynamic-attack/index.html')


class DirectLoginHandler(tornado.web.RequestHandler):
    """ 直接登录 """
    def get(self):
        """ get直接返回登录页面 """
        self.render("login.html", msg="")

    def post(self):
        """ POST会检查给定的用户名和密码是否正确，如果不正确会返回错误 """
        username = self.request.body_arguments.get('username')[0]
        password = self.request.body_arguments.get('password')[0]
        msg = u'用户名或密码错误'

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                self.set_secure_cookie(config.get('uname'), username)
                self.write(json.dumps(make_success_response({'uname': username})))
            else:
                self.render('login.html', user=user)
        except:
            self.render('login.html')


class LogoutHandler(tornado.web.RequestHandler):
    """ 退出登录 """
    def get(self):
        """ 处理退出登录相关的事宜 """
        self.clear_cookie(config.get('uname'))
        self.render('login.html', msg='')

    def post(self):
        """ 处理退出登录相关的事宜 """
        self.clear_cookie(config.get('uname'))
        self.render('login.html', msg='')
