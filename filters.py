# coding=utf8
#

'''
包括所有的过滤器，
请求参数检查过滤器以及用户权限过滤器
'''

from flask import request

from utils.contrib import parse_params


class BaseFilters(object):
    ''' 过滤器的基类，其它过滤器都需要继承自本基类 '''

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def process_request(self):
        raise NotImplementedError("You should implement this func in sub class")


class PermissionFilters(BaseFilters):
    ''' 权限相关的过滤器，如果用户没有访问某个app的权限，那么会返回一个403 '''
    def process_request(self):
        return True


class ParamsFilters(BaseFilters):
    ''' 参数相关的过滤器，会检查参数是否合法并格式化参数 '''
    def process_request(self, request):
        parse_params(request)   # 首先，处理请求参数
        return True


filter_tuple = [ParamsFilters,
                PermissionFilters]


def process_filters(request):
    for cur_filter in filter_tuple:
        cur_result = cur_filter().process_request(request)
        if isinstance(cur_result, Exception):
            return cur_result
        else:
            return None


