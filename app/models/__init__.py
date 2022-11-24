#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/12 15:20
# @Author  : 冉勇
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
# @desc    : orm操作
from app.config.config import Config as config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker  # 创建session类
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine  # 异步操作、创建engine
from sqlalchemy.ext.declarative import declarative_base  # 建立基本映射类


# 创建数据库
def create_database():
    engine = create_engine(
        f'mysql+mysqlconnector://{config.MYSQL_USER}:{config.MYSQL_PWD}@{config.MYSQL_HOST}:{config.MYSQL_PORT}',
        echo=True)
    with engine.connect() as conn:
        conn.execute(
            "CREATE DATABASE IF NOT EXISTS fastapi default character set utf8mb4 collate utf8mb4_unicode_ci")
    # 关闭连接池的所有连接
    engine.dispose()


# 优先建表
create_database()

# 异步engine
async_engine = create_async_engine(config.ASYNC_SQLALCHEMY_URI, pool_recycle=1500)
# 异步会话
async_session = sessionmaker(async_engine, class_=AsyncSession)

# 创建对象的基类
Base = declarative_base()
