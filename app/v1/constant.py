#!/usr/bin/env python
# -*- coding:utf-8 -*-

from data_packer import RequiredField, OptionalField
from data_packer.checker import (
    ReChecker, LenChecker, TypeChecker
)


class RESP_CODE(object):
    SUCCESS = '0000'

    SYSTEM_ERROR = '1000'
    INNER_SERVICE_ERROR = '1001'
    OUTTER_SERVICE_ERROR = '1002'

    PARAM_ERROR = '2000'
    INVALID_REQUEST = '2001'
    DATA_ERROR = '2002'

    DB_ERROR = '3000'
    DB_QUERY_NOT_FOUND = '3001'
    MEHTOD_NOT_FOUND = '4000'

    PERMISSION_ERROR = '6000'
    USER_NOT_LOGIN = '6001'
    AUTH_FAIL_ERROR = '6002'


RESP_ERR_MSG = {
    RESP_CODE.SUCCESS: '成功',

    RESP_CODE.SYSTEM_ERROR: '系统错误',
    RESP_CODE.INNER_SERVICE_ERROR: '内部服务错误',
    RESP_CODE.OUTTER_SERVICE_ERROR: '外部服务错误',

    RESP_CODE.PARAM_ERROR: '请求参数错误',
    RESP_CODE.DB_ERROR: 'DB错误',
    RESP_CODE.DB_QUERY_NOT_FOUND: 'DB 查询无结果',

    RESP_CODE.USER_NOT_LOGIN: '用户未登陆',
    RESP_CODE.MEHTOD_NOT_FOUND: '暂未支持该请求方法'
}


