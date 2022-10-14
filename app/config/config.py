#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/11 16:05
# @Author  : 冉勇
# @Site    : 
# @File    : config.py
# @Software: PyCharm
# @desc    :
import os
from pathlib import Path
from typing import List
from pydantic import BaseSettings


class Settings(BaseSettings):
    class Config:
        # 环境变量文件
        env_file = ".env"

    # debug模式
    debug: bool = True
    # jwt加密的key
    jwt_secret_key: str = 'ran'
    # jwt 加密算法
    jwt_algorithm: str = "HS256"
    # token过期时间，单位：秒
    jwt_exp_seconds: int = 60 * 60
    # 项目标题
    project_title = "FastAPI 后端"
    # 项目描述
    project_description = "一个牛逼的API后端"
    # 项目版本
    project_version = '0.0.1'
    # url的前缀
    url_prefix: str = "/api/v1"
    # host
    server_host: str = "localhost"
    server_port: int = 8000
    # 是否启用/test接口
    enable_test_router: bool = True
    # swagger docs 后登录重定向地址
    swagger_ui_oauth2_redirect_url: str = f"{url_prefix}/test/token"
    # 项目根目录 父一级再父一级再父一级
    base_dir = Path(__file__).absolute().parent.parent.parent
    # 日志目录
    log_dir = base_dir / 'logs'
    # 日志名
    log_info = 'log_info'
    log_err = 'log_error'
    log_warning = 'log_warning'
    log_debug = 'log_debug'
    log_exception = 'log_exception'
    log_name = os.path.join(log_dir, 'fastapi_template.log')
    # 静态资源
    static_dir = base_dir / 'static'
    static_url_prefix: str = '/static'
    # 用户上传目录
    media_dir = base_dir / 'media'
    media_url_prefix: str = '/media'
    # jinjia2模板目录
    jinja2_template_dir = base_dir / 'backend' / 'templates'
    # 中间件配置
    # 跨域请求
    cors_origins: List[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["PUT", "POST", "GET", "DELETE", "OPTIONS"]
    cors_allow_headers: List[str] = ["*"]
    # Session
    session_secret_key = "sadehewagbwft34ba"
    session_cookie = "session_id"
    session_max_age = 14 * 24 * 60 * 60
