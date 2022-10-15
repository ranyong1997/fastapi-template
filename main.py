#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/12 15:16
# @Author  : 冉勇
# @Site    : 
# @File    : server.py
# @Software: PyCharm
# @desc    : 项目启动文件
import uvicorn
from app.config import settings

if __name__ == '__main__':
    uvicorn.run("app.server:app",
                reload=True,
                reload_dirs=['app'],
                host=settings.server_host,
                port=settings.server_port)
    # reload_dirs 只监视该目录的代码变化进行热更新
