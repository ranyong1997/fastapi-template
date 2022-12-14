#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/11 16:05
# @Author  : 冉勇
# @Site    : 
# @File    : config.py
# @Software: PyCharm
# @desc    : 全局配置文件
import os
from pathlib import Path
from typing import List
from pydantic import BaseSettings

# 项目根目录 父一级再父一级再父一级 root根路径
base_dir = Path(__file__).absolute().parent.parent.parent


class Settings(BaseSettings):
    # debug模式
    debug: bool = True
    # 数据库—server
    MYSQL_HOST: str = None  # 数据库主机
    MYSQL_PORT: int = None  # 数据库端口
    MYSQL_USER: str = None  # 数据库用户名
    MYSQL_PWD: str = None  # 数据库密码
    DBNAME: str = None  # 数据库表名
    # redis_server:关闭redis可以让job同时运行多次
    REDIS_ON: bool = None  # redis开关
    REDIS_HOST: str = None  # redis主机
    REDIS_PORT: int = None  # redis端口
    REDIS_DB: int = None  # redis表名
    REDIS_PASSWORD: str = None  # redis密码
    REDIS_NODES: List[dict] = []  # redis连接信息
    # sqlalchemy_server
    SQLALCHEMY_DATABASE_URI: str = ''
    # 异步URI
    ASYNC_SQLALCHEMY_URI: str = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # jwt加密的key
    jwt_secret_key: str = 'ran'
    # jwt 加密算法
    jwt_algorithm: str = "HS256"
    # token过期时间，单位：秒
    jwt_exp_seconds: int = 7 * 24 * 60 * 60
    # 项目标题
    project_title = "FastAPI 后端模板"
    # 项目描述
    project_description = "自用后端模板，开发简单"
    # 项目版本
    project_version = '0.0.2'
    # url的前缀
    url_prefix: str = "/api/v1"
    # host
    server_host: str = "192.168.1.243"
    server_port: int = 8000
    # 是否启用/test接口
    enable_test_router: bool = True
    # swagger docs 后登录重定向地址
    swagger_ui_oauth2_redirect_url: str = f"{url_prefix}/test/token"
    # 日志目录
    log_dir = base_dir / 'logs'
    # 日志名
    log_info = 'log_info'
    log_error = 'log_error'
    log_warning = 'log_warning'
    log_debug = 'log_debug'
    log_name = os.path.join(log_dir, 'fastapi_template.log')
    # 静态资源
    static_dir = base_dir / 'static'
    static_url_prefix: str = '/static'
    # 环境
    env_dir = base_dir / 'conf'
    env_url_prefix: str = '/conf'
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
    TABLE_TAG = "__tag__"
    BANNER = """
      ____|             |                 _)      __ __|                        |         |         
      |     _` |   __|  __|   _` |  __ \   |         |   _ \  __ `__ \   __ \   |   _` |  __|   _ \ 
      __|  (   | \__ \  |    (   |  |   |  | _____|  |   __/  |   |   |  |   |  |  (   |  |     __/ 
     _|   \__,_| ____/ \__| \__,_|  .__/  _|        _| \___| _|  _|  _|  .__/  _| \__,_| \__| \___| 
                                   _|                                   _|                          
    """


class DevConfig(Settings):
    # 开发者模式
    class Config:
        env_file = os.path.join(base_dir, "conf", "dev.env")


class ProConfig(Settings):
    # 正式环境
    class Config:
        env_file = os.path.join(base_dir, "conf", "pro.env")


# 获取sakura环境变量
FASTAPI_ENV = os.environ.get("fastapi_env", "dev")

# 如果fastapi_env存在且为pro
Config = ProConfig() if FASTAPI_ENV and FASTAPI_ENV.lower() == "pro" else DevConfig()
# 初始化 sqlalchemy（由创建数据引擎）
Config.SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{Config.MYSQL_USER}:{Config.MYSQL_PWD}@{Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.DBNAME}'
# 初始化sqlalchemy
Config.ASYNC_SQLALCHEMY_URI = f'mysql+aiomysql://{Config.MYSQL_USER}:{Config.MYSQL_PWD}' \
                              f'@{Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.DBNAME}'
# 初始化redis
Config.REDIS_NODES = [
    {
        "host": Config.REDIS_HOST, "port": Config.REDIS_PORT, "db": Config.REDIS_DB, "password": Config.REDIS_PASSWORD
    }
]
