#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/26 16:03
# @Author  : 冉勇
# @Site    : 
# @File    : db_user_new.py
# @Software: PyCharm
# @desc    : 用户相关的数据模型
# 导入相关模块
from pydantic import BaseModel, validator
from typing import Optional


# 定义ItemBase模型类，从BaseModel继承
class ItemBase(BaseModel):
    # 定义模型的属性
    title: str
    description: Optional[str] = None


# 定义ItemCreate模型类，从ItemBase继承
class ItemCreate(ItemBase):
    pass


# 定义Item模型类，从ItemBase继承
class Item(ItemBase):
    title: str
    description: str

    class Config:  # 配置项中启用ORM模式
        orm_mode = True


# 定义Item模型类，从ItemBase继承
class Item_Config(BaseModel):
    id: str
    title: str
    description: str

    class Config:  # 配置项中启用ORM模式
        orm_mode = True


# 定义Item模型类，从ItemBase继承
class Item_Delete(BaseModel):
    id: str

    class Config:  # 配置项中启用ORM模式
        orm_mode = True


# 定义UserBase模型类，从BaseModel继承
class UserBase(BaseModel):
    email: str
    name: str
    password: str

    @validator('email', 'name', 'password')
    def field_not_empty(cls, v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise {'不能为空'}
        return v


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: str
    email: str
    name: str
    status: bool = True

    class Config:  # 配置项中启用ORM模式
        orm_mode = True
