#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/12 15:20
# @Author  : 冉勇
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
# @desc    : orm操作
from ..config import Settings
from ..config.config import config
from ..enums.DatabaseEnum import DatabaseEnum
from .user import UserInDB
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker  # 创建session类
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine  # 异步操作、创建engine
from sqlalchemy.ext.declarative import declarative_base  # 建立基本映射类


def create_database():
    engine = create_engine('mysql+mysqlconnector://{}:{}@{}:{}'.format(
        config.MYSQL_USER, config.MYSQL_PWD, config.MYSQL_HOST, config.MYSQL_PORT), echo=True)
    with engine.connect() as conn:
        conn.execute(
            "CREATE DATABASE IF NOT EXISTS fastapi default character set utf8mb4 collate utf8mb4_unicode_ci")
    # 关闭引擎
    engine.dispose()


# 优先建表
create_database()

# 异步engine
async_engine = create_async_engine(config.ASYNC_SQLALCHEMY_URI, pool_recycle=1500)

async_session = sessionmaker(async_engine, class_=AsyncSession)

# 创建对象的基类
Base = declarative_base()


# 创建一个数据库助手类
class DatabaseHelper(object):
    def __init__(self):
        self.connections = {}

    async def get_connection(self, sql_type: int, host: str, port: int, username: str, password: str, database: str):
        # 拼接key
        key = f"{host}:{port}:{database}:{username}:{password}:{database}"
        connection = self.connections.get(key)
        # 判断是否已经连接,如果True,直接返回
        if connection is not None:
            return connection
        # 获取sqlalchemy需要jdbc url
        jdbc_url = DatabaseHelper.get_jdbc_url(sql_type, host, port, username, password, database)
        # 创建异步引擎
        eg = create_engine(jdbc_url, pool_recycle=1500)
        # 建立会话
        ss = sessionmaker(bind=eg, class_=AsyncSession)
        # 将数据缓存起来
        data = dict(engine=eg, session=ss)
        self.connections[key] = data
        return data

    @staticmethod
    def get_jdbc_url(sql_type: int, host: str, port: int, username: str, password: str, database: str):
        if sql_type == DatabaseEnum.MYSQL:
            # MYSQL模式
            return f"mysql+aiomysql://{username}:{password}@{host}:{port}/{database}"
        if sql_type == DatabaseEnum.POSTGRESQL:
            # POSTGRESQL模式
            return f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{database}"
        raise Exception("未知数据库类型,目前只支持mysql和postgresql")

    # 删除连接
    def remove_connection(self, host: str, port: int, username: str, password: str, database: str):
        key = f"{host}:{port}:{database}:{username}:{password}:{database}"
        if self.connections.get(key):
            self.connections.pop(key)


db_heloper = DatabaseHelper()
