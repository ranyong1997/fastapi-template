#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/26 15:53
# @Author  : 冉勇
# @Site    : 
# @File    : db_user_new.py
# @Software: PyCharm
# @desc    : 用户建表
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from ..models import Base


# 定义 User 类
class User(Base):
    __tablename__ = 'users'  # 定义表名
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    name = Column(String(255))
    password = Column(String(255))
    is_active = Column(Boolean, default=True)   # 是否被冻结，默认未冻结
    items = relationship("Item", back_populates="owner")  # 定义一对多关系
    # 关联 Item 表


# 定义 Item 类
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(String(255), index=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="items")  # 定义关联
    # 关联 User 表
