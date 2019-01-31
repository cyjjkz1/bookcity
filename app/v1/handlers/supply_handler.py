#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import request,jsonify
from flask import current_app as app
from ..models.supply import Supply
from base_handler import BaseHandler, HandlerException
from data_packer import RequiredField, OptionalField, SelectorField, converter
from data_packer.checker import (
    ReChecker
)
from ..constant import RESP_CODE, RESP_ERR_MSG

# id = db.Column(db.Integer, primary_key=True, autoincrement=True)
# name = db.Column(db.String(30), nullable=False)
# mobile = db.Column(db.String(11), nullable=False)
# address = db.Column(db.String(50), nullable=False)

SUPPLY_Name = RequiredField('supply_name', checker=ReChecker(ur'([\u4e00-\u9fa5]{2,30})'))
SUPPLY_Mobile = RequiredField('supply_mobile', checker=ReChecker(r'1[0-9]{10}'))
SUPPLY_Address = RequiredField('supply_address', checker=ReChecker(ur'([a-z0-9\u4e00-\u9fa5]{2,50})'))

OPTION_SUPPLY_id = OptionalField('supply_id', converter=converter.TypeConverter(str), checker=ReChecker(r'[0-9]{1,}'))
OPTION_SUPPLY_Name = OptionalField('supply_name', checker=ReChecker(ur'([\u4e00-\u9fa5]{2,30})'))
OPTION_SUPPLY_Mobile = OptionalField('supply_mobile', checker=ReChecker(r'1[0-9]{10}'))
OPTION_SUPPLY_Address = OptionalField('supply_address', checker=ReChecker(ur'([a-z0-9\u4e00-\u9fa5]{2,30})'))


class SupplyHandler(BaseHandler):
    POST_FIELDS = [
        SUPPLY_Name, SUPPLY_Mobile, SUPPLY_Address
    ]
    GET_FIELDS = [SelectorField(
        fields=[
            OPTION_SUPPLY_Name,
            OPTION_SUPPLY_Mobile,
            OPTION_SUPPLY_Address,
        ],
        at_least=1,
    )]

    def get(self):
        return jsonify(self.handle())

    def post(self):
        return jsonify(self.handle())

    def _handle(self, *args, **kwargs):
        params = self.parse_request_params()
        app.logger.info('func=parse_request_params | parse_params = '.format(params))
        if request.method == 'GET':
            pass
        elif request.method == 'POST':
            # 插入
            supply = Supply(name=params['supply_name'], mobile=params['supply_mobile'], address=params['supply_address'])
            supply.save()
            if supply.id:
                return {'supply_id': supply.id}
            else:
                raise HandlerException(respcd=RESP_CODE.DB_ERROR, respmsg=RESP_ERR_MSG.get(RESP_CODE.DB_ERROR))
        else:
            raise BaseException
