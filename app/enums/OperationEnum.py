#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/24 10:52
# @Author  : 冉勇
# @Site    : 
# @File    : OperationEnum.py
# @Software: PyCharm
# @desc    : 数据库类型
from enum import IntEnum


class OperationType(IntEnum):
    INSERT = 0
    UPDATE = 1
    DELETE = 2
    EXECUTE = 3
    STOP = 4
