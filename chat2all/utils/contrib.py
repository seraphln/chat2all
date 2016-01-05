#!/usr/bin/env python
# coding=utf8
#


"""

"""

import json
from flask import Response


def make_s_response(result):
    ''' 当请求一个API成功时，
        会调用该函数并返回包含正常数据的json对象
    '''
    response = Response()
    response.status = '200 OK'
    ret = {
        "status": "ok",
        "errors":[],
        "messages":[],
        "result": {}
    }
    if result is not None:
        ret['result'] = result

    response.set_data(json.dumps(ret))
    return response


def make_error_response(e):
    ''' 当请求一个API失败时，
        会调用该函数返回一个包含错误信息的json对象
    '''
    response = Response()
    response.status = e.http_status
    ret = {
        "status": "error",
        "errors":[],
        "messages":[],
        "result": {}
    }
    error = {}
    error['code'] = e.code
    error['message'] = e.message
    ret['errors'].append(error)
    response.set_data(json.dumps(ret))
    return response

