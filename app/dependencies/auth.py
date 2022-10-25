#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/11 10:04
# @Author  : 冉勇
# @Site    : 
# @File    : auth.py
# @Software: PyCharm
# @desc    :
import traceback
import jwt
from datetime import timedelta, datetime, timezone
from typing import Optional
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from app.config import settings
from app.libs.db_lib import db
from app.utils import log

# 获取token地址
tokenUrl = settings.swagger_ui_oauth2_redirect_url
oauth2_scheme = OAuth2PasswordBearer(tokenUrl)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(seconds=settings.jwt_exp_seconds)
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def auth_depend(token: str = Depends(oauth2_scheme)):
    # 第二步 解析token 中的payload 信息
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError:
        exc_msg = '\n' + "-" * 40 + " 捕捉到一些错误 " + "-" * 40 + "\n"
        exc_msg += traceback.format_exc() + "\n"
        local_vars = locals()
        exc_msg += f"{locals()=}" + "\n"
        exc_msg += "-" * 100
        log.error(JWTError)
        return HTTPException(status_code=401, detail="token已失效，请重新登录！")
    # 第三步 根据payload 中的信息去数据库中找到对应的用户
    username = payload.get('username')
    user = db.get_or_none(username)
    return {"msg": "认证不通过"} if user is None else user
