#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/21 17:59
# @Author  : 冉勇
# @Site    : 
# @File    : basic.py
# @Software: PyCharm
# @desc    : 基本方法
import json
from datetime import datetime
from decimal import Decimal
from typing import Tuple
from sqlalchemy import INT, Column, BIGINT, TIMESTAMP
from ..models import Base
from ..config import Settings


class FastapiBase(Base):
    id = Column(INT, primary_key=True)
    create_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)
    deleted_at = Column(BIGINT, nullable=False, default=0)
    create_user = Column(INT, nullable=False)
    update_user = Column(INT, nullable=False)
    __abstract__ = True
    __fields__: Tuple[Column] = [id]
    __tag__ = "未定义"
    __alias__ = dict(name="名称")
    __show__ = 1

    def __init__(self, user, id=None):
        self.create_at = datetime.now()
        self.updated_at = datetime.now()
        self.create_user = user
        self.update_user = user
        self.update_user = user
        self.deleted_at = user

    def serialize(self,*ignore):
        """
        :param ignore:
        :return:
        """
        data = {}
        for c in self.__table__.columns:
            if c.name in ignore:
                continue
            val = getattr(self,c.name)
            if isinstance(val,datetime):
                data[c.name] = val.strftime("%Y-%m-%d %H:%M:%S")
