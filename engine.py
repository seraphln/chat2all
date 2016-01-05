# coding=utf8
#

'''
项目的入口文件

请求执行流程：
    1. 先过过滤器，在filters.py里定义了哪些过滤器需要被执行
    2. 如果过滤器执行结果正常，那么会路由到不同的请求上并作出相应的处理以及返回
    3. 如果过滤器返回结果为一个异常，会根据这个异常的类型来返回不同的错误页面

'''


__AUTHOR__ = 'seraphwlq@gmail.com'
__VERSION__ = '0.1.0beta'


import flask

from app import app
from models import conn

from utils import exceptions
from utils.const import API_METHODS
from utils.contrib import make_s_response
from utils.contrib import make_error_response


@app.route('/api/<path:path>', methods=API_METHODS)
def backend(path):
    '''
        更改了之前的设计，现在由backend作为API请求的统一入口
        所有的API请求处理都在该函数内进行
    '''
    try:
        result = {}
        if isinstance(result, Exception):
            return make_error_response(result)
        elif isinstance(result, flask.wrappers.Response):
            return result
        else:
            return make_s_response(result)
    except Exception as e:
        return make_error_response(exceptions.ParamsErrorException())


@app.route('/', methods=['GET'])
def index():
    site_info = SiteInfo.objects.filter().first()
    cates = Category.objects.filter()
    products = Product.objects.filter().limit(50)
    for p in products:
        p.discount = p.discount.replace('(', '').replace(')', '')
    page_count = Product.objects.count()

    return render_template('index.html', site_info=site_info,
                           cates=cates, products=products,
                           page_count=page_count)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8355)
