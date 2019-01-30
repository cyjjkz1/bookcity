#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask_resuful import Api
from handlers.post_company_handler import PostCompanyHandler


bp_supply = Blueprint('bp_supply', __name__, url_prefix='/bookcity/v1/supply')
bp_post = Blueprint('bp_post', __name__, url_prefix='/bookcity/v1/post_company')

api_post = Api(bp_post)

api_post.add_resource(PostCompanyHandler, '/query', endpoint='supply_query')
api_post.add_resource(PostCompanyHandler, '/add', endpoint='supply_add')
