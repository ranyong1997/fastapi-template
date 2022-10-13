#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/12 15:23
# @Author  : 冉勇
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
# @desc    :
from fastapi import APIRouter
from .user import router as user_router
from .docs import custom_docs
from ..config import settings
from .dev import router as dev_router

api_router = APIRouter(prefix=settings.url_prefix)
api_router.include_router(user_router)
if settings.debug:
    api_router.include_router(dev_router)

api_router.include_router(user_router)
