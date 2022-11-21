#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/26 16:03
# @Author  : 冉勇
# @Site    : 
# @File    : user_crud.py
# @Software: PyCharm
# @desc    : user_new【curd】
from sqlalchemy.orm import Session
from app.models import db_user_new as models
from app.schemas import schema_user_new as schemas
from app.utils.hash_lib import Hash


# 创建用户
def create_user(db: Session, user: schemas.UserCreate):
    """
    创建用户
    :param db: 数据库会话
    :param user: 用户模型
    :return: 根据email和password登录的用户信息
    """
    hash_password = Hash.encrypt_password(user.password)  # 哈希加密密码
    db_users = models.User(email=user.email, name=user.name,
                           password=hash_password)
    db.add(db_users)  # 添加到会话
    db.flush()
    db.commit()  # 提交到数据库
    db.refresh(db_users)  # 刷新数据库
    return db_users


# 通过id获取单个用户
def get_user(db: Session, user_id: int):
    """
    根据id获取用户信息
    :param db: 数据库会话
    :param user_id: 用户id
    :return: 用户信息
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


# 通过email读取单个用户
def get_user_by_email(db: Session, email: str):
    """
    根据email获取用户信息
    :param db: 数据库会话
    :param email: 用户email
    :return: 用户信息
    """
    return db.query(models.User).filter(models.User.email == email).first()


# 获取前100个用户
def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    获取特定数量的用户
    :param db: 数据库会话
    :param skip: 开始位置
    :param limit: 限制数量
    :return: 用户信息列表
    """
    return db.query(models.User).offset(skip).limit(limit).all()


# 删除用户，根据id删除
def delete_user(db: Session, user_id: int):
    """
    删除用户
    :param user_id:
    :param db:
    :return:
    """
    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()
    return {'message': '删除成功'}


# 创建用户item
def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    """
    创建用户item
    :param db: 数据库会话
    :param item: Item对象
    :param user_id: 用户id
    :return: Item模型对象
    """
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# 获取前100个item中的数据
def get_items(db: Session, skip: int = 0, limit: int = 100):
    """
    获取指定数量的item
    :param db: 数据库会话
    :param skip: 开始位置
    :param limit: 限制数量
    :return: item列表
    """
    return db.query(models.Item).offset(skip).limit(limit).all()


# 根据user_id返回item数据
def get_item_by_user_id(db: Session, user_id: int):
    """
    根据user_id获取item.id的数据
    :param user_id:
    :param db:
    :param item:
    :return:
    """
    return db.query(models.Item).filter(models.Item.owner_id == user_id).all()


# 根据user_id批量更新item
def update_items(db: Session, item: schemas.Item, user_id: int):
    """
    根据user_id批量更新items
    :param user_id:
    :param db:
    :param item:
    :return:
    """
    db.query(models.Item).filter(models.Item.owner_id == user_id).update(
        {'title': item.title, 'description': item.description})
    db.commit()
    return {'message': '更新成功'}


# 根据items_id修改title和description
def update_item_by_item_id(db: Session, item: schemas.Item_Config):
    """
    根据items_id修改title和description
    :param item:
    :param db:
    :param id:
    :return:
    """
    db.query(models.Item).filter(models.Item.id == item.id).update(
        {'title': item.title, 'description': item.description})
    db.commit()
    return {'message': '修改成功'}


# 根据items_id删除数据
def delete_item_by_item_id(db: Session, item: schemas.Item_Delete):
    """
    根据items_id删除数据
    :param db:
    :param item:
    :return:
    """
    db.query(models.Item).filter(models.Item.id == item.id).delete()
    db.commit()
    return {'message': '删除成功'}
