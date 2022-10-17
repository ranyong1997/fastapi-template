#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/12 15:40
# @Author  : 冉勇
# @Site    : 
# @File    : user.py
# @Software: PyCharm
# @desc    :
from fastapi import APIRouter, Body, Depends
from ..dependencies import auth_depend
from ..libs.db_lib import db
from ..utils import hash_tool
from ..models.user import UserInDB
from ..schemas.user import UserSignUp, UserInfo
from ..utils import log

router = APIRouter(prefix="/user", tags=['用户接口'])


@router.post("/signup", summary="注册接口")
def signup(form_data: UserSignUp = Body(...)):
    username = form_data.username
    password = form_data.password
    # 根据用户名去数据库里面查询对应的 user
    user = db.get_or_none(username)
    if user is not None:
        log.warning(f"当前用户名【{username}】已经被占用")
        return {"msg": "当前用户名已经被占用"}
    # 保存到数据库 哈希加密
    encode_pwd = hash_tool.encrypt_password(password)
    user = UserInDB(username=username, password=encode_pwd)
    db.save(user)
    return {"msg": "ok"}


@router.post("/login", summary="登录接口")
def login():
    return {"msg": "login"}


@router.get("/me", summary="个人信息")
def get_my_info(me: UserInDB = Depends(auth_depend)):
    user_info = UserInfo(**me.dict())
    # 返回
    return {"mag": user_info}


@router.get("/vip", summary="查看vip信息", dependencies=[Depends(auth_depend)])
def get_vip_info():
    return {"msg": "vip info"}
