#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/26 16:03
# @Author  : 冉勇
# @Site    : 
# @File    : user_new.py
# @Software: PyCharm
# @desc    : 用户模型模式
from typing import List
from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True
