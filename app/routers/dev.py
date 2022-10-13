#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/12 16:39
# @Author  : 冉勇
# @Site    : 
# @File    : dev.py
# @Software: PyCharm
# @desc    :
import datetime

from fastapi import APIRouter

router = APIRouter(prefix="/dev", tags=['开发调试用接口'])


@router.get("/ping", summary="ping")
def ping():
    return {"msg": "pong"}


@router.get("/now", summary="now")
def now():
    return {"msg": datetime.datetime.now()}
