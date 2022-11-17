#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/14 14:39
# @Author  : 冉勇
# @Site    :
# @File    : logger.py
# @Software: PyCharm
# @desc    : 日志相关工具
import inspect
import os
from loguru import logger
from app.config import settings


class Log(object):
    business = None

    def __init__(self, name="app"):
        """
        :param name: 业务名称
        """
        if not os.path.exists(settings.log_dir):
            os.mkdir(settings.log_dir)
        self.business = name

    def info(self, msg: str):
        """
        普通日志
        :param msg:
        :return:
        """
        file_name, line, func, _, _ = inspect.getframeinfo(inspect.currentframe().f_back)
        logger.bind(name=settings.log_info, func=func, line=line, business=self.business,
                    filename=file_name).info(msg)

    def error(self, msg: str):
        """
        错误日志
        :param msg:
        :return:
        """
        file_name, line, func, _, = inspect.getframeinfo(inspect.currentframe().f_back)
        logger.bind(name=settings.log_error, func=func, line=line, business=self.business, filename=file_name).error(
            msg)

    def warning(self, msg: str):
        """
        警告日志
        :param msg:
        :return:
        """
        file_name, line, func, _, _ = inspect.getframeinfo(inspect.currentframe().f_back)
        logger.bind(name=settings.log_warning, func=func, line=line, business=self.business,
                    filename=file_name).warning(
            msg)

    def debug(self, msg: str):
        """
        debug日志
        :param msg:
        :return:
        """
        file_name, line, func, _, _ = inspect.getframeinfo(inspect.currentframe().f_back)
        logger.bind(name=settings.log_debug, func=func, line=line, business=self.business,
                    filename=file_name).debug(msg)

    def exception(self, msg: str):
        """
        其他日志
        :param msg:
        :return:
        """
        file_name, line, func, _, _ = inspect.getframeinfo(inspect.currentframe().f_back)
        logger.bind(name=settings.log_exception, func=func, line=line, business=self.business,
                    filename=file_name).exception(msg)
