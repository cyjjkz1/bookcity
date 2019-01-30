#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)

    # 应用配置
    app.config.from_object(config[config_name])
    app.config['JSON_AS_ASCII'] = False

    # 配置数据库
    db.init_app(app)

    # 配置蓝图
    from v1.urls import bp_post
    app.register_blueprint(bp_post)

    # 配置日志
    import logging
    from logging.handlers import RotatingFileHandler
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(process)d %(thread)d '
        '%(pathname)s %(lineno)s %(message)s')

    file_handler_info = RotatingFileHandler(filename=config[config_name].LOG_PATH_INFO)
    file_handler_info.setFormatter(formatter)
    app.logger.addHandler(file_handler_info)
    app.logger.setLevel(logging.INFO)

    return app

