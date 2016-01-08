# coding=utf8
#

"""
cookie check relative functions
"""

import md5
import json
import base64
import random
from urllib2 import urlparse
from datetime import datetime
from datetime import timedelta

from utils.config import config


def decode_cookie(str_data):
    """ decode the cookie with an base64 algo """
    try:
        if not str_data.endswith('=='):
            str_data += '=='
        data = base64.b64decode(str_data)
        data = json.loads(data)
    except:
        data = {}
    return data


def encode_cookie(data):
    """ encode the cookie with an base64 algo """
    try:
        str_data = json.dumps(data)
        str_data = base64.b64encode(str_data)
        str_data = str_data.strip('=')
    except:
        str_data = ''
    return str_data


def build_sign(*args):
    """ build a self signed cookie for verify login state """
    skey = config.get('skey')

    tm = datetime.now().strftime('%Y%m%d')
    signed_args = list(args)
    signed_args.append(tm)
    signed_args.append(skey)
    s = '/'.join(signed_args).lower()
    sign = md5.md5(s).hexdigest()
    return sign


def build_sbuss(user, request):
    """ build the entire cookie info """

    user_info = {
        'id' : user['id'],
        'username' : user['username'],
        'level' : user['level'],
    }

    rand_str = config.get('rand_str')
    user_ip = request.environ.get('REMOTE_ADDR') or request.remote_addr
    user_agent = request.get_header('User-Agent', '')
    user_info['rand'] = ''.join(random.sample(rand_str, 8))
    user_info['sign'] = build_sign(user_info['id'], str(user_info['level']),
                                   user_ip, user_agent, user_info['rand'])
    return encode_cookie(user_info)


def verify_sbuss(sbuss, request):
    """ verify the given sbuss """
    if not sbuss or not request:
        return None
    user_info = decode_cookie(sbuss)
    if not user_info or not isinstance(user_info, dict):
        return None
    if any(['rand' not in user_info, 'id' not in user_info,
            'sign' not in user_info, 'level' not in user_info]):
        return None

    user_ip = request.environ.get('REMOTE_ADDR') or request.remote_addr
    user_agent = request.get_header('User-Agent', '')
    sign = build_sign(user_info['id'], str(user_info['level']),
                      user_ip, user_agent, user_info['rand'])
    if user_info['sign'] != sign:
        return None
    return user_info


def generate_csrf_token(request, tm=None):
    """ """
    if not hasattr(request, 'user'):
        request.user = {}
    uid = request.user.get('uid')
    user_agent = request.get_header('User-Agent', '').lower()
    host = request.get_header('Host', '').lower()
    tm = tm or datetime.datetime.now()
    tm_str = tm.strftime('%Y%m%d%H')
    s = '/%s/%s/%s/%s/'%(str(uid), user_agent, host, tm_str)
    s = s.lower()
    token = md5.md5(s).hexdigest()
    return token

def csrf_check(request, level):
    if level >= 1:
        referer_host = get_host(request.get_header('Referer'))
        host = request.get_header('Host', '').lower().strip()
        if referer_host != host:
            return False

    if level >= 2:
        csrf_seed = request.get_cookie('seed', '')
        csrf_token = request.get_header('X-CSRF-Token')
        new_token = generate_csrf_token(request)
        old_token = generate_csrf_token(request, datetime.now()-timedelta(hours=1))
        if not csrf_token:
            return False
        if csrf_token != csrf_seed and \
            csrf_token != new_token and \
            csrf_token != old_token:
            return False

    return True


def get_host(url):
    try:
        host = urlparse.urlparse(url).netloc.lower()
    except:
        host = ''
    return host.strip()
