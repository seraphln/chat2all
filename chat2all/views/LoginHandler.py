# coding=utf8
#


import json
import tornado.web

from models.users import User
from utils.config import config
from utils.contrib import make_error_response
from utils.contrib import make_success_response
from sso.qq.api import APIClient as QQAPIClient


class QQLoginHandler(tornado.web.RequestHandler):
    """ QQ联合登录 """
    def get(self):
        import ipdb;ipdb.set_trace()
        api = QQAPIClient(config.get('qq_apiid'),
                          config.get('qq_appkey'),
                          redirect_uri=config.get('qq_callback_url'))
        code = self.request.body.get('code')
        access_token = api.request_access_token(code)
        api.set_access_token(access_token['access_token'],
                             access_token['expires_in'])
        user_info = api.get.user__get_user_info()
        openid = api.get_openid()

        user = User.objects.filter(third_info__third_type='qq',
                                 third_info__openid=openid).first()
        if not user:
            user = User()

        user.nick_name = user_info.get('nickname', '')
        user.gender = user_info.get('gender', '')
        user.avatar = user_info.get('figureurl_qq_2', '')
        user.third_info = {'third_type': 'qq', 'info': user_info, 'openid': openid}
        user.save()
        set_login_cookie(self.request, user)
        # set user cookie

        self.write(json.dumps(make_response(user)))


class WeiboLoginHandler(tornado.web.RequestHandler):
    """ Weibo联合登录 """
    def get(self):
        self.render('dynamic-attack/index.html')


class DirectLoginHandler(tornado.web.RequestHandler):
    """ 直接登录 """
    def get(self):
        """ get直接返回登录页面 """
        self.render("login.html")

    def post(self):
        """ POST会检查给定的用户名和密码是否正确，如果不正确会返回错误 """
        params = self.request.form.to_dict()
        username = params.get('username')
        password = params.get('password')
        msg = u'用户名或密码错误'

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                res = self.redirect('/login/')
                res.set_cookie(config.get('login_cookie_key'),
                               encode_cookie(username))
                return res
            else:
                return self.render('login.html', user=user, msg=msg)
        except:
            return self.render('login.html', msg=msg)


class LogoutHandler(tornado.web.RequestHandler):
    """ 退出登录 """
    def post(self):
        """ 处理退出登录相关的事宜 """
        pass
