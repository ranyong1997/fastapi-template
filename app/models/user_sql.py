#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/17 17:12
# @Author  : 冉勇
# @Site    : 
# @File    : user_sql.py
# @Software: PyCharm
# @desc    : 用户建库
from datetime import datetime
from sqlalchemy import Column, INT, TIMESTAMP, Boolean, BIGINT
from ..config import Settings

class User(Settings):
    __tablename__ = 'users'
