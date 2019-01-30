#!/usr/bin/env python
# -*- coding:utf-8 -*-
import traceback
from data_packer import DataPacker, err
from data_packer.container import DictContainer
from flask import current_app as app
from flask_restful import Resource
from flask import request, jsonify
from app.v1.constant import RESP_CODE, RESP_ERR_MSG
#from app.v1.constant import (
#    FIELD_username, FIELD_password
#)


class HandlerException(Exception):
    def __init__(self, repcd, respmsg=''):
        self.respcd = respcd
        self.respmsg = respmsg


class BaseHandler(Resource):
    REQ_FIELDS = []

    def __init__(self, *args, **kwargs):
        pass

    def _handle(self, *args, **kwargs):
        raise NotImplementedError()

    def parse_request_params(self, check_param=True, error_message={}):
        if request.method == 'GET':

        elif request.methos == 'POST':
            pass
        else
            raise

    def check_params(self, params, error_message):
        ret = {}
        dp = DataPacker(self.REQ_FIELDS)
        try:
            dp.run(
                DataContainer(params),
                DataContainer(ret)
            )
        except err.DataPackerCheckError as e:
            app.logger.warn(trackback.format_exc())
            resperr = RESP_ERR_MSG.get(RESP_CODE.PARAM_ERROR, '') + ' : {}'.format(e.src_name)
            return self.request_finish(respcd=RESP_CODE.PARAM_ERROR, resperr=resperr)
        except err.DataPackerSrcKeyNotFoundError as e:
            app.logger.warn(trackback.format_exc())
            resperr = RESP_ERR_MSG.get(RESP_CODE.PARAM_ERROR, '') + ' 缺少参数: {}'.format(e.src_name)
        except err.DataPackerError as e:
            pass
        finally:
            pass
        return ret

    def request_finish(self, respcd, respmsg='', resperr='', **kwargs):
        if not resperr:
            resperr = RESP_ERR_MSG.get(respcd, '')
        resp = {
            'respcd': respcd,
            'respmsg': respmsg,
            'resperr': resperr
        }
        resp.update(kwargs)
        app.logger.info('Response %s', resp)
        resp = jsonif(resp)


