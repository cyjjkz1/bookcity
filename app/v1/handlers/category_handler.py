#!/usr/bin/env python
# -*- coding:utf-8 -*-

import traceback
from flask import request, jsonify, abort
from flask import current_app as app
from ..models.category import AgeGroup, Function
from base_handler import BaseHandler, HandlerException
from data_packer import RequiredField, OptionalField, SelectorField, converter
from data_packer.checker import (
    ReChecker
)
from ..constant import RESP_CODE, RESP_ERR_MSG
from app import db


AGE_Name = RequiredField('age_name', checker=ReChecker(ur'([~0-9\u4e00-\u9fa5]{2,10})'))
FUNCTION_Name = RequiredField('func_name', checker=ReChecker(ur'([\u4e00-\u9fa5]{2,10})'))

OPTION_id = OptionalField(src_name='supply_id',
                          dst_name='id',
                          converter=converter.TypeConverter(str),
                          checker=ReChecker(r'[0-9]{1,}'))

OPTION_Name = OptionalField(src_name='name',
                            dst_name='name',
                            checker=ReChecker(ur'([\u4e00-\u9fa5]{2,30})'))

RELATION_AGE_id = RequiredField(src_name='age_id',
                                converter=converter.TypeConverter(str),
                                checker=ReChecker(r'[0-9]{1,}'))
RELATION_FUNC_id = RequiredField(src_name='func_id',
                                 converter=converter.TypeConverter(str),
                                 checker=ReChecker(r'[0-9]{1,}'))


class AgeGroupHandler(BaseHandler):
    POST_FIELDS = [
        AGE_Name
    ]
    GET_FIELDS = [SelectorField(
        fields=[
            OPTION_id,
            OPTION_Name
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
                age = AgeGroup.query.filter_by(**params).first()
                if age:
                    return age.model_to_dict(query_relation=True)
                else:
                    raise HandlerException(respcd=RESP_CODE.DB_ERROR, respmsg=RESP_ERR_MSG.get(RESP_CODE.DB_ERROR))
            elif request.method == 'POST':
                # 插入
                age = AgeGroup(name=params['age_name'])
                age.save()
                if age.id:
                    return {'age_id': age.id}
                else:
                    raise HandlerException(respcd=RESP_CODE.DB_ERROR, respmsg=RESP_ERR_MSG.get(RESP_CODE.DB_ERROR))
            else:
                abort(404)
        except BaseException as e:
            db.session.rollback()
            raise e


class FunctionHandler(BaseHandler):
    POST_FIELDS = [
        FUNCTION_Name
    ]
    GET_FIELDS = [SelectorField(
        fields=[
            OPTION_id,
            OPTION_Name
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
        app.logger.info(
            'func=parse_request_params | parse_type={} | parse_params = {}'.format(type(params), params))
        try:
            if request.method == 'GET':
                func = Function.query.filter_by(**params).first()
                if func:
                    return func.model_to_dict(query_relation=False)
                else:
                    raise HandlerException(respcd=RESP_CODE.DB_ERROR, respmsg=RESP_ERR_MSG.get(RESP_CODE.DB_ERROR))
            elif request.method == 'POST':
                # 插入
                func = Function(name=params['func_name'])
                func.save()
                if func.id:
                    return {'func_id': func.id}
                else:
                    raise HandlerException(respcd=RESP_CODE.DB_ERROR, respmsg=RESP_ERR_MSG.get(RESP_CODE.DB_ERROR))
            else:
                abort(404)
        except BaseException as e:
            db.session.rollback()
            raise e


class AgeGroupAddFuncHandler(BaseHandler):
    POST_FIELDS = [
        RELATION_AGE_id, RELATION_FUNC_id
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
            age = AgeGroup.query.filter_by(id=params['age_id']).first()
            if age is None:
                raise HandlerException(respcd=RESP_CODE.DB_QUERY_NOT_FOUND,
                                       respmsg=RESP_ERR_MSG.get(RESP_CODE.DB_QUERY_NOT_FOUND) + ' age_id {}'.format(
                                           params['age_id']))
            app.logger.info('<AgeGroup>DB query result: {}'.format(age.model_to_dict(query_relation=False)))
            func = Function.query.filter_by(id=params['func_id']).first()
            if func is None:
                raise HandlerException(respcd=RESP_CODE.DB_ERROR,
                                       respmsg=RESP_ERR_MSG.get(RESP_CODE.DB_QUERY_NOT_FOUND) + ' func_id {}'.format(
                                           params['func_id']))
            app.logger.info('<Function>DB query result: {}'.format(func.model_to_dict(query_relation=False)))

            age.functions.append(func)
            age.save()
            return self.request_finish(RESP_CODE.SUCCESS, RESP_ERR_MSG.get(RESP_CODE.SUCCESS, ''))
        except BaseException as e:
            db.session.rollback()
            raise e


class CategoryQueryHandler(BaseHandler):
    def get(self):
        get_ret = self.handle(())
        if get_ret:
            return jsonify(get_ret)

    def _handle(self, *args, **kwargs):
        """
        无需查询参数, 要查询一个年龄段下面的分类直接按照年龄段查询
        :param args:
        :param kwargs:
        :return:
        """
        try:
            age_gp = AgeGroup.query.filter().all()
            ag_arr = []
            for ag in age_gp:
                ag_arr.append(ag.model_to_dict(query_relation=True))
            return self.request_finish(RESP_CODE.SUCCESS, RESP_ERR_MSG.get(RESP_CODE.SUCCESS, ''), data=ag_arr)
        except BaseException as e:
            raise e
