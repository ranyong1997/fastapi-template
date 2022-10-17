#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/12 15:24
# @Author  : 冉勇
# @Site    : 
# @File    : docs.py
# @Software: PyCharm
# @desc    : 处理docs缓慢问题(仅用于调试，项目上线会隐藏docs)
from fastapi import APIRouter, FastAPI, Depends
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.security import OAuth2PasswordRequestForm
from ..config import settings
from ..dependencies import create_access_token
from ..libs.db_lib import db
from ..utils import hash_tool
from ..utils import log
router = APIRouter()


def custom_docs(application: FastAPI):
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=application.openapi_url,
            title=application.title + " - Swagger UI",
            oauth2_redirect_url=application.swagger_ui_oauth2_redirect_url)

    async def redoc_html():
        return get_redoc_html(
            openapi_url=application.openapi_url,
            title=application.title + " - ReDoc")

    def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
        # 第一步 拿到用户名和密码，校验
        username = form_data.username
        password = form_data.password
        # 第二步 通过用户名去数据库中查找对应的user
        user = db.get_or_none(username)
        if user is None:
            log.error("登录失败，用户名与密码不匹配")
            return {"msg": "登录失败，用户名与密码不匹配"}
        # 第三步 检查密码
        if not hash_tool.check_password(user.password, password):
            log.error("登录失败，用户名与密码不匹配")
            return {"msg": "登录失败，用户名与密码不匹配"}
        # 第四步 生成token
        token = create_access_token({"username": user.username})
        return {"access_token": token, "token_type": "bearer"}

    if settings.debug:  # debug为False，用户就无法看到docs
        application.get("/docs", include_in_schema=False)(custom_swagger_ui_html)
        application.get("/redoc", include_in_schema=False)(redoc_html)
        application.post(settings.swagger_ui_oauth2_redirect_url, summary="获取token接口", tags=['获取token接口'])(get_token)
