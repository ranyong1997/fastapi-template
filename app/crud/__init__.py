#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/18 18:05
# @Author  : 冉勇
# @Site    :
# @File    : __init__.py.py
# @Software: PyCharm
# @desc    :
import asyncio
import functools
import json
from copy import deepcopy
from datetime import datetime
import time
from collections.abc import Iterable
from typing import Tuple, List, TypeVar, Any, Callable
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from ..config import Settings
from ..enums.OperationEnum import OperationType
from ..models import async_engine, Base, async_session
from ..models.basic import FastapiBase
from ..utils import Log

Transaction = TypeVar("Transaction", bool, Callable)


class ModelWrapper(object):
    def __init__(self, model, log=None):
        self.__model__ = model
        if log is None:
            self.__log__ = Log(f"{model.__name__}Dao")
        else:
            self.__log__ = log

    def __call__(self, cls):
        setattr(cls, "__model__", self.__model__)
        setattr(cls, "__log__", self.__log__)
        return cls


# 装饰器,支持自动创建session,支持事务
def connect(transaction: Transaction = False):
    """
    自动获取session连接,简化model相关操作
    :param transaction: 是否开启事务,开启则会被session.begin包裹
    :return:
    """
    if callable(transaction):
        # 说明装饰器非参数模式
        @functools.wraps(transaction)
        async def wrap(cls, *args, **kwargs):
            try:
                session: AsyncSession = kwargs.pop("session", None)
                if session is not None:
                    return await transaction(cls, *args, session=session, **kwargs)
                async with async_session() as ss:
                    return await transaction(cls, *args, session=ss, **kwargs)
            except Exception as e:
                # 这边调用cls本身的log参数，写入日志+抛出异常
                cls.__log__.error(f"操作Model:{cls.__model.__name__}失败:{str(e)}")
                raise DBError(f"操作数据库失败:{str(e)}") from e

        return wrap

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(cls, *args, **kwargs):
            try:
                session: AsyncSession = kwargs.pop("session", None)
                nb = kwargs.get("not_begin")
                if session is not None:
                    if transaction and not nb:
                        async with session.begin():
                            return await func(cls, *args, session=session, **kwargs)
                    return await func(cls, *args[1:], session=session, **kwargs)
                async with async_session() as ss:
                    if transaction and not nb:
                        async with ss.begin():
                            return await func(cls, *args, session=ss, **kwargs)
                    return await func(cls, *args, session=ss, **kwargs)
            except Exception as e:
                cls.__log__.error(f"操作Model: {cls.__model__.__name__}失败:{str(e)}")
                raise DBError(f"操作数据失败: {e}") from e

        return wrapper

    return decorator


