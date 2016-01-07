#!/usr/bin/env python
# coding=utf8
#


"""

"""

import json


def make_success_response(result):
    ''' 当请求一个API成功时，
        会调用该函数并返回包含正常数据的json对象
    '''
    ret = {
        "status": "ok",
        "errors":[],
        "messages":[],
        "result": {}
    }
    if result is not None:
        ret['result'] = result

    return ret


def make_error_response(e):
    ''' 当请求一个API失败时，
        会调用该函数返回一个包含错误信息的json对象
    '''
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

    return ret
