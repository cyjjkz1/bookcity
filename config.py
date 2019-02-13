#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))

# 数据库配置
USERNAME = 'manager'
PASSWORD = 'TianTian1121@@'
HOSTNAME = 'localhost'
DATABASE = 'bookcity'


class Config:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS =True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(USERNAME, PASSWORD, HOSTNAME, DATABASE)
    LOG_PATH = os.path.join(basedir, 'logs')
    LOG_PATH_INFO = os.path.join(LOG_PATH, 'bookcity.log')
    LOG_FILE_MAX_BYTES = 100 * 1024 * 1024

    # 轮转数量10个
    LOG_FILE_BACKUP_COUNT = 10


class DevelopmentConfig(Config):
    pass


class TestingConfig(Config):
    pass


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
