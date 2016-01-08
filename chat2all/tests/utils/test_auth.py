# coding=utf8
#


import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.curdir)))

import unittest
from datetime import datetime

from utils.auth import encode_cookie
from utils.auth import decode_cookie
from utils.auth import build_sbuss


class TestDecodeCookie(unittest.TestCase):

    def test_normal_cookie(self):
        """ """
        s = 'eyJhIjogMX0'
        ret = decode_cookie(s)
        self.assertEqual({'a': 1}, ret)

    def test_fake_cookie(self):
        """ """
        s = ""
        ret = decode_cookie(s)
        self.assertEqual({}, ret)


class TestEncodeCookie(unittest.TestCase):

    def test_jsonable_value(self):
        """ """
        data = {'a': 1}
        ret = encode_cookie(data)
        self.assertEqual('eyJhIjogMX0', ret)

    def test_non_jsonable_value(self):
        """ """
        data = {'d': datetime(2015, 12, 31)}
        ret = encode_cookie(data)
        self.assertEqual('', '')


class ContextRequest(object):
    """
        self defined request object for unittest cases
    """

    def __init__(self):
        self.environ = {'REMOTE_ADDR': '127.0.0.1'}
        self.headers = {}

    def get_header(self, key, default_value):
        return self.headers.get(key, default_value)


class TestBuildSbuss(unittest.TestCase):

    def setUp(self):
        """ prepare the test data """
        self.user = {'id': '1', 'username': 'foo', 'level': '10'}
        self.request = ContextRequest()

    def test_normal_value(self):
        """ """

        ret = build_sbuss(self.user, self.request)
        r = decode_cookie(ret)
        result = {'id': r.get('id'),
                  'username': r.get('username'),
                  'level': r.get('level')}
        self.assertEqual(result, self.user)


if __name__ == '__main__':
    unittest.main()
