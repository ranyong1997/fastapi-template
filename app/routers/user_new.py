#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/26 16:07
# @Author  : 冉勇
# @Site    : 
# @File    : user_new.py
# @Software: PyCharm
# @desc    : 用户路由相关
from typing import List
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.config.database import SessionLocal, engine
from app.crud import user_crud as crud
from app.models import user_new as models
from app.schemas import user_new as schemas

models.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/user_new", tags=['用户接口_new'])


# 依赖
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.post("/users/", response_model=schemas.User, summary="创建用户")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 根据email查找用户
    db_user = crud.get_user_by_email(db, email=user.email)
    # 如果用户存在，提示该邮箱已经被注册
    if db_user:
        raise HTTPException(status_code=400, detail="电子邮件已注册")
    # 返回创建的user对象
    return crud.create_user(db=db, user=user)


@router.get("/users/", response_model=List[schemas.User], summary="获取用户数量")
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


@router.post("/users/{user_id}/items/", response_model=schemas.Item, summary="创建用户item")
def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    # 创建该用户的items
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@router.get("/items/", response_model=List[schemas.Item], summary="查询用户item")
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_items(db, skip=skip, limit=limit)


@router.delete("/users/{user_id}", response_model=schemas.Item, summary="删除用户")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    # 获取当前id的用户信息
    db_user = crud.get_user(db, user_id=user_id)
    # 如果没有信息，提示用户不存在
    if db_user is None:
        raise HTTPException(status_code=404, detail="未找到用户")
    crud.delete_user_item(db=db)
    return db_user
