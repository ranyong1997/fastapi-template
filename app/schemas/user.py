#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/12 15:22
# @Author  : 冉勇
# @Site    : 
# @File    : user.py
# @Software: PyCharm
# @desc    :
from pydantic import BaseModel, validator, Field


class UserSignUp(BaseModel):
    username: str = Field(..., example='tom')
    password: str = Field(..., example='123')
    password2: str = Field(..., example='123')

    @validator("password2")
    def two_password_match(cls, value, values):
        if value != values['password']:
            raise ValueError("两个密码必须一致")
        return value


class UserLogin(BaseModel):
    username: str = Field(..., example='tom')
    password: str = Field(..., example='123')


class UserInfo(BaseModel):
    username: str
    is_superuser: bool = False
    status: bool = True
