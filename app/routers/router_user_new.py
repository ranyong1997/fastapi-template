#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/26 16:07
# @Author  : 冉勇
# @Site    : 
# @File    : db_user_new.py
# @Software: PyCharm
# @desc    : 与用户路由相关
from typing import List
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session  # 导入会话组件
from app.config.database import engine, get_db
from app.crud import user_crud as crud
from app.models import db_user_new as models  # 导入前面定义的models模块
from app.schemas import schema_user_new as schemas  # 导入前面定义的models模块

# 生成数据库中的表
models.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/user_new", tags=['用户接口_new'])


# 定义路径操作函数，并注册路由路径：用户
@router.post("/creat/", response_model=schemas.User, summary="创建用户")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 根据email查找用户，如果用户存在，提示该邮箱已经被注册
    if crud.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=400, detail="电子邮件已注册")
    # 返回创建的user对象
    return crud.create_user(db=db, user=user)


@router.get("/users/list/", response_model=List[schemas.User], summary="获取用户列表")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)


@router.get("/users/{user_id}", response_model=schemas.User, summary="根据用户id查询信息")
def read_user(user_id: int, db: Session = Depends(get_db)):
    # 获取当前id的用户信息
    db_user = crud.get_user(db, user_id=user_id)
    # 如果没有信息，提示用户不存在
    if db_user is None:
        raise HTTPException(status_code=404, detail="未找到用户")
    return db_user


@router.delete("/users/{user_id}", summary="根据用户id删除用户")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    # 获取当前id的用户信息
    db_user = crud.get_user(db, user_id=user_id)
    # 如果没有信息，提示用户不存在
    if db_user is None:
        raise HTTPException(status_code=404, detail="未找到该用户")
    crud.delete_user(db=db, user_id=user_id)
    return {'code': 1, 'msg': '删除成功'}


@router.post("/users/{user_id}/items/", response_model=schemas.Item, summary="根据用户id创建item")
def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    # 创建该用户的items
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@router.get("/items/list/", response_model=List[schemas.Item], summary="获取用户item列表")
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_items(db=db, skip=skip, limit=limit)


@router.put("/items/{user_id}/update/", summary="根据用户id更新item数据")
def update_items(user_id: int, item: schemas.Item, db: Session = Depends(get_db)):
    return crud.update_items(db=db, item=item, user_id=user_id)
