#!/usr/bin/env python
# -*- coding:utf-8 -*-

from data-packer import RequiredField, OptionalField
from data-packer.checker import (
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

    PERMISSION_ERROR = '4000'
    USER_NOT_LOGIN = '4001'
    AUTH_FAIL_ERROR = '4002'

RESP_ERR_MSG = {
    RESP_CODE.SUCCESS: '成功',

    RESP_CODE.SYSTEM_ERROR: '系统错误',
    RESP_CODE.INNER_SERVICE_ERROR: '内部服务错误',
    RESP_CODE.OUTTER_SERVICE_ERROR: '外部服务错误',

    RESP_CODE.PARAM_ERROR: '请求参数错误',
    RESP_CODE.DB_ERROR: 'DB错误'

    RESP_CODE.USER_NOT_LOGIN: '用户未登陆'
}

FIELD_username = RequiredField('username', checker=ReChecker(r'[a-zA-Z0-9]{1,60}'))
FIELD_password = RequiredField('password', checker=Rechecker(r'[a-zA-Z0-9]{1,20}'))

