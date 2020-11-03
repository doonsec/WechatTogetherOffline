# -*- coding: UTF-8 -*-
__author__ = 'Joynice'
from flask import jsonify


class HttpCode(object):
    ok = 200
    unautherror = 401
    paramserror = 400
    methoderror = 405
    servererror = 500


def restful_result(code, message, data, count):
    return jsonify({"code": code, "message": message, "count": count, "data": data or {}})


def success(message="", data=None, count=None):
    return restful_result(code=HttpCode.ok, message=message, data=data, count=count)


def layui_success(message="", data=None, count=None):
    return restful_result(code=0, message=message, data=data, count=count)


def unauth_error(message="认证失败", count=None):
    return restful_result(code=HttpCode.unautherror, message=message, data=None, count=count)


def params_error(message="", count=None):
    return restful_result(code=HttpCode.paramserror, message=message, data=None, count=count)


def server_error(message="", count=None):
    return restful_result(code=HttpCode.servererror, message=message or '服务器内部错误', data=None, count=count)


def method_error(message='', count=None):
    return restful_result(code=HttpCode.methoderror, message=message, data=None, count=count)
