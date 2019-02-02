#!/usr/bin/env python
# -*- coding:utf-8 -*-
import traceback
from flask import request,jsonify, abort
from flask import current_app as app
from ..models.supply import Supply, PostCompany
from base_handler import BaseHandler, HandlerException
from data_packer import RequiredField, OptionalField, SelectorField, converter
from data_packer.checker import (
    ReChecker
)
from ..constant import RESP_CODE, RESP_ERR_MSG
from app import db

SUPPLY_Name = RequiredField('supply_name', checker=ReChecker(ur'([\u4e00-\u9fa5]{2,30})'))
SUPPLY_Mobile = RequiredField('supply_mobile', checker=ReChecker(r'1[0-9]{10}'))
SUPPLY_Address = RequiredField('supply_address', checker=ReChecker(ur'([a-z0-9\u4e00-\u9fa5]{2,50})'))

OPTION_SUPPLY_id = OptionalField(src_name='supply_id',
                                 dst_name='id',
                                 converter=converter.TypeConverter(str),
                                 checker=ReChecker(r'[0-9]{1,}'))
OPTION_SUPPLY_Name = OptionalField(src_name='supply_name',
                                   dst_name='name',
                                   checker=ReChecker(ur'([\u4e00-\u9fa5]{2,30})'))
OPTION_SUPPLY_Mobile = OptionalField(src_name='supply_mobile',
                                     dst_name='mobile',
                                     checker=ReChecker(r'1[0-9]{10}'))
OPTION_SUPPLY_Address = OptionalField(src_name='supply_address',
                                      dst_name='address',
                                      checker=ReChecker(ur'([a-z0-9\u4e00-\u9fa5]{2,30})'))

RELATION_SUPPLY_id = RequiredField(src_name='supply_id',
                                   converter=converter.TypeConverter(str),
                                   checker=ReChecker(r'[0-9]{1,}'))
RELATION_POST_id = RequiredField(src_name='post_id',
                                 converter=converter.TypeConverter(str),
                                 checker=ReChecker(r'[0-9]{1,}'))


class SupplyHandler(BaseHandler):
    POST_FIELDS = [
        SUPPLY_Name, SUPPLY_Mobile, SUPPLY_Address
    ]
    GET_FIELDS = [SelectorField(
        fields=[
            OPTION_SUPPLY_id,
            OPTION_SUPPLY_Name,
            OPTION_SUPPLY_Mobile,
            OPTION_SUPPLY_Address,
        ],
        at_least=1,
    )]

    def get(self):
        get_ret = self.handle(())
        if get_ret:
            return jsonify(get_ret)

    def post(self):
        post_ret = self.handle(())
        if post_ret:
            return jsonify(post_ret)

    def _handle(self, *args, **kwargs):
        params = self.parse_request_params()
        if params is None:
            return app.logger.info('func=parse_request_params | 没有正确解析参数')
        app.logger.info('func=parse_request_params | parse_type={} | parse_params = {}'.format(type(params), params))
        try:
            if request.method == 'GET':
                supply = Supply.query.filter_by(**params).first()
                if supply:
                    return supply.model_to_dict(query_relation=True)
                else:
                    raise HandlerException(respcd=RESP_CODE.DB_ERROR, respmsg=RESP_ERR_MSG.get(RESP_CODE.DB_ERROR))
            elif request.method == 'POST':
                # 插入
                supply = Supply(name=params['supply_name'], mobile=params['supply_mobile'], address=params['supply_address'])
                supply.save()
                if supply.id:
                    return {'supply_id': supply.id}
                else:
                    raise HandlerException(respcd=RESP_CODE.DB_ERROR, respmsg=RESP_ERR_MSG.get(RESP_CODE.DB_ERROR))
            else:
                abort(404)
        except BaseException as e:
            db.session.rollback()
            raise e


class SupplySelectHandler(BaseHandler):
    POST_FIELDS = [
        RELATION_SUPPLY_id, RELATION_POST_id
    ]

    def post(self):
        post_ret = self.handle(())
        if post_ret:
            return jsonify(post_ret)

    def _handle(self, *args, **kwargs):
        params = self.parse_request_params()
        if params is None:
            return app.logger.info('func=parse_request_params | 没有正确解析参数')
        app.logger.info('func=parse_request_params | parse_type={} | parse_params = {}'.format(type(params), params))
        try:
            supply = Supply.query.filter_by(id=params['supply_id']).first()
            if supply is None:
                raise HandlerException(respcd=RESP_CODE.DB_QUERY_NOT_FOUND,
                                       respmsg=RESP_ERR_MSG.get(RESP_CODE.DB_QUERY_NOT_FOUND) + ' supply_id {}'.format(params['supply_id']))
            app.logger.info('<Supply>DB query result: {}'.format(supply.model_to_dict(query_relation=False)))
            post = PostCompany.query.filter_by(id=params['post_id']).first()
            if post is None:
                raise HandlerException(respcd=RESP_CODE.DB_ERROR,
                                       respmsg=RESP_ERR_MSG.get(RESP_CODE.DB_QUERY_NOT_FOUND) + ' supply_id {}'.format(params['post_id']))
            app.logger.info('<PostCompany>DB query result: {}'.format(post.model_to_dict(query_relation=False)))

            post.supply_set.append(supply)
            supply.save()
            return self.request_finish(RESP_CODE.SUCCESS, RESP_ERR_MSG.get(RESP_CODE.SUCCESS, ''))
        except BaseException as e:
            db.session.rollback()
            raise e
