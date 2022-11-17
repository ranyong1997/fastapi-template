#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/26 16:16
# @Author  : 冉勇
# @Site    : 
# @File    : database.py
# @Software: PyCharm
# @desc    : 公共依赖
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import config

# 创建数据库引擎
engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
with engine.connect() as conn:
    conn.execute(
        "CREATE DATABASE IF NOT EXISTS fastapi default character set utf8mb4 collate utf8mb4_unicode_ci")
engine.dispose()

# 创建本地会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建数据模型基础类
Base = declarative_base()
