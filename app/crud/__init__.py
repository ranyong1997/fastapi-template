#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/18 18:05
# @Author  : 冉勇
# @Site    :
# @File    : __init__.py.py
# @Software: PyCharm
# @desc    :
from ..models import async_engine, Base


# 异步创建连接
async def create_table():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
