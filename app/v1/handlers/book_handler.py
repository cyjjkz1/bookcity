#!/usr/bin/env python
# -*- coding:utf-8 -*-

import traceback
from flask import request, jsonify, abort
from flask import current_app as app
from ..models.book import Book
from ..models.supply import Supply, PostCompany
from ..models.category import AgeGroup, Function
from base_handler import BaseHandler, HandlerException
from data_packer import RequiredField, OptionalField, SelectorField, converter
from data_packer.checker import (
    ReChecker
)
from ..constant import RESP_CODE, RESP_ERR_MSG

BOOK_Name = RequiredField('name', checker=ReChecker(ur'([\u4e00-\u9fa5]{1,30})'))
BOOK_Price = RequiredField('price', converter=converter.TypeConverter(str), checker=ReChecker(r'[0-9]{1,4}'))
BOOK_Details = RequiredField('details', checker=ReChecker(ur'([\u4e00-\u9fa5]{10,100})'))
BOOK_Stock = RequiredField('stock', converter=converter.TypeConverter(str), checker=ReChecker(r'[0-9]{1,5}'))
BOOK_Choicest = RequiredField('choicest', converter=converter.TypeConverter(str), checker=ReChecker(r'[0-1]{1}'))


OPTION_id = OptionalField(src_name='id',
                          converter=converter.TypeConverter(str),
                          checker=ReChecker(r'[0-9]{1,}'))
OPTION_Name = OptionalField('name', checker=ReChecker(ur'([\u4e00-\u9fa5]{1,30})'))
OPTION_Price = OptionalField('price', converter=converter.TypeConverter(str), checker=ReChecker(r'[0-9]{1,4}'))
OPTION_Details = OptionalField('details', checker=ReChecker(ur'([\u4e00-\u9fa5]{10,100})'))
OPTION_Stock = OptionalField('stock', converter=converter.TypeConverter(str), checker=ReChecker(r'[0-9]{1,5}'))
OPTION_Choicest = OptionalField('choicest', converter=converter.TypeConverter(str), checker=ReChecker(r'[0-1]{1}'))


RELATION_AGE_id = RequiredField(src_name='age_id',
                                converter=converter.TypeConverter(str),
                                checker=ReChecker(r'[0-9]{1,}'))
RELATION_FUNC_id = RequiredField(src_name='func_id',
                                 converter=converter.TypeConverter(str),
                                 checker=ReChecker(r'[0-9]{1,}'))
RELATION_SUPPLY_id = RequiredField(src_name='supply_id',
                                   converter=converter.TypeConverter(str),
                                   checker=ReChecker(r'[0-9]{1,}'))


class BookHandler(BaseHandler):
    POST_FIELDS = [
        BOOK_Name, BOOK_Price, BOOK_Details, BOOK_Stock,
        BOOK_Choicest, RELATION_AGE_id, RELATION_FUNC_id,
        RELATION_SUPPLY_id
    ]
    GET_FIELDS = [SelectorField(
        fields=[
            OPTION_id,
            OPTION_Name,
            OPTION_Details,
            OPTION_Stock,
            OPTION_Choicest
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
                book = Book.query.filter_by(**params).first()
                if book:
                    return book.model_to_dict(query_img=True, query_supply=True, query_category=True)
                else:
                    raise HandlerException(respcd=RESP_CODE.DB_ERROR, respmsg=RESP_ERR_MSG.get(RESP_CODE.DB_ERROR))
            elif request.method == 'POST':
                # 插入
                book = Book(name=params['name'],
                            price=params['price'],
                            details=params['details'],
                            stock=params['stock'],
                            choicest=params['stock'],
                            )
                # 建立关系
                supply = Supply.query.filter_by(id=params['supply_id']).first()
                age = AgeGroup.query.filter_by(id=params['age_id']).first()
                func = Function.query.filter_by(id=params['func_id']).first()
                if supply is None:
                    app.logger.info('Can not find supply with id = {}'.format(params['supply_id']))
                    raise HandlerException(respcd=RESP_CODE.DB_ERROR, respmsg=RESP_ERR_MSG.get(RESP_CODE.DB_ERROR))
                if age is None:
                    app.logger.info('Can not find age_group with id = {}'.format(params['age_id']))
                    raise HandlerException(respcd=RESP_CODE.DB_ERROR, respmsg=RESP_ERR_MSG.get(RESP_CODE.DB_ERROR))
                if func is None:
                    app.logger.info('Can not find function with id = {}'.format(params['func_id']))
                    raise HandlerException(respcd=RESP_CODE.DB_ERROR, respmsg=RESP_ERR_MSG.get(RESP_CODE.DB_ERROR))
                book.supply_set = supply
                book.age_set = age
                book.function_set = func
                book.save()
                if book.id:
                    return {'book_id': book.id}
                else:
                    raise HandlerException(respcd=RESP_CODE.DB_ERROR, respmsg=RESP_ERR_MSG.get(RESP_CODE.DB_ERROR))
            else:
                abort(404)
        except BaseException as e:
            raise e