#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask_restful import Api
from handlers.post_company_handler import PostCompanyHandler
from handlers.supply_handler import SupplyHandler, SupplySelectHandler
from handlers.category_handler import AgeGroupHandler, FunctionHandler, AgeGroupAddFuncHandler, CategoryQueryHandler
from handlers.book_handler import BookHandler

# 快递公司蓝图
bp_post = Blueprint('bp_post', __name__, url_prefix='/bookcity/v1/post_company')

api_post = Api(bp_post)

api_post.add_resource(PostCompanyHandler, '/query', endpoint='post_query')

api_post.add_resource(PostCompanyHandler, '/add', endpoint='post_add')


# 供应商蓝图
bp_supply = Blueprint('bp_supply', __name__, url_prefix='/bookcity/v1/supply')

api_supply = Api(bp_supply)

api_supply.add_resource(SupplyHandler, '/query', endpoint='supply_query')

api_supply.add_resource(SupplyHandler, '/add', endpoint='supply_add')

api_supply.add_resource(SupplySelectHandler, '/add_post_company', endpoint='supply_add_post')


# 分类蓝图
bp_category = Blueprint('bp_category', __name__, url_prefix='/bookcity/v1/category')

api_category = Api(bp_category)

api_category.add_resource(AgeGroupHandler, '/age_group/query', endpoint='age_group_query')

api_category.add_resource(AgeGroupHandler, '/age_group/add', endpoint='age_group_add')

api_category.add_resource(AgeGroupAddFuncHandler, '/age_group/add_function', endpoint='age_add_func')

api_category.add_resource(FunctionHandler, '/function/query', endpoint='func_query')

api_category.add_resource(FunctionHandler, '/function/add', endpoint='func_add')

api_category.add_resource(CategoryQueryHandler, '/query', endpoint='category_query')

# 书籍蓝图
bp_book = Blueprint('bp_book', __name__, url_prefix='/bookcity/v1/book')

api_book = Api(bp_book)

api_book.add_resource(BookHandler, '/query', endpoint='book_query')

api_book.add_resource(BookHandler, '/add', endpoint='book_add')