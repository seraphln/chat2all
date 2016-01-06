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


@app.route('/register/', methods=['POST', 'GET'])
def register():
    """

    """
    pass


@app.route('/qq_redirect/', methods=['POST', 'GET'])
def qq_login():
    """

    """
    pass


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
    res = redirect('/admin/login/')
    res.set_cookie(config.get('login_cookie_key'), '')
    return res
