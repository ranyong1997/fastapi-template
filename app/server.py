#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/10 15:07
# @Author  : 冉勇
# @Site    : 
# @File    : server.py
# @Software: PyCharm
# @desc    : 配置文件
import asyncio
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from .config.config import FASTAPI_ENV
from .routers import custom_docs, api_router
from .config import settings
from .views import views_router
from . import init_logging
from .crud import create_table

# 实例化fastapi对象
app = FastAPI(docs_url=None,
              redoc_url=None,
              title=settings.project_title,
              description=settings.project_description,
              version=settings.project_version)

# 挂载静态文件目录
app.mount(settings.static_url_prefix, StaticFiles(directory=settings.static_dir))
# 用户上传文件
app.mount(settings.media_url_prefix, StaticFiles(directory=settings.media_dir))

# 自定义docs界面
custom_docs(app)

# 挂载api路由
app.include_router(api_router)

# 挂载view路由
app.include_router(views_router)

# 挂载loguru路由
logger = init_logging()
logger.bind(name=None).opt(ansi=True).success(
    f"fastapi 正在运行环境: <blue>{FASTAPI_ENV} 网址: http://localhost:8000/docs</blue>")
logger.bind(name=None).success(settings.BANNER)


@app.on_event("startup")
async def init_database():
    """
    初始化数据库.建表
    :return:
    """
    try:
        asyncio.create_task(create_table())
        logger.bind(name=None).success("数据库和表创建成功.          ✔")
    except Exception as e:
        logger.bind(name=None).error(f"数据库和表创建失败.          ❌ \n Error:{str(e)}")
        raise