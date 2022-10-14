#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/10 15:54
# @Author  : 冉勇
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
# @desc    :
import os
import sys
import logging
from fastapi import FastAPI, Request, status
from loguru import logger
from starlette.responses import JSONResponse
from .config import settings
from pprint import pformat
from loguru._defaults import LOGURU_FORMAT
from starlette.middleware.cors import CORSMiddleware
from .utils import logger
from starlette.middleware.errors import ServerErrorMiddleware

app = FastAPI()

# 配置日志格式
INFO_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> " \
              "| <level>{level: <8}</level> | <cyan>文件: {extra[filename]}</cyan> " \
              "| 模块: <cyan>{extra[business]}</cyan> | 方法: <cyan>{extra[func]}</cyan> " \
              "| <cyan>行数: {extra[line]}</cyan> | - <level>{message}</level>"

ERROR_FORMAT = "<red>{time:YYYY-MM-DD HH:mm:ss.SSS}</red> " \
               "| <level>{level: <8}</level> | <cyan>文件: {extra[filename]}</cyan> " \
               "| 模块: <cyan>{extra[business]}</cyan> | 方法: <cyan>{extra[func]}</cyan> " \
               "| <cyan>行数: {extra[line]}</cyan> | - <level>{message}</level>"


def make_filter(name):
    """
    过滤操作,当日志要选择对应的日志文件的时候,通过filter进行筛选
    :param name:
    :return:
    """

    def filter_(record):
        return record["extra"].get("name") == name

    return filter_


async def global_execution_handler(request: Request, exc: Exception):
    """
    全局执行处理程序
    :param request:
    :param exc:
    :return:
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=dict(code=110, msg="未知错误:" + str(exc))
    )


def format_record(record: dict) -> str:
    """
    记录日志格式
    :param record:
    :return:
    例子：
    Example:
    # >>> payload = [{"users":[{"name": "Nick", "age": 87, "is_active": True}, {"name": "Alex", "age": 27, "is_active": True}], "count": 2}]
    # >>> logger.bind(payload=).debug("users payload")
    # >>> [   {   'count': 2,
    # >>>         'users': [   {'age': 87, 'is_active': True, 'name': 'Nick'},
    # >>>                      {'age': 27, 'is_active': True, 'name': 'Alex'}]}]
    """
    format_string = LOGURU_FORMAT
    if record["extra"].get("payload") is not None:
        record["extra"]["payload"] = pformat(
            record["extra"]["payload"], indent=4, compact=True, width=88
        )
        format_string += "\n<level>{extra[payload]}</level>"
    format_string += "{exception}\n"
    return format_string


# 添加全局error
app.add_middleware(
    ServerErrorMiddleware,
    handler=global_execution_handler,
)

# 添加跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class InterceptHandler(logging.Handler):
    """拦截处理程序"""

    def emit(self, record: logging.LogRecord):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def init_logging():
    """
    初始化日志
    :return:
    """
    loggers = {
        logging.getLogger(name)
        for name in logging.root.manager.loggerDict
        if name.startswith("uvicorn.")  # 以【uvicorn.】开始
    }
    for uvicorn_logger in loggers:
        uvicorn_logger.handlers = []
    # 这里啊错做事为了改变uvicorn默认的logger,采用loguru的logger
    intercept_handler = InterceptHandler()
    logging.getLogger("uvicorn").handlers = [intercept_handler]
    # 为sakura添加一个info log的文件,主要记录debug和info级别的日志
    log_info = os.path.join(settings.LOG_DIR, f"{settings.log_info}.log")
    # 为sakura添加一个error log的文件,主要记录warning和error级别的日志
    log_err = os.path.join(settings.LOG_DIR, f"{settings.log_err}.log")
    logger.add(log_info, enqueue=True, rotation="20 MB", level="DEBUG", filter=make_filter(settings.log_info))
    logger.add(log_err, enqueue=True, rotation="20 MB", level="ERROR", filter=make_filter(settings.log_err))

    # 配置loguru的日志句柄,sink代表输出目标
    logger.configure(
        handlers=[
            {"sink": sys.stdout, "level": logging.DEBUG, "format": format_record},
            {"sink": log_info, "level": logging.INFO, "format": INFO_FORMAT,
             "filter": make_filter(settings.log_info)},
            {"sink": log_err, "level": logging.WARNING, "format": ERROR_FORMAT,
             "filter": make_filter(settings.log_err)}
        ]
    )
    return logger
