# coding=utf8
#

"""

请求流程如下：

请求执行流程：
    1. 先过过滤器，在filters.py里定义了哪些过滤器需要被执行
    2. 如果过滤器执行结果正常，那么会路由到不同的请求上并作出相应的处理以及返回
    3. 如果过滤器返回结果为一个异常，会根据这个异常的类型来返回不同的错误页面

"""

import os
import tornado.web
import tornado.ioloop

from models import conn
from utils.config import config
from utils.logger import getLogger

from views.IndexHandler import IndexHandler
from views.LoginHandler import QQLoginHandler


logger = getLogger("chat2all.engine")


def make_app():
    """ make an app instance to start the server """
    settings = {'static_path': os.path.join(os.path.dirname(__file__),
                'templates')}

    app = tornado.web.Application([(r"/qq_redirect/", QQLoginHandler,
                                    r"/", IndexHandler)],
                                    **settings)
    return app


if __name__ == "__main__":

    # 1. generate app instance
    app = make_app()

    # 2. Make Tornado app listen on port 8080
    serve_port = int(config.get('server_port'))
    app.listen(serve_port)
    print "Listening at %s" % serve_port

    # 3. Start IOLoop
    tornado.ioloop.IOLoop.instance().start()
