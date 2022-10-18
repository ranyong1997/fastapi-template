#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/17 17:12
# @Author  : 冉勇
# @Site    : 
# @File    : user_sql.py
# @Software: PyCharm
# @desc    : 用户建库
from datetime import datetime
from sqlalchemy import Column, INT, TIMESTAMP, String
from ..config import Settings


class User(Settings):
    __tablename__ = 'users'  # 表名
    id = Column(INT, primary_key=True)  # 设置主键
    username = Column(String(16), unique=True, index=True)  # unique=True 记录值都要唯一，不允许重复
    name = Column(String(16), index=True)  # 昵称
    password = Column(String(32), unique=False)
    is_superuser = Column(Boolean=False, unique=False, comment="是否管理员")  # 是否管理员
    status = Column(Boolean=False, unique=False, comment="是否合法")  # 状态（禁用/正常） True为正常
    create_at = Column(TIMESTAMP, nullable=False, default=datetime.now(), comment="创建时间")  # 创建时间
    last_login_at = Column(TIMESTAMP, comment="最后登录时间")  # 最后一次登录时间

    def __init__(self, username, name, password, is_superuser=False, status=True):
        self.username = username
        self.name = name
        self.password = password
        self.is_superuser = is_superuser
        self.status = status
        self.create_at = datetime.now()
