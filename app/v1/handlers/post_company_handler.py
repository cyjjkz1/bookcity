#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import request
from flask import current_app as app
from ..models.supply import PostCompany
from base_handler import BaseHandler, HandlerException
from data_packer import RequiredField, converter
from data_packer.checker import (
    ReChecker
)
from ..constant import RESP_CODE, RESP_ERR_MSG

POST_Name = RequiredField('post_name', checker=ReChecker(ur'([\u4e00-\u9fa5]{2,30})'))
POST_Price = RequiredField('post_price', checker=ReChecker(r'[0-9]{1,4}'))
POST_id = RequiredField('post_id', converter=converter.TypeConverter(str), checker=ReChecker(r'[0-9]{1,}'))


class PostCompanyHandler(BaseHandler):
    POST_FIELDS = [
        POST_Name, POST_Price
    ]
    GET_FIELDS = [
        POST_id
    ]

    def get(self):
        self.handle()

    def post(self):
        self.handle()

    def _handle(self, *args, **kwargs):
        params = self.parse_request_params()
        app.logger.info('func=parse_request_params | ret_params = '.format(params))
        if request.method == 'GET':
            # 查询
            post = PostCompany.query.filter_by(id=params['post_id']).first()
            if post:
                return post.model_to_dict(query_relation=False)
            else:
                raise HandlerException(respcd=RESP_CODE.DB_ERROR, respmsg=RESP_ERR_MSG.get(RESP_CODE.DB_ERROR))
        elif request.method == 'POST':
            # 插入
            app
            post = PostCompany(name=params['post_name'], price=params['post_price'])
            post.save()
            if post.id:
                return {'post_id': post.id}
            else:
                raise HandlerException(respcd=RESP_CODE.DB_ERROR, respmsg=RESP_ERR_MSG.get(RESP_CODE.DB_ERROR))
        else:
            raise BaseException
