# coding=utf8
#

import tornado.web


class IndexHandler(tornado.web.RequestHandler):
    ''' '''
    def get(self):
        self.render('templates/index.html')