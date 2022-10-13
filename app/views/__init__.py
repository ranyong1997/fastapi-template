#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/12 17:19
# @Author  : 冉勇
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
# @desc    :
from fastapi import APIRouter
from .home import router as home_router

views_router = APIRouter()
views_router.include_router(home_router)
