#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask_restful import Api
from handlers.post_company_handler import PostCompanyHandler
from handlers.supply_handler import SupplyHandler, SupplySelectHandler


bp_post = Blueprint('bp_post', __name__, url_prefix='/bookcity/v1/post_company')

api_post = Api(bp_post)

api_post.add_resource(PostCompanyHandler, '/query', endpoint='post_query')

api_post.add_resource(PostCompanyHandler, '/add', endpoint='post_add')


bp_supply = Blueprint('bp_supply', __name__, url_prefix='/bookcity/v1/supply')

api_supply = Api(bp_supply)

api_supply.add_resource(SupplyHandler, '/query', endpoint='supply_query')

api_supply.add_resource(SupplyHandler, '/add', endpoint='supply_add')

api_supply.add_resource(SupplyHandler, '/add_post', endpoint='supply_add_post')