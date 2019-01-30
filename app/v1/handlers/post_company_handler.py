#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import request
from ..models.supply import PostCompany
from base_handler import BaseHandler, HandlerException
from data_packer import RequiredField, OptionalField
from data_packer.checker import (
    ReChecker, TypeChecker
)
from ..constant import RESP_CODE, RESP_ERR_MSG

POST_Name = RequiredField('post_name', checker=ReChecker(r'[\u4e00-\u9fa5]{2, 10}'))
POST_Price = RequiredField('post_price', checker=ReChecker(r'[0-9]{1,4}'))
POST_id = RequiredField('post_id', checker=ReChecker(r'[0-9]{1,}'))


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
        if request.method == 'GET':
            # 查询
            post = PostCompany.query.filter_by(id=params['post_id']).first()
            return post.model_to_dict(query_relation=False)
        elif request.method == 'POST':
            # 插入
            post = PostCompany(name=params['post_name'], price=params['post_price'])
            return self.request_finish(RESP_CODE.SUCCESS, resperr=RESP_ERR_MSG.get(RESP_CODE.SUCCESS, ''), post_id=post.id)
        else:
            raise BaseException

