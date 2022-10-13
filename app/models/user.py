#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/12 15:21
# @Author  : 冉勇
# @Site    : 
# @File    : user.py
# @Software: PyCharm
# @desc    :
from pydantic import BaseModel


class UserInDB(BaseModel):
    """
    这个模型是orm模型
    """
    username: str
    password: str
    is_superuser: bool = False
    status: bool = True
