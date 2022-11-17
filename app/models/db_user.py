#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/12 15:21
# @Author  : 冉勇
# @Site    : 
# @File    : db_user.py
# @Software: PyCharm
# @desc    :
from pydantic import BaseModel


# 定义UserInDB模板类，从BaseModel继承
class UserInDB(BaseModel):
    """
    这个模型是orm模型
    """
    username: str  # 定义模型username属性
    password: str  # 定义模型password属性
    is_superuser: bool = False  # 定义模型is_superuser属性
    status: bool = True  # 定义模型status属性
