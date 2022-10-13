#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/10 15:19
# @Author  : 冉勇
# @Site    : 
# @File    : db_lib.py
# @Software: PyCharm
# @desc    :
import json
from pathlib import Path
from typing import List
from pydantic import parse_file_as
from app.models.user import UserInDB


class FakeDB:
    def __init__(self):
        self.__data_path = Path(__file__).absolute().parent / 'data.json'
        if not self.__data_path.exists():
            self.__data: List[UserInDB] = []
        else:
            self.__data: List[UserInDB] = parse_file_as(List[UserInDB], self.__data_path)

    def all(self):
        print("-" * 35)
        print(f"{'No.':>3}{'username':>15}{'password':>15}")
        print("-" * 35)
        for i, user in enumerate(self.__data):
            print(f"{i:>3}{user.username:>15}{user.password:>15}")
        print("-" * 35)
        return self.__data

    def get_or_none(self, name):
        for user in self.__data:
            if user.username == name:
                return user
        return None

    def save(self, user):
        if self.get_or_none(name=user.username) is not None:
            raise ValueError(f"不满足唯一性约束，当前用户名：{user.username}")
        self.__data.append(user)
        data = [x.dict() for x in self.__data]
        self.__data_path.write_text(json.dumps(data, indent=4), encoding="utf-8")


db = FakeDB()

if __name__ == '__main__':
    db.all()
    print(db.get_or_none("lily"))
    db.save(UserInDB(username='lily', password="1"))
    print(db.get_or_none("lily"))
