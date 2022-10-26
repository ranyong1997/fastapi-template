#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/26 16:16
# @Author  : 冉勇
# @Site    : 
# @File    : database.py
# @Software: PyCharm
# @desc    :
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import config

# 创建数据库引擎
engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
with engine.connect() as conn:
    conn.execute(
        "CREATE DATABASE IF NOT EXISTS fastapi default character set utf8mb4 collate utf8mb4_unicode_ci")
# 关闭引擎
engine.dispose()

# 创建数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 声明基类
Base = declarative_base()
