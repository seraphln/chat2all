# coding=utf8
#


"""
login relative functions

inlucded:
    qq login
    weibo login
    normal login
"""

from app import app
from app import request

from models.users import User
from models.users import UserProfile

from sso.qq.api import APIClient as QQAPIClient


@app.route('/register/', methods=['POST', 'GET'])
def register():
    """

    """
    pass


@app.route('/qq_redirect/', methods=['POST', 'GET'])
def qq_login():
    """
    {u'province': u'\u5317\u4eac', u'yellow_vip_level': u'0', u'is_lost': 0, u'figureurl_qq_2': u'http://q.qlogo.cn/qqapp/101284802/554A183DD46C32645091DB005735C618/100', u'vip': u'0', u'is_yellow_year_vip': u'0', u'year': u'1988', u'nickname': u'\u52a0\u83f2', u'figureurl_1': u'http://qzapp.qlogo.cn/qzapp/101284802/554A183DD46C32645091DB005735C618/50', u'city': u'\u4e1c\u57ce', u'figureurl': u'http://qzapp.qlogo.cn/qzapp/101284802/554A183DD46C32645091DB005735C618/30', u'figureurl_2': u'http://qzapp.qlogo.cn/qzapp/101284802/554A183DD46C32645091DB005735C618/100', u'level': u'0', u'gender': u'\u7537', u'figureurl_qq_1': u'http://q.qlogo.cn/qqapp/101284802/554A183DD46C32645091DB005735C618/40', u'ret': 0, u'is_yellow_vip': u'0', u'msg': u''}

    """
    import ipdb;ipdb.set_trace()
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

    set_login_cookie(request, user)
    # set user cookie


@app.route('/weibo_redirect/', methods=['POST', 'GET'])
def weibo_login():
    """

    """
    pass


@app.route('/login/', methods=['GET', 'POST'])
def login():
    """
    登录
    """
    if request.method == 'GET':
        return render_template('login.html')
    else:
        params = request.form.to_dict()
        username = params.get('username')
        password = params.get('password')
        msg = u'用户名或密码错误'

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                res = redirect('/login/')
                res.set_cookie(config.get('login_cookie_key'),
                               encode_cookie(username))
                return res
            else:
                return render_template('login.html', user=user, msg=msg)
        except:
            return render_template('login.html', msg=msg)


@app.route('/admin/logout/', methods=['GET', 'POST'])
def logout():
    """
    退出登录
    """
    res = redirect('/index/')
    res.set_cookie(config.get('login_cookie_key'), '')
    return res