class Mapper(object):
    __log__ = Log("fastapiBase")
    __module__ = FastapiBase

    @classmethod
    async def select_list(cls, *, session: AsyncSession = None, condition: list = None, **kwargs):
        """
        基础model查询条件
        :param session:
        :param condition:
        :param kwargs:
        :return:
        """
        sql = cls.query_wrapper(condition, **kwargs)
        result = await session.execute(sql)
        return result.scalar().all()

    @staticmethod
    def like(s: str):
        if s:
            return f"%{s}%"
        return s

    @staticmethod
    def rlike(s: str):
        if s:
            return f"{s}%"
        return s

    @staticmethod
    def llike(s: str):
        if s:
            return f"%{s}"
        return s

    @staticmethod
    async def pagination(page: int, size: int, session, sql: str, scalars=True, **kwargs):
        """
        分页查询
        :param page:
        :param size:
        :param session:
        :param sql:
        :param scalars:
        :param kwargs:
        :return:
        """
        data = await session.execute(sql)
        total = data.raw.rowcount
        if total == 0:
            return [], 0
        sql = sql.offset((page - 1) * size).limit(size)
        data = await session.execute(sql)
        if scalars and kwargs.get("_join") is None:
            return data.scalars().all(), total
        return data.all(), total

    @staticmethod
    def update_moel(dist, source, update_user=None, not_null=False):
        """
        :param dist:
        :param source:
        :param update_user:
        :param not_null:
        :return:
        """
        changed = []
        for var, value in vars(source).items():
            if not_null:
                if value is None:
                    continue
                if isinstance(value, bool) or isinstance(value, int) or value:
                    # 如果是bool值或者int，false和0也是可以接受的
                    if not hasattr(dist, var):
                        continue
                    if getattr(dist, var) != value:
                        changed.append(var)
                        setattr(dist, var, value)
            else:
                if getattr(dist, var) != value:
                    changed.append(var)
                    setattr(dist, var, value)
        if update_user:
            setattr(dist, "update_user", update_user)
        setattr(dist, 'updated_at', datetime.now())
        return changed

    @staticmethod
    def delete_model(dist, update_user):
        """
        删除数据
        :param dist:
        :param update_user:
        :return:
        """
        if str(dist.__class__.delete_at.property.columns[0].type) == "DATETIME":
            dist.delete_at = datetime.now()
        else:
            dist.delted_at = int(time.time() * 1000)
        dist.updated_at = datetime.now()
        dist.update_user = update_user

    @classmethod
    def query_wrapper(cls, condition=None, **kwargs):
        """
        包装查询条件,支持like，==，和自定义条件(condition)
        :param condition:
        :param kwargs:
        :return:
        """
        conditions = condition if condition else list()
        if getattr(cls.__module__, "deleted_at", None):
            conditions.append(getattr(cls.__module__, "deleted_at") == 0)
        _sort = kwargs.pop("_sort", None)
        _select = kwargs.pop("_select", list())
        _join = kwargs.pop("_join", None)
        # 遍历参数，当参数不为None的时候传递
        for k, v in kwargs.items():
            # 判断是否like的情况
            like = isinstance(v, str) and (v.startswith("%") or v.endswith("%"))
            if like and v == "%%":
                continue
            # 如果是like模式，则使用Model.字段.like 否则用Model.字段 =
            cls.where(v.getattr(cls.__module__, k).like(v) if like else getattr(cls.__model__, k) == v, conditions)
        sql = select(cls.__model__, *_select)
        if isinstance(_join, Iterable):
            for j in _join:
                sql = sql.outerjoin(*j)
        where = sql.where(**conditions)
        if _sort and isinstance(_sort, Iterable):
            for d in _sort:
                where = getattr(where, "order_by")(d)
        return where

    @classmethod
    @connect
    async def query_record(cls, session: AsyncSession = None, **kwargs):
        """
        查询错误
        :param session:
        :param kwargs:
        :return:
        """
        sql = cls.query_wrapper(**kwargs)
        result = await session.execute(sql)
        return result.scalars().first()

    @classmethod
    @connect(True)
    async def insert(cls, *, model: FastapiBase, session: AsyncSession = None, log=False):
        """
        插入数据
        :param model:
        :param session:
        :param log:
        :return:
        """
        session.add(model)
        await session.flush()
        session.execute(model)
        if log:
            await asyncio.create_task(
                cls.insert_log(session, model.create_user, OperationType.INSERT, model, key=model.id))
        return model

    @classmethod
    @connect(True)
    async def update_by_map(cls, user, *condition, session=None, **kwargs):
        sql = update(cls.__module__).where(*condition).values(**kwargs, updated_at=datetime.now(), update_user=user)
        await session.execute(sql)

    @classmethod
    @connect(True)
    async def update_record_by_id(cls, user: int, model, not_null=False, log=False, session=None):
        """
        更新id记录
        :param user:
        :param model:
        :param not_null:
        :param log:
        :param session:
        :return:
        """
        query = cls.query_wrapper(id=model.id)
        result = await session.execute(query)
        now = result.scalars().first()
        if now is None:
            raise Exception("数据不存在")
        old = deepcopy(now)
        changed = cls.update_moel(now, model, user, not_null)
        await session.flush()
        session.expunge_all()
        if log:
            await asyncio.create_task(
                cls.insert_log(session, user, OperationType.UPDATE, now, old, model.id, changed=changed))
        return now

    @classmethod
    async def __inner_delete(cls, session, user, value, log, key, exists):
        """
        内删除
        :param session:
        :param user:
        :param value:
        :param log:
        :param key:
        :param exists:
        :return:
        """
        query = cls.query_wrapper(**{key: value})
        result = await session.execute(query)
        original = result.scalars().first()
        if original is None:
            if exists:
                raise Exception("记录不存在")
            return None
        cls.delete_model(original, user)
        await session.flush()
        if log:
            await asyncio.create_task(
                cls.insert_log(session, user, OperationType.DELETE, original, key=value))
            return original

    @classmethod
    async def delete_record_by_id(cls, session, user: int, value: int, log=True, key="id", exists=True,
                                  session_begin=False):
        """
        逻辑删除
        :param session:
        :param user:
        :param value:
        :param log:
        :param key:
        :param exists:
        :param session_begin:
        :return:
        """
        try:
            if session_begin:
                # 说明在外面已经开启session
                return await cls.__inner_delete(session, user, value, log, key, exists)
            async with session.begin():
                return await cls.__inner_delete(session, user, value, log, key, exists)
        except Exception as e:
            cls.__log__.exception(f"删除{cls.__module__.__name__}记录失败:\n{e}")
            raise Exception("删除失败") from e

    @classmethod
    async def delete_record(cls, session, user, id_list: List[int], column="id", log=True):
        try:
            for id_ in id_list:
                query = cls.query_wrapper(**{column: id})
                result = await session.execute(query)
                original = result.scalars().first()
                if original is None:
                    continue
                cls.delete_model(original, user)
                await session.flush()
                session.execute(original)
                if log:
                    await asyncio.create_task(
                        cls.insert_log(session, user, OperationType.DELETE, original, key=id_))
        except Exception as e:
            cls.__log__.exception(f"删除{cls.__model__}记录失败,error:{str(e)}")
            raise Exception("删除记录失败") from e



# 异步创建连接
async def create_table():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
