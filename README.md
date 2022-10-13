# Fastapi-Template

[![](https://img.shields.io/badge/Python-3.8-red.svg)](https://www.python.org/downloads)[![](https://img.shields.io/badge/FastAPI-0.75-yellowgreen.svg)](https://fastapi.tiangolo.com/)

## 目录结构

```
├── app	            # 项目框架核心，做整体项目逻辑
│   ├── config              # 配置相关
│   │   ├── __init__.py
│   │   └── config.py 
│   ├── dependencies         # 依赖相关
│   │   ├── init_.py
│   │   └── auth.py
│   ├── libs         # 数据库相关 
│   │   ├── init_.py
│   │   ├── data.json
│   │   └── db_lib.py
│   ├── models         # 模型相关 
│   │   ├── init_.py
│   │   └── user.py
│   ├── routers         # 路由相关 
│   │   ├── init_.py
│   │   ├── dev.py
│   │   ├── docs.py
│   │   └── user.py
│   ├── schemas         # 设计模型
│   │   ├── init_.py
│   │   └── user.py
│   ├── utils         # 工具相关
│   │   ├── init_.py
│   │   └── has_lib.py
│   ├── views         # 试图相关
│   │   ├── init_.py
│   │   └── home.py
│   ├── websocket         # 协议相关
│   │   └── init_.py
│   ├── __init__.py
│   └── server.py
├── deploy	        # 项目部署
├── logs	        # 项目日志
├── media	        # 用户上传文件
├── static           # 静态资源
├── .env	        # 虚拟环境
├── main	        # 项目启动文件
├── .gitignore      # 忽略文件
├── README      # README文档
└── requirement      # 依赖相关包
```

---
*后端*

* Python Web 框架：FastAPI
* 数据库：MySQL
* ORM：SQLAlchemy

---
*前端*

* 框架：Vue
* 管理界面：ElementUI

---

### 基本要求

* Python: 3.7.x
* MySQL: 5.7.x
* Node: 12.13.x
* Vue: 3.x

---

### 安装

*后端*

```
1: 安装Python >= 3.7.x，创建虚拟环境
2: 安装MySQL 8.0.x
```

*前端*

```
1: 安装Node版本 12.13.x 和 vue-cli
```

## 快速上手

### 1、下载代码

```python
git@github.com:ranyong1997/fastapi-template.git
```

### 2、创建python虚拟环境

> 本项目使用的是 python3.8，推荐也用这个版本 其他版本，可能需要您自行处理一些版本间的差异问题

### 3、安装依赖

```python
cd fastapi-template
pip3 install -r requirements.txt
```
### 4、启动mysql等基础设施
> 如果不习惯使用 docker 也可以自己手动搞定这些
版本要求：mysql 8.0.27 redis 6.2.7
其他版本，没测试过，不保证能跑起来。
```dockerfile
docker-compose -f docker-compose.local.yml up -d
```
### 5、迁移数据库
>pass
### 6、运行项目
```python
python main.py
```
已实现功能:
- [x] 哈希加密
- [x] JWT认证 
- [x] swagger文件加载过慢
- [X] 基础接口调试
- [X] 开发接口调试/隐藏

待实现功能:
- [ ] 使用loguru日志模块
- [ ] 使用SQLAlchemy数据库
## 截图
![image-20221013164104847](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202210131641293.png)