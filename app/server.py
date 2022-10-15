#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/10 15:07
# @Author  : 冉勇
# @Site    : 
# @File    : server.py
# @Software: PyCharm
# @desc    : 配置文件
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from .routers import custom_docs, api_router
from .config import settings
from .views import views_router
from . import app, init_logging

# 实例化fastapi对象
app = FastAPI(docs_url=None,
              redoc_url=None,
              title=settings.project_title,
              description=settings.project_description,
              version=settings.project_version)

# 挂载静态文件目录
app.mount(settings.static_url_prefix, StaticFiles(directory=settings.static_dir))
# 用户上传文件
app.mount(settings.media_url_prefix, StaticFiles(directory=settings.media_dir))

# 自定义docs界面
custom_docs(app)

# 挂载api路由
app.include_router(api_router)

# 挂载view路由
app.include_router(views_router)

# 挂载loguru路由
logger = init_logging()
logger.bind(name=None).opt(ansi=True).success(
    f"fastapi 正在运行环境: <blue>{settings.FASTAPI_ENV} 网址: http://localhost:8000/docs</blue>")
logger.bind(name=None).success(settings.BANNER)

# async def send_email(email: str, msg: str):
#     print(f"send email to {email},{msg=},start at:{datetime.datetime.now()}")
#     await asyncio.sleep(1)
#
#
# class Scheduler:
#     def __init__(self, store=None):
#         self.store = store  # 未来可能要把任务持久化
#         self.bgt = None  # BackgroundTasks
#         self.func = None  # 任务函数
#         self.task = None  # 实际执行的任务
#         self.args = []
#         self.kwargs = {}
#
#     async def __call__(self, bgt: BackgroundTasks):
#         self.bgt = bgt
#         return self
#
#     def bind(self, func, *args, **kwargs):
#         self.func = func
#         self.args = args
#         self.kwargs = kwargs
#         return self
#
#     async def run(self):
#         if self.task is None:
#             self.task = self.func
#         self.bgt.add_task(self.task, *self.args, **self.kwargs)
#
#     # 延时任务
#     async def delay(self, seconds: int):
#         async def task_delay(*args, **kwargs):
#             await asyncio.sleep(seconds)
#             await self.func(*args, **kwargs)
#             print(f"task run at {datetime.datetime.now()},delay:{seconds} seconds")
#
#         self.task = task_delay
#         await self.run()
#
#     # 定时任务
#     async def at(self, time_point: datetime.datetime):
#         async def task_at(*args, **kwargs):
#             while True:
#                 await asyncio.sleep(0.1)
#                 if datetime.datetime.now() >= time_point:
#                     break
#             await self.func(*args, **kwargs)
#             print(f"task run at {datetime.datetime.now()}")
#
#         self.task = task_at
#         await self.run()
#
#     # 周期任务
#     async def every(self, seconds: int, end_time: Optional[datetime.datetime] = None, count: Optional[int] = None):
#         async def task_every(*args, **kwargs):
#             task_count = 0
#             next_time = datetime.datetime.now()
#             while True:
#                 if datetime.datetime.now() >= next_time:
#                     next_time += datetime.timedelta(seconds=seconds)
#                     await self.func(*args, **kwargs)
#                     task_count += 1
#                     while datetime.datetime.now() <= next_time:
#                         await asyncio.sleep(0.1)
#                 if end_time is not None and datetime.datetime.now() >= end_time:
#                     print(f"break at {datetime.datetime.now()},{end_time}")
#                     break
#                 if count is not None and task_count >= count:
#                     print(f"break at {datetime.datetime.now()},{count}")
#                     break
#
#         self.task = task_every
#         await self.run()
#
#     async def cron(self):
#         """
#         arq
#         apscheduler
#         celery
#         :return:
#         """
#         pass
#
#
# # 后台任务 用于发送验证码、邮件
# @app.get("/task", summary="简单演示")
# def task(bgt: BackgroundTasks):
#     bgt.add_task(send_email, "123@qq.com", "hello")
#     return {"now": datetime.datetime.now()}
#
#
# @app.get("/class", summary="封装成依赖项类")
# async def task(s: Scheduler = Depends(Scheduler())):
#     # 后台立即执行
#     # await s.bind(send_email, "123@qq.com", "hello").run()
#     # 延时执行
#     # await s.bind(send_email, "123@qq.com", "hello delay").delay(3)
#     # new_time = datetime.datetime.now() + datetime.timedelta(seconds=5)
#     # 固定时间点执行
#     # await s.bind(send_email, "123@qq.com", "hello at").at(new_time)
#     # 周期执行 每2秒执行一次，执行3次
#     # await s.bind(send_email, "123@qq.com", "hello every").every(2, count=3)
#     # 周期执行 每2秒执行一次，执行5秒
#     end_time = datetime.datetime.now() + datetime.timedelta(seconds=5)
#     await s.bind(send_email, "123@qq.com", "hello every").every(2, end_time=end_time)
#     return {"now": datetime.datetime.now()}
