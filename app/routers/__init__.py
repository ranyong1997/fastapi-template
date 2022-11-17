#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/12 15:23
# @Author  : 冉勇
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
# @desc    :
from fastapi import APIRouter
from .router_user import router as user_router
from .router_docs import custom_docs
from ..config import settings
from .router_dev import router as dev_router
from .router_user_new import router as user_new_router

api_router = APIRouter(prefix=settings.url_prefix)
api_router.include_router(user_new_router)
api_router.include_router(user_router)
if settings.debug:
    api_router.include_router(dev_router)
