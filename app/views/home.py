#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/12 17:19
# @Author  : 冉勇
# @Site    : 
# @File    : home.py
# @Software: PyCharm
# @desc    :
from fastapi.responses import HTMLResponse
from fastapi import APIRouter

# include_in_schema 在swagger中显示出来
router = APIRouter(prefix="/home", include_in_schema=True, tags=['HttpResponseDemo接口'])


@router.get("")
def home():
    return HTMLResponse("<h1>HOME</h1>")
