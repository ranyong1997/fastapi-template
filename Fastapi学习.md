![image](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211110952477.png)

> *FastAPI 框架，高性能，易于学习，高效编码，生产可用*

官方文档： [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com/)

FastAPI 是一个用于构建 API 的现**convert_underscores**代、快速（高性能）的 web 框架，使用 Python 3.6+ 并基于标准的 Python 类型提示。

关键特性:

- **快速**：可与 **NodeJS** 和 **Go** 比肩的极高性能（归功于 Starlette 和 Pydantic）。[最快的 Python web 框架之一](https://fastapi.tiangolo.com/zh/#_11)。
- **高效编码**：提高功能开发速度约 200％ 至 300％。
- **更少 bug**：减少约 40％ 的人为（开发者）导致错误。
- **智能**：极佳的编辑器支持。处处皆可自动补全，减少调试时间。
- **简单**：设计的易于使用和学习，阅读文档的时间更短。
- **简短**：使代码重复最小化。通过不同的参数声明实现丰富功能。bug 更少。
- **健壮**：生产可用级别的代码。还有自动生成的交互式文档。
- **标准化**：基于（并完全兼容）API 的相关开放标准。

## 安装FastApi

```python
pip3 install fastapi
pip3 install unicorn
```

**验证**

![202211031610474](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211110954540.png)

## 第一个程序：Hello World

```python
from fastapi import FastAPI  # 导入FastAPI类
import uvicorn  # 导入uvicorn,ASGI容器

app = FastAPI()  # 创建应用实例


@app.get('/')  # 定义路由路径
async def root():  # 定义路径操作函数
    return {'message': 'Hello,World'}  # 返回 Hello,World 信息到浏览器上


if __name__ == '__main__':
    uvicorn.run(app=app)  # 在ASGI容器中启动FastAPI应用实例
```

## FastAPI框架构成

![202211031638161](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211110954642.jpg)

## 请求参数

### 请求原理

 ![202211031655678](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211110955738.jpg)

## 路径参数

- 请求URL：http://127.0.0.1:8000/items/参数1
- 使用装饰器：@app.get('/items/{id_value}')
- 简单参数
- 有类型参数

```python
from fastapi import FastAPI  # 导入FastAPI类
import uvicorn  # 导入uvicorn,ASGI容器

app = FastAPI()  # 创建应用实例


@app.get("/items{item_id}")  # 注册路由路径，使用{}定义路径参数，参数名为item_id
async def read_item(item_id):  # 路径操作函数中定义同名的路径参数
    print(item_id)  # 打印路径参数值
    return {'item_id': item_id}  # 用return 关键字，将得到的参数返回给浏览器端


if __name__ == '__main__':
    uvicorn.run(app=app)  # 在ASGI容器中启动FastAPI应用实例
```

## 查询参数 

- http://127.0.0.1:8000/items?skip=0&limit=10,则'?'后跟skip=0、limit=10两个查询参数。
- 可选参数
- 必选参数

```python
from fastapi import FastAPI  # 导入FastAPI类
import uvicorn  # 导入uvicorn,ASGI容器

app = FastAPI()  # 创建应用实例


items = [{'name': '泰迪'}, {'name': '柯基'}, {'name': '加菲'}, {'name': '斗牛'}, {'name': '英短'}]


@app.get('/items/')  # 注册路由路径,未定义路径参数
async def read_item(skip: int = 0, limit: int = 10):  # 定义了两个参数，参数类型int
    print('参数skip:', skip)
    print('参数limit', limit)
    return items[skip:skip + limit]  # 用下标方式从列表items中取出数据


if __name__ == '__main__':
    uvicorn.run(app=app)  # 在ASGI容器中启动FastAPI应用实例
```

## 请求体

- 使用浏览器等客户端访问Web服务器端时，会发送请求数据；另外web服务器端处理完数据后，会返回响应数据给客户端。
- 在FastAPI框架中，客户端发送给服务器端的受数据模型约束的请求数据称为请求体。请求体默认时JSON格式，方便前端开发人员和后端开发人员共享调用数据。

### 定义请求体的数据模型

- FastAPI里的所有请求体实现对象，通过Pydantic库里的BaseModel类进行模型类的继承定义实现
- 首先，从Pydantic中导入BaseModel类，然后，继承BaseModel类定义数据模型类，再使用Python标准数据类型定义数据模型的字段，这样就完成了数据模型类的创建。

### 数据模型示例代码

```python
from typing import Optional
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel  # 导入基础模型类


class Item(BaseModel):  # 定义数据模型类，继承自BaseModel类
    name: str  # 定义字段name，类型str
    description: Optional[str] = None  # 定义可选字段description，类型str
    price: float  # 定义字段price，类型float
    tax: Optional[float] = None  # 定义可选字段tax，类型float
```

### 同时使用路径参数、查询参数和请求体

```python
from typing import Optional
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel  # 导入基础模型类

app = FastAPI()


class Item(BaseModel):  # 定义数据模型类，继承自BaseModel类
    name: str  # 定义字段name，类型str
    description: Optional[str] = None  # 定义可选字段description，类型str
    price: float  # 定义字段price，类型float
    tax: Optional[float] = None  # 定义可选字段tax，类型float


@app.post('/items/{item_id}')  # 注册路由，定义路径参数item_id
async def create_item(  # 定义路径操作函数
        item_id: int,  # 定义路径参数，类型int
        item: Item,  # 定义请求体对象，类型是数据模型
        q: Optional[str] = None  # 定义可选查询参数，类型str
):
    result = {"item_id": item_id, **item.dict()}  # 将路径参数和请求体参数组合为数据对象
    if q:
        result.update({"q": q})  # 如果传入了查询参数，则更新查询参数
    return result  # 返回组合好的数据对象


if __name__ == '__main__':
    uvicorn.run(app=app)  # 在ASGI容器中启动FastAPI应用实例
```

## 表单和文件

- 文件上传也是一种特殊的表单提交请求数据方式，对应的数据是文件流，而不是格式化的数据。

```python
import uvicorn
from fastapi import FastAPI, Form  # 导入Form对象

app = FastAPI()


@app.post("/login/")  # 注册路由路径
async def login(  # 定义路径操作参数
        username: str = Form(...),  # 定义查询参数，数据类型是str，初始值是Form
        password: str = Form(...)  # 定义查询参数，数据类型是str，初始值是Form
):
    return {"username": username}


if __name__ == '__main__':
    uvicorn.run(app=app)  # 在ASGI容器中启动FastAPI应用实例
```

## 文件上传

- FastApi对文件上传的支持，也依赖第三方库python-multipart。与使用Body类、Form类的方法类似，上传文件时，需要引入File类。

```python
pip3 install python-multipart
```

```python
import uvicorn
from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post('/files/')  # 注册路由路径
async def create_file(  # 定义路径操作函数，第一种上传方式
        file: bytes = File(...)  # 定义文件参数，数据类型为bytes，初始值时File
):
    return {"file_size": len(file)}  # 返回文件大小


@app.post('/uploadfile/')  # 注册路由路径
async def create_upload_file(  # 定义路径操作函数，第二种上传方式
        file: UploadFile = File(...)  # 定义文件参数，数据类型为UploadFile，初始值为File
):
    return {'filename': file.filename}  # 返回原始文件名


if __name__ == '__main__':
    uvicorn.run(app=app)  # 在ASGI容器中启动FastAPI应用实例
```

## 认识响应

### 响应原理

![UML 图 (2)](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211041022756.jpg)

### 响应模型

- 响应模型，指在处理响应数据时，也可以将响应数据转换成Pydantic数据模型实例，以保证响应数据得规范性。同时，响应数据模型在API文档中体现为JSON模式，也增加了文档的可读性及接口的标准化。

### 定义响应模型

```python
from optparse import Option
from pydantic import BaseModel


# 请求模型
class UserIn(BaseModel):  # 定义数据模型
    username: str  # 定义字段用户名,类型str
    password: str  # 定义字段密码,类型str
    email: str  # 定义邮箱,类型str
    full_name: Option[str] = None  # 定义可选字段全名,类型str


# 响应模型
class UserOut(BaseModel):  # 定义数据模型
    usernmae: str  # 定义字段用户名,类型str
    email: str  # 定义邮箱,类型str
    full_name: Option[str] = None  # 定义可选字段全名,类型str
```

### 使用响应模型返回数据

```python
import uvicorn
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


# 请求模型
class UserIn(BaseModel):  # 定义数据模型
    username: str  # 定义字段用户名,类型str
    password: str  # 定义字段密码,类型str
    email: str  # 定义邮箱,类型str
    full_name: Optional[str] = None  # 定义可选字段全名,类型str


# 响应模型
class UserOut(BaseModel):  # 定义数据模型
    username: str  # 定义字段用户名,类型str
    email: str  # 定义邮箱,类型str
    full_name: Optional[str] = None  # 定义可选字段全名,类型str


@app.post('/user/', response_model=UserOut)  # 注册路由路径,设置响应模型为UserOut
async def create_user(user: UserIn):  # 设置请求模型为UerIn
    return user  # 返回请求数据


if __name__ == '__main__':
    uvicorn.run(app=app)  # 在ASGI容器中启动FastAPI应用实例
```

### 内容响应类

FastAPI中内置了以下响应类：

- 纯文本响应（PlainTextResponse）
- HTML响应（HTML Response）
- 重定向响应（RedirectResponse）
- JSON数据响应（JSONResponse）
- 通用响应（Response）
- 流响应（StreamingResponse）
- 文件响应（FileResponse）

## 深入请求和响应

### 在请求中使用类

- 利用类可以为服务器端请求数据处理，提供更加方便地使用功能。这里地类包括了查询参数类、路径参数类、Cookie参数类、Header参数类、Field类等。
- FastAPI中提供了查询参数类Query，使用Query类能够对参数做更多细微的控制。

```python
import uvicorn
from typing import Optional
from fastapi import FastAPI, Query, Path  # 导入query、path包

app = FastAPI()

# 查询参数中使用Query类
@app.get('/')
async def read_items(q: Optional[str] = Query(None, max_length=10)):  # 使用Query设置规则
    return {"q": q}  

# 在路径参数中使用Path类
@app.get('/items/{item_id}')
async def read_items(item_id: int = Path(    # 定义路径参数，设置默认值为Path类
            ...,    # 路径参数是必选参数
            description='项目ID是路径的一部分')  # 设置描述信息
):
    return {"item_id": item_id}


if __name__ == '__main__':
    uvicorn.run(app=app)  # 在ASGI容器中启动FastAPI应用实例
```

### 请示中的其他类

- Cookie参数类

```python
import uvicorn
from typing import Optional
from fastapi import FastAPI, Cookie  # 导入Cookie类

app = FastAPI()


@app.get('/items/')
async def read_items(user_id: Optional[str] = Cookie(None)):  # 定义Cookie参数，默认为空
    return {"user_id": user_id}


if __name__ == '__main__':
    uvicorn.run(app=app)  # 在ASGI容器中启动FastAPI应用实例

```

- Header参数类

```python
import uvicorn
from typing import Optional
from fastapi import FastAPI, Header  # 导入Header类

app = FastAPI()


@app.get('/items/')
async def read_items(user_agent: Optional[str] = Header(None)):  # 定义Header参数，类型为str
    return {"User-Agent": user_agent}   # 返回Usage-Agent的值


if __name__ == '__main__':
    uvicorn.run(app=app)  # 在ASGI容器中启动FastAPI应用实例
```

- Field类

  - 数据模型字段的规则设置

    ```python
    import uvicorn
    from typing import Optional
    from fastapi import FastAPI, Body
    from pydantic import BaseModel, Field  # 导入Field类
    
    app = FastAPI()
    
    
    class Item(BaseModel):  # 定义数据模型类，继承自BaseModel
        name: str  # 定义字段，类型为str
        description: Optional[str] = Field(  # 定义可选字段，类型为str，Field类提供规则设置
            None,  # 设置字段默认值
            title='一大段说明信息',  # 设置字段标题
            max_length=300  # 设置字段内容最大长度
        )
        price: float = Field(  # 定义字段，类型为float
            ...,  # 设置必填参数
            gt=0,  # 设置验证规则，数值大于0
            description="单价必须大于0"  # 设置字段描述信息
        )
        tax: Optional[float] = None  # 定义可选字段，类型float
    
    
    @app.post("/items/{item_id}")
    async def update_item(item_id: int, item: Item = Body(...)):
        return {"item_id": item_id, "item": item}
    
    
    if __name__ == '__main__':
        uvicorn.run(app=app)  # 在ASGI容器中启动FastAPI应用实例
    ```

  - 配置类设置统一的元数据

    ```python
    import uvicorn
    from typing import Optional
    from fastapi import FastAPI, Body
    from pydantic import BaseModel, Field  # 导入Field类
    
    app = FastAPI()
    
    
    class Item(BaseModel):  # 定义数据模型类，继承自BaseModel
        name: str  # 定义字段，类型为str
        description: Optional[str] = None  # 定义可选字段，类型为str
        price: float  # 定义字段，类型为float
        tax: Optional[float] = None  # 定义可选字段，类型float
    
        class Config:
            schema_extra = {
                "example": {
                    'name': '猫',
                    'description': '这是一个非常不错的项目',
                    'price': 3.15,
                    'tax': 3.2
                }
            }
    
    
    @app.post("/items/{item_id}")
    async def update_item(item_id: int, item: Item):
        return {"item_id": item_id, "item": item}
    
    
    if __name__ == '__main__':
        uvicorn.run(app=app)  # 在ASGI容器中启动FastAPI应用实例
    ```

  - 用Field类设置样例数据

    ```python
    import uvicorn
    from typing import Optional
    from fastapi import FastAPI, Body
    from pydantic import BaseModel, Field  # 导入Field类
    
    app = FastAPI()
    
    
    class Item(BaseModel):  # 定义数据模型类，继承自BaseModel
        name: str = Field(..., example='三酷猫')  # 使用Field对象的example
        description: Optional[str] = Field(None, example='这是一个不错的项目')
        price: float = Field(..., example=3.15)
        tax: Optional[float] = Field(None, example=3.2)
    
    
    @app.post("/items/{item_id}")
    async def update_item(item_id: int, item: Item):
        return {"item_id": item_id, "item": item}
    
    
    if __name__ == '__main__':
        uvicorn.run(app=app)  # 在ASGI容器中启动FastAPI应用实例
    ```

- Request类

```python
import uvicorn
from fastapi import FastAPI, Request

app = FastAPI()


@app.get('/host/')
def read_root(request: Request):
    client_host = request.client.host
    return {'客户端主机地址': client_host}


if __name__ == '__main__':
    uvicorn.run(app=app)  # 在ASGI容器中启动FastAPI应用实例
```

### 自定义响应数据

- 自定义Cookie数据

  ```python
  import uvicorn
  from fastapi import FastAPI
  from fastapi.responses import JSONResponse
  
  app = FastAPI()
  
  
  @app.post('/cookie/')
  def create_cookie():
      content = {'message': '三酷猫 like cookies'}  # 创建响应数据
      response = JSONResponse(content=content)  # 创建响应类实例
      response.set_cookie(key='user_id', value='9527')  # 设置cookie
      return response  # 返回响应类实例
  
  
  if __name__ == '__main__':
      uvicorn.run(app=app)  # 在ASGI容器中启动FastAPI应用实例
  ```

  ![image-20221104162653383](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211041626439.png)

- 自定义Header数据

  ```python
  import uvicorn
  from fastapi import FastAPI
  from fastapi.responses import JSONResponse
  
  app = FastAPI()
  
  
  @app.get('/headers/')  # 注册路由路径
  def get_headers():  # 定义路径操作函数
      content = {'message': 'Hello，三酷猫'}  # 创建响应内容数据
      headers = {'X-three-cool-cat': 'miao-miao-miao',  # 自定义Header
                 'User-Agent': 'threecoolcat Browser'}  # 内置自定义Header数据
      response = JSONResponse(content=content, headers=headers)  # 创建响应类实例
      return response  # 返回响应类实例
  
  
  if __name__ == '__main__':
      uvicorn.run(app=app)  # 在ASGI容器中启动FastAPI应用实例
  ```

  ![image-20221104163311529](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211041633608.png)

- 自定义响应状态码

  - 默认状态码

    ```python
    import uvicorn
    from fastapi import FastAPI
    
    app = FastAPI()
    
    
    @app.get('/items/', status_code=201)  # 注册路由路径，设置默认状态码
    async def create_item(name: str):  # 定义路径操作函数
        return {'name': name}
    
    
    if __name__ == '__main__':
        uvicorn.run(app=app)  # 在ASGI容器中启动FastAPI应用实例
    ```

  - 自定义状态码

    ```python
    import uvicorn
    from fastapi import FastAPI, Response, status
    
    app = FastAPI()
    
    items = {'1': 'cat'}  # 模拟数据
    
    
    @app.get('/items/{item_id}', status_code=200)  # 默认响应状态码
    def get_or_create_item(item_id: str, response: Response):  # 使用Response类的实例
        if item_id not in items:
            items[item_id] = 'dog'
            response.status_code = status.HTTP_201_CREATED  # 自定义的响应状态码
        return items[item_id]
    
    
    if __name__ == '__main__':
        uvicorn.run(app=app)  # 在ASGI容器中启动FastAPI应用实例
    ```

  

## 异常处理

> 异常处理，是编程语言或计算机硬件里的一种机制，用于捕获并处理软件或运行系统中出现的异常信息。这些异常信息可能是因为访问了不存在的资源，也可能是因为代码报错的需要，而主动被触发并抛出。

### 异常类HttpException

```python
import uvicorn
from fastapi import FastAPI, HTTPException

app = FastAPI()
items = {"1": "cat"}    # 定义模拟数据


@app.get("/items/{item_id}")    # 注册路由路径，定义路径参数
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=401, detail="未找到指定项目")  # 抛出异常
    return {"item": items[item_id]}


if __name__ == '__main__':
    uvicorn.run(app=app)  # 在ASGI容器中启动FastAPI应用实例
```

### 全局异常处理器

```python
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()


class MyException(Exception):  # 自定义异常类，继承自Exception
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(MyException)
async def my_exception_handler(  # 定义异常处理函数
        request: Request,  # 请求类实例
        exc: MyException):  # 异常类实例
    return JSONResponse(  # 返回相应类实例
        status_code=418,  # 响应状态码
        content={"message": f"OMG,{exc.name}又迷路了"})  # 状态文本


@app.get("/cats/{name}")  # 注册路由路径，定义路径参数
async def find_cats(name: str):
    if name == '三酷猫':
        raise MyException(name=name)  # 抛出自定义异常
    return {"cat": name}


if __name__ == '__main__':
    uvicorn.run(app=app)  # 在ASGI容器中启动FastAPI应用实例
```

![image-20221104170803237](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211041708945.png)

### 内置异常处理器

```python
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse  # 导入普通文本相应类
from starlette.exceptions import HTTPException as StarletteHTTPException  # 使用别名导入

app = FastAPI()


@app.exception_handler(StarletteHTTPException)  # 注册系统异常
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)  # 注册系统异常
async def validation_exception_handler(request, exc):  # 覆盖系统异常处理器，重写方法
    return PlainTextResponse(str(exc), status_code=400)


@app.get("/items/{item_id}")    # 注册路由路径，定义路径参数
async def read_item(item_id: int):
    if item_id == 3:    # 如果 item_id == 3时，抛出异常HTTPException
        raise HTTPException(status_code=418, detail="禁止填入3")
    return {"item_id": item_id}


if __name__ == '__main__':
    uvicorn.run(app=app)  # 在ASGI容器中启动FastAPI应用实例
```

![image-20221104180436273](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211041804072.png)

## 中间件

![UML 图 (2)](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211070940107.jpg)

> FastAPI中间件实际上是服务器端得一种函数，在每个请求处理之前被调用，又在每个响应返回给客户端之前被调用。中间件提供了服务器端与客户端通信得预处理功能，接收客户端提交得请求数据，发送服务器端得响应数据。

FastAPI主要提供如下详细功能

- Web服务器端通过中间件接收客户端传过来得每个请求数据；
- 对接收的请求数据执行自定义逻辑代码操作；
- 将请求数据传递给路径操作函数；
- 接收路径函数返回的响应数据；
- 对响应数据执行自定义逻辑代码操作；
- 返回响应数据给客户端；

### 自定义中间件

> 自定义中间件的方式，是先定义一个中间件函数，然后在这个函数上增加装饰器@app.middleware("http")，该函数的参数包括了请求Request的实例request和处理过程回调函数call_next。自定义中间件函数的工作流程如下：

- 参数call_next接收请求类实例
- 该函数把请求数据传递给相应的路径操作函数
- 返回路径操作函数生成的响应数据
- 在返回响应数据给客户端之前，进一步修改响应

```python
import uvicorn
import time
from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")  # 使用装饰器，将下一行函数注册为中间件函数
async def add_process_time_header(request: Request, call_next):  # 定义中间件函数
    # 此处在路径操作收到请求之前执行
    start_time = time.time()  # 记录时间点
    response = await call_next(request)  # 获取响应类实例
    # 此处在生成响应数据返回之前执行
    process_time = time.time() - start_time  # 计算处理时间
    response.headers['X-Process-Time'] = str(process_time)  # 修改响应Header
    return response  # 返回响应实例


if __name__ == '__main__':
    uvicorn.run(app=app)  # 在ASGI容器中启动FastAPI应用实例
```

### 调用CORS中间件

> CORS(跨域资源共享)

```python
import uvicorn
from fastapi.middleware.cors import CORSMiddleware  # 导入CORSMiddleware
from fastapi import FastAPI

app = FastAPI()

origins = [  # 定义可用域列表
    'http://localhost',
    'http://localhost:8080'
]
app.add_middleware(  # 在应用上添加中间件
    CORSMiddleware,  # 内置中间件类
    allow_origins=origins,  # 参数1 可用域列表
    allow_credentials=True,  # 参数2 允许cookie，是
    allow_methods=['*'],  # 参数3 允许的方法，全部
    allow_headers=['*']  # 参数4，允许的Header，全部
)


@app.get('/')  # 注册路由路径
async def main():
    return {'message': 'Hello,world'}


if __name__ == '__main__':
    uvicorn.run(app=app)  # 在ASGI容器中启动FastAPI应用实例
```

| 项目名称           | 项目说明                                                     |
| :----------------- | :----------------------------------------------------------- |
| allow_origins      | 允许跨域请求的资源列表，例如：['https://a.org','https://b.org']，使用['*']代表允许使用任何源 |
| allow_origin_regex | 正则表达式字符串，使用正则表达式匹配的源允许跨域请求，例如：'https://.*\.example\.org' |
| allow_methods      | 允许跨域请求的HTTP方法列表，默认为['GET']，可以使用['*']来允许所有标准方法 |
| allow_headers      | 允许跨域请求的HTTP请求头列表，默认为[]，可以使用['*']代表允许使用的请求头。Accept、Accept-Language、Content-Language以及Content-Type请求头默认允许CORS请求 |
| allow_credentials  | 指示跨域请求支持cookies，默认是False，若设置为Tru时，则allow_origins不能设定为['*']，必须指定源 |
| expose_headers     | 指示可以被浏览器访问的响应信息头，默认为[]                   |
| max_age            | 设定浏览器缓存CORS响应的最长时间，单位为秒，默认为600        |

### 调用UnicornMiddleware中间件

```python
from fastapi import FastAPI
from unicorn import UnicornMiddleware	# 导入中间件UnicornMiddleware

app = FastAPI()
app.add_middleware(UnicornMiddleware,some_config='cool')	# 添加UnicornMiddleware中间件
```

> 上述代码中，app.add_middleware()接收UnicornMiddleware中间件作为第一个参数，some_config参数可以根据实例需求传递任何参数值。

### 调用HTTPSRedirectMiddleware中间件

> 强制使用HTTPS协议来访问服务器

```python
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware  # 导入中间件

app = FastAPI()

app.add_middleware(HTTPSRedirectMiddleware)	# 添加中间件，无其他参数


@app.get('/')
async def main():
    return {'message': 'hello world'}


if __name__ == '__main__':
    uvicorn.run(app=app)  # 在ASGI容器中启动FastAPI应用实例
```

### 调用TrustedHostMiddleware中间件

> 设置域名访问白名单

```python
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware  # 导入中间件

app = FastAPI()

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=['example.com', '*.example.com']  # 添加中间件
    # TrustedHostMiddleware, allowed_hosts=['*']  # 添加中间件,['*'] 为所有人可访问
)


@app.get('/')
async def main():
    return {'message': 'Hello,World'}


if __name__ == '__main__':
    uvicorn.run(app=app)  # 在ASGI容器中启动FastAPI应用实例
```

![202211071058403](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211110956981.png)

### 调用GZipMiddleware中间件

> 压缩响应数据

```python
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware  # 导入中间件

app = FastAPI()

app.add_middleware(GZipMiddleware, minimum_size=1000)  # 添加中间件，设置压缩参数


@app.get('/')
async def main():
    return 'somebigcontent'


if __name__ == '__main__':
    uvicorn.run(app=app)  # 在ASGI容器中启动FastAPI应用实例
```

> 该中间件有一个参数minimum_size，其作用是设置数据包的最小值，也就是说，只有当需要传递的数据长度大于这个值时，才会使用GZip压缩，否则将会传递原始数据。

## 依赖注入

> 当一个类调用另外一个类时，允许另外一个类的代码功能自由调整，而不影响调用类的使用。

### 使用函数实现依赖注入

```python
import uvicorn
from fastapi import FastAPI, Depends
from typing import Optional

app = FastAPI()


async def dep_params(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, 'skip': skip, 'limit': limit}


@app.get("/items/")  # 注册路由路径
async def read_items(  # 定义路径操作函数
        commons: dict = Depends(dep_params)):  # 用Depends()方法指定依赖函数
    return commons  # 返回依赖项结果


@app.get("/users/")  # 注册路由路径
async def read_users(  # 定义路径操作函数
        commons: dict = Depends(dep_params)):  # 用Depends()方法指定依赖函数
    return commons  # 返回依赖项结果


if __name__ == '__main__':
    uvicorn.run(app=app)  # 在ASGI容器中启动FastAPI应用实例
```

> 以上代码中，定义了一个依赖函数dep_params，此函数接收路径操作函数的所有参数，然后对参数进行处理，返回结果。在路径操作函数中，通过Depend()方法指定了依赖函数dep_params，而不是直接调用dep_params

### 使用类实现依赖注入

```python
import uvicorn
from fastapi import FastAPI, Depends
from typing import Optional

app = FastAPI()


class DepParams:  # 定义依赖类
    def __init__(self, q: Optional[str] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get("/items/")  # 注册路由路径
async def read_items(  # 定义路径操作函数
        params: DepParams = Depends(DepParams)):  # Depends()方法指定依赖类
    return params  # 返回依赖项的结果


if __name__ == '__main__':
    uvicorn.run(app=app)  # 在ASGI容器中启动FastAPI应用实例
```

### 依赖注入的嵌套

```python
import uvicorn
from fastapi import FastAPI, Depends, Cookie
from typing import Optional

app = FastAPI()


def query_extractor(  # 定义依赖函数1
        q: Optional[str] = None
):
    return q


def params_extractor(  # 定义依赖函数2
        q: str = Depends(query_extractor,use_cache=False),  # 定义依赖项q，use_cache=False 关闭依赖的缓存
        last_q: Optional[str] = Cookie(None)  # cookie参数
):
    if not q:  # 如果未传入参数q，则使用cookie中的参数
        return last_q
    return q


@app.get("/items/")  # 注册路由路径
async def read_query(  # 定义路径操作函数
        params: str = Depends(params_extractor, use_cache=False)  # 指定依赖函数，use_cache=False 关闭依赖的缓存
):
    return {"params": params}


if __name__ == '__main__':
    uvicorn.run(app=app)  # 在ASGI容器中启动FastAPI应用实例
```

> 若希望每次调用子依赖项时，都能执行该子依赖项函数，而不将其执行结果放入缓存，则可以在Depends()调用时，使用参数use_cache=False关闭缓存

### 在装饰器中使用依赖注入

```python
import uvicorn
from fastapi import FastAPI, Depends, Cookie, HTTPException, Header


async def verify_token(x_token: str = Header(...)):  # 定义依赖函数
    if x_token != 'my_token':  # 取值不合法时抛出异常
        raise HTTPException(status_code=400, detail='Token已失效')  # 没有返回值


async def check_userid(userid: str = Cookie(...)):  # 定义依赖函数
    if userid != '9527':  # 取值不合法时抛出异常
        raise HTTPException(status_code=400, detail='无效的用户')
    return userid  # 有返回值


app = FastAPI(dependencies=[Depends(verify_token), Depends(check_userid)])  # 依赖项列表


@app.get("/items/")  # 注册路由路径
async def read_items():
    return 'Hello World'


@app.get('/users/')  # 注册路由路径
async def read_users():
    return ['张三', '李四']


if __name__ == '__main__':
    uvicorn.run(app=app)  # 在ASGI容器中启动FastAPI应用实例
```

### 依赖项中的yield

> FastAPI支持在依赖函数中用yield代替return，这样就可以在路径操作函数执行完后，在执行一些其他操作。

```python
# 演示代码
from fastapi import Depends

async def dependency_a():   # 定义依赖函数A
    dep_a = generate_dep_a()
    try:
        yield dep_a
    finally:
        dep_a.close()


async def dependency_b(dep_a=Depends(dependency_a)):    # 定义依赖函数B，依赖项时函数A
    dep_b = generate_dep_a()
    try:
        yield dep_b
    finally:
        dep_b.close(dep_a)  # 操作完成后，关闭依赖对象A


async def dependency_c(dep_b=Depends(dependency_b)):        # 定义依赖函数C，依赖项时函数B
    dep_c = generate_dep_c()
    try:
        yield dep_c
    finally:
        dep_c.close(dep_b)  # 操作完成后，关闭依赖对象B
```

> 上面代码中，分别定义了3个依赖函数，这里称之为A、B、C，并且都是用了yield关键字，其中：
>
> A没有指定依赖项，执行完成后关闭自身；
>
> B指定了依赖项A，执行完成后关闭A；
>
> C指定了依赖项B，执行完成后关闭B。

### 以类的可调用实例

```python
import uvicorn
from fastapi import FastAPI, Depends

app = FastAPI()


class PetQueryChecker:  # 定义依赖类
    def __init__(self, pet_name: str):  # 构造方法
        self.pet_name = pet_name

    def __call__(self, q: str = ""):  # 使类的实例可调用
        if q:
            return self.pet_name in q  # 检测参数值
        return False


checkcat = PetQueryChecker('cat')  # 创建依赖类的可调用实例
checkdog = PetQueryChecker('dog')  # 创建依赖类的可调用实例


@app.get('/pet/')  # 注册路由路径
async def read_query_check(  # 定义路径操作函数
        has_cat: bool = Depends(checkcat),  # 依赖类，参数有cat
        has_dog: bool = Depends(checkdog)  # 依赖类，参数有dog
):
    return {"has_cat": has_cat, "has_dog": has_dog}


if __name__ == '__main__':
    uvicorn.run(app=app)  # 在ASGI容器中启动FastAPI应用实例
```

> 以上代码中,依赖类的定义中实现了方法`__call__()`,使这个类生成的实例也是可被Depends()方法调用的

## 数据库操作

### SQLAlchemy基本操作

#### 安装和连接

```shell
pip3 install sqlalchemy
```

![202211080945072](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211110956437.png)

```python
from sqlalchemy import create_engine  # 第一步，导入sqlalchemy组件包
from sqlalchemy.orm import sessionmaker

# 第二步，创建数据连接引擎
engine = create_engine("mysql+pymysql://user:password@server/dbname", encoding="utf-8",
                       echo=True, max_overflow=5)

# 创建本地会话
session = sessionmaker(autocommit=False, bind=engine)
# 回滚数据
session.rollback()
# 提交事物
session.commit()
# 关闭会话
session.close()
```

#### 定义数据模型

```python
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, create_engine

# 创建数据引擎
engine = create_engine("mysql+pymysql://user:password@server/dbname", encoding="utf-8",
                       echo=True, max_overflow=5)

session = sessionmaker(autocommit=False, bind=engine)  # 创建本地会话
Base = declarative_base()  # 创建模型基类


class User(Base):  # 定义数据模型类
    __tablename__ = "sql_test"  # 数据库中对应的表
    id = Column('id', Integer, primary_key=True)  # 定义字段id，整形
    user_name = Column('name', String(32), primary_key=True)  # 定义字段user_name,字符串型
    user_password = Column('password', String(64))  # 定义字段user_password,字符串型


Base.metadata.create_all(bind=engine)  # 在数据库中生成表结构
```

![202211091048333](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211110957879.png)

#### 定义关联关系

> 关联关系一般是指数据库中多个表的数据之间的相互依赖关系，常见的关联关系有：一对一，一对多，多对一，多对多。在SQLAlchemy中，使用relationship函数定义关联关系。常用参数如下：
>
> - argument：设置另外一个用于建立关联关系的数据模型类名称
> - backref：通过指定另外一个数据模型类的关联字段名，在一对多或者多对多之间建立双向关系
> - uselist：是否建立一对多关系，默认为True
> - remote_size：当外键是数据模型类自身时使用
> - secondary：用于指向多对多的中间表
> - back_populates：当属性为反向关系时，指定另一个数据模型类所对应的关联字段名
> - cascade：指定级联操作时得可用动作，比如，当删除主表数据时，与其关联得子表是否会同步删除对应数据

##### 一对一关系

```python
class User(Base):  # 定义数据模型类,用户
    __tablename__ = "user"  # 数据库中对应的表名
    id = Column(Integer, primary_key=True)  # id列，主键
    account = relationship('Account', uselist=False, backref='account')  # 账号字段
```

以上代码使用了参数useliback_populatesst=False，建立了一对一得关系

##### 一对多，多对一关系

**用户表**

|  id  | name |
| :--: | :--: |
|  1   | 张三 |
|  2   | 李四 |

**图书记录表**

|  id  |         book_name          | user_id | borrow_time           |
| :--: | :------------------------: | ------- | --------------------- |
|  1   |   《Python从入门到放弃》   | 1       | 2022-11-09 11：22：01 |
|  2   | 《Python从入门到项目实战》 | 1       | 2022-11-11 11：23：01 |
|  3   | 《Web3.0从入门到项目实战》 | 2       | 2022-11-09 11：24：01 |

```python
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey

# 创建数据引擎
engine = create_engine("mysql+pymysql://user:password@server/dbname", encoding="utf-8",
                       echo=True, max_overflow=5)

session = sessionmaker(autocommit=False, bind=engine)  # 创建本地会话
Base = declarative_base()  # 创建模型基类


class User(Base):  # 定义数据模型类,用户
    __tablename__ = "user"  # 数据库中对应的表名
    id = Column(Integer, primary_key=True)  # id列，主键
    name = Column('name', String(50))  # 定义字段name，字符串型
    bookrecords = relationship("BookRecords", backref='user')  # 图书列表字段，定义一对多关系


class BookRecords(Base):
    __tablename__ = 'book_record'  # 数据库中得表名
    id = Column(Integer, primary_key=True)  # id列，主键，顺序记录好唯一
    book_name = Column('book_name', String(50))  # 书名
    user_id = Column(Integer, ForeignKey('user.id'))  # user_id,主键


Base.metadata.create_all(bind=engine)  # 在数据库中生成表结构
```

![image-20221109114048016](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211091140695.png)

##### 多对多关系

> 多对多关系一般需要一个中间表，中间表的两个字段分别指向另外两张表中的字段

**用户表**

|  id  | name |
| :--: | :--: |
|  1   | 张三 |
|  2   | 李四 |

**行为表**

|  id  | name |
| :--: | :--: |
|  1   | 增加 |
|  2   | 删除 |
|  3   | 修改 |

**用户行为关联表**

|  id  | user_id | action_id |
| :--: | :-----: | :-------: |
|  1   |    1    |     1     |
|  2   |    1    |     2     |
|  3   |    2    |     1     |
|  4   |    2    |     3     |

```python
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey
from sqlalchemy.testing.schema import Table

# 创建数据引擎
engine = create_engine("mysql+pymysql://user:password@server/dbname", encoding="utf-8",
                       echo=True, max_overflow=5)

session = sessionmaker(autocommit=False, bind=engine)  # 创建本地会话
Base = declarative_base()  # 创建模型基类

user_action_rel = Table(    # 定义中间表
    'user_action_rel',  # 数据库中的表名
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),  # 外键，关联到user.id
    Column('action_id', Integer, ForeignKey('action.id'))   # 外键，关联到action.id
)


class User(Base):  # 定义数据模型类,用户
    __tablename__ = "user"  # 数据库中对应的表名
    id = Column(Integer, primary_key=True)  # id列，主键
    name = Column('name', String(50))  # 定义字段name，字符串型
    actions = relationship('Action', secondary=user_action_rel, backref='user')  # 增secondary参数


class Action(Base):
    __tablename__ = 'action'  # 数据库中得表名
    id = Column(Integer, primary_key=True)  # id列，主键，顺序记录好唯一
    name = Column('name', String(50))
    user = relationship('User', secondary=user_action_rel, backref='actions')  # 增secondary参数


Base.metadata.create_all(bind=engine)  # 在数据库中生成表结构
```

##### CRUD操作

> CRUD是关系数据库中的常用语，用来描述软件系统中对数据的基本操作。包括：增加、检索、更新、删除。

```python
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey, DateTime

# 创建数据引擎
engine = create_engine("mysql+pymysql://user:password@server/dbname", encoding="utf-8",
                       echo=True, max_overflow=5)

LocalSession = sessionmaker(autocommit=False, bind=engine)  # 创建本地会话
Base = declarative_base()  # 创建模型基类


class User(Base):  # 定义数据模型，用户
    __tablename__ = 'user'  # 数据库中的表名
    id = Column(Integer, primary_key=True)
    name = Column("name", String(50))  # 定义字段name，字符串型，对应数据库中的name列
    phone = Column("phone", String(50))  # 定义字段phone，字符串型，对应数据库中的phone列
    bookrecords = relationship("BookRecord", backref='user')  # 图书列表字段


class BookRecord(Base):  # 定义数据模型，图书
    __tablename__ = 'book_record'  # 数据库中的表名
    id = Column(Integer, primary_key=True)  # id列，主键
    book_name = Column('book_name', String(50))  # 书名
    borrow_time = Column('borrow_time', DateTime)  # 借书时间
    user_id = Column(Integer, ForeignKey('user.id'))  # user_id 外键


Base.metadata.create_all(bind=engine)  # 在数据库中生成表结构


# 数据库操作：增加
def create(session):
    user = User(name='三酷猫')
    session.add(user)  # 在name中增加一条数据
    session.flush()  # 执行插入数据语句
    session.refresh(user)  # 增加完成后刷新数据的id字段
    print(f"增加：id={user.id},name={user.name},phone={user.phone}")  # 打印user数据
    bookrecords = [BookRecord(book_name='book_' + str(i), user_id=1) for i in range(10)]
    session.bulk_save_objects(bookrecords)  # 批量插入数据
    session.commit()  # 提交事务，将数据保存到数据库


# 数据库操作：检索
def retrieve(session):
    queryuser = session.query(User)  # 创建query对象
    print('获取：记录条数：', queryuser.count())  # 打印记录数量
    first = queryuser.get(1)  # 根据主键获取第一条记录
    print('获取：第一条记录的name字段值：', first.name)  # 打印第一条记录name值
    querybook = session.query(BookRecord)  # 创建query对象
    all = querybook.all()  # 获取全部记录
    print('获取：全部图书记录的name字段值：', [book.book_name for book in all])
    books = querybook.filter(BookRecord.id > 5).all()  # 获取id大于5的图书记录
    print('获取：id大于5的图书记录：', [book.book_name for book in books])


# 数据库操作：更新
def update(session):
    query = session.query(User)  # 创建query对象
    query.filter(User.name == '三酷猫').update({User.phone: '13888888888'})
    session.commit()  # 提交事务
    user = query.filter(User.name == '三酷猫').first()
    print(f"更新后：id={user.id},name={user.name},phone={user.phone}")  # 打印user数据


# 数据库操作：删除
def delete(session):
    query = session.query(BookRecord)  # 创建query对象
    query.filter(BookRecord.id > 5).delete()  # 删除图书id大于5的数据
    session.commit()  # 提交事务
    all = query.all()  # 获取全部记录
    print("删除后：全部图书记录name字段值：", [book.book_name for book in all])


if __name__ == '__main__':
    session = LocalSession()
    create(session)
    retrieve(session)
    update(session)
    delete(session)
```

### 连接MySQL

#### 安装数据库驱动

```python
pip3 install pymysql
```

#### 创建项目并连接SQLAlchemy

![image-20221110091837482](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211100918489.png)

```python
# __intit__.py
import pymysql  # 导入数据库驱动

pymysql.install_as_MySQLdb()    # 将数据库驱动注册为MySQLdb模式
```

其中，`__init__.py` 是一个空文件，它的作用是将sql_db目录定义为Python包。SQLAlchemy在连接MYSQL数据时，需要对数据库驱动PyMySQL做一些初始化工作，以保证程序正常运行，所以需要在`__init__.py`中添加初始化代码。

```python
# database.py

# 第一步：导入SQLAlchemy组件包
from sqlalchemy.orm import sessionmaker  
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

# 第二步：创建数据引擎
engine = create_engine("mysql+pymysql://user:password@server/dbname", encoding="utf-8",
                       echo=True, max_overflow=5)
# 第三步：创建本地会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 第四步：创建数据模型基础类
Base = declarative_base()
```

在文件database.py中，使用数据库连接串`"mysql+pymysql://user:password@server/dbname"`建立数据库连接对象engine，数据库连接串的格式为”数据库类型://用户名:密码@主机/数据库实例名“。

#### 创建SQLAlchemy数据库模型

```python
# models.py

# 第一步：导入SQLAlchemy组件包
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
# 第二步：从database模块中导入基类Base
from .database import Base


# 定义User模板类，继承自Base
class User(Base):
    __tablename__ = 'user'  # 指定数据库中的表名
    id = Column(Integer, primary_key=True, index=True)  # 定义类的属性，对应表的字段
    email = Column(String(50),unique=True,index=True)
    hash_password = Column(String(50))
    is_active = Column(Boolean, default=True)
    books = relationship('Book', back_populates='owner')  # 定义一对多关系


class Book(Base):
    __tablename__ = 'book'  # 指定数据库中的表名
    id = Column(Integer, primary_key=True, index=True)	  # 定义类的属性，对应表的字段
    title = Column(String(50), index=True)
    description = Column(String(200), index=True)
    owner_id = Column(Integer, ForeignKey('user.id'))
    owner = relationship('User', back_populates='books')  # 定义关联
```

以上代码，导入所需的**SQLAlchemy**组件包，然后从**database.py**中导入**Base**类，作为数据库模型的基类，最后定义两个数据库模型：**User**、**Book**。在数据模型**User**中，使用**relationship**函数定义一个多对多关系的**books**，该关系指向另一个数据库模型**Book**。在数据库模型**Book**中也可以使用**relationship**函数定义一个多对一关系**owner**，指向数据库模型**User**。

#### 创建Pydantic数据模型

用**Pydantic**实现的数据模型主要是为了实现数据的读写操作，并提供API接口文档。为了避免**Pydantic**与**SQLAlchemy**模型混淆，这里将**Pydantic**模型写在文件**schemas.py**中。

```python
# schemas.py

# 第一步：导入相关模块
from typing import List, Optional
from pydantic import BaseModel


# 第二步：定义BookBase模型类，从BaseModel继承
class BookBase(BaseModel):
    # 第三步：定义模型的属性
    title = str
    description = Optional[str] = None


# 第四步：定义BookCreate模型类，从BookBase继承
class BookCreate(BookBase):
    pass


# 第五步：定义Book模型类，从BookBase继承
class Book(BookBase):
    id: int
    owner_id: int

    # 第六步：配置项中启用ORM模式
    class Config:
        orm_mode = True


# 第七步：定义UserBase模型类，从BaseModel继承
class UserBase(BaseModel):
    email = str


class UserCreate(UserBase):
    password = str


class User(UserBase):
    id: int
    is_active = bool
    books: List[Book] = []

    # 配置项中启用ORM模式
    class Config:
        orm_mode = True
```

在**schemas.py**中，首先导入相关模块；然后从**BaseModel**类继承定义**BookBase**模型类，在模型中定义所需的字段：**title**和**description**；再从**BookBase**模型类继承，分别定义**BookCreate**和**Book**模型类，在**Book**模型类内部的**Config**类中增加选项：**orm_mode=True**。再使用上述相同方式定义一组新模型类：**UserBase**、**UserCreate**、**User**。

**Book**模型类和**User**模型类都定义了内部**Config**类，其中的配置项**orm_model=True**，意思是开启**ORM**模式，它的作用是让**Pydantic**模型也可以从任意的**ORM**模型读取数据。当这个配置项默认为**False**的时候，只能从字典中读取数据，不能从**ORM**模型读取数据。

#### 实现数据操作

```python
# crud.py

# 第一步：导入会话组件
from sqlalchemy.orm import Session
# 第二步：导入前面定义的models和schemas模块
from . import models, schemas


# 第三步，读取数据的函数
# 读取单个用户
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


# 通过email读取单个用户
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


# 读取带分页的用户列表
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


# 读取图书列表
def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()


# 第四步：创建数据的函数
# 创建一个用户
def create_user(db: Session, user: schemas.UserCreate):
    # 模拟加密过程
    fake_hashed_password = user.password + 'notesfjalksdjfklejlkhgg'
    # 第一步：根据数据创建数据库模型的实例
    db_user = models.User(email=user.email, hash_password=fake_hashed_password)
    # 第二步：将实例添加到会话
    db.add(db_user)
    # 第三步：提交会话
    db.flush()
    db.commit()
    # 第四步：刷新实例，用于获取数据或者生成数据库中的id
    db.refresh(db_user)
    return db_user


# 创建与用户相关的一本图书
def create_user_book(db: Session, book: schemas.BookCreate, user_id: int):
    db_row = models.Book(**book.dict(), owner_id=user_id)
    db.add(db_row)
    db.flush()
    db.commit()
    db.refresh(db_row)
    return db_row


# 更新图书的标题
def update_book_title(db: Session, book: schemas.Book):
    db.query(models.Book).filter(models.Book.id == book.id).update({'title': book.title})
    db.commit()
    return 1


# 删除图书
def delete_book(db: Session, book: schemas.Book):
    res = db.query(models.Book).filter(models.Book.id == book.id).delete()
    print(res)
    db.commit()
    return 1
```

#### 实现FastAPI请求函数

```python
# main.py

from typing import List
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
# 导入自定义模块
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

# 生成数据库中的表
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# 定义依赖函数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 定义路径操作函数，并注册路由路径：创建用户
@app.post('/users/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="邮箱被注册")
    return crud.create_user(db=db, user=user)


# 定义路径操作函数，并注册路由路径：获取用户列表
@app.get('/users/', response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)


# 定义路径操作函数，并注册路由路径：获取用户信息
@app.get('/users/{user_id}', response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='用户没找到')
    return db_user


# 定义路径操作函数，并注册路由路径：创建用户相关的项目
@app.post('/users/{user_id}/books/', response_model=schemas.Book)
def create_book_for_user(user_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_user_book(db=db, book=book, user_id=user_id)


# 定义路径操作函数，并注册路由路径：获取项目列表
@app.get('/books/', response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_books(db, skip=skip, limit=limit)


# 定义路径操作函数，并注册路由路径：修改图书标题
@app.put('/books/')
def update_book_title(book: schemas.Book, db: Session = Depends(get_db)):
    return crud.update_book_title(db, book)


# 定义路径操作函数，并注册路由路径：删除图书
@app.delete('/books/')
def delete_book(book: schemas.Book, db: Session = Depends(get_db)):
    return crud.delete_book(db, book)


if __name__ == '__main__':
    uvicorn.run(app=app)
```

![image-20221110150109552](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211101501280.png)

## 连接MongoDB

### 安装MongoDB

- [x] 安装MongoDB	[MongoDB安装教程](https://www.runoob.com/mongodb/mongodb-linux-install.html)
- [x] 开放对应端口 默认是27017

### 安装数据库驱动

```python
pip3 install pymongo
```

### 实现MongoDB中的数据操作

```python
from typing import Optional, List
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI, Depends
from pymongo import MongoClient
from bson.json_util import dumps
import json

app = FastAPI()

MONGO_DATABASE_URL = 'http://MongoDBServer:27017/'  # mongodb连接字符串


def get_db():  # 定义依赖注入函数，用于连接MongoDB
    client = MongoClient(MONGO_DATABASE_URL)
    db = client['test']
    try:
        yield db
    finally:
        client.close()


class Item(BaseModel):  # 定义数据模型类
    title: str
    description: Optional[str] = None


@app.post('/items/', response_model=Item)  # 注册路由路径
async def create_item(item: Item,  # 定义路径操作函数，定义参数item
                      db: MongoClient = Depends(get_db)):  # 依赖数据库
    mycol = db['items']  # 获取集合
    obj = mycol.insert_one(item.dict())  # 保存一条数据
    return item


@app.get('/items/', response_model=List[Item])  # 注册路由路径
async def get_item(db: MongoClient = Depends(get_db)):  # 定义路径操作函数，依赖数据库
    mycol = db['items']  # 获取集合
    return json.loads(dumps(mycol.find()))  # 将数据库中的对象转换为dict并返回


if __name__ == '__main__':
    uvicorn.run(app=app)
```

![image-20221110155127893](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211101551743.png)

![image-20221110155158213](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211101551623.png)

## 连接Redis

### 安装Redis

- [x] 安装Redis	[Redis安装教程](https://www.runoob.com/redis/redis-install.html)
- [x] 开放对应端口 默认是6379

### 安装数据驱动

```python
pip3 install redis
```

### 实现Redis中的数据操作

```python
from typing import Optional
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI, Depends
from redis import Redis, ConnectionPool  # 导入redis组件包
import json

app = FastAPI()


def get_rdb():  # 定义依赖注入函数，用于连接Redis
    pool = ConnectionPool(host='RedisServer', port=6379, password='RedisPassword')
    rdb = Redis(connection_pool=pool)
    try:
        yield rdb
    finally:
        rdb.close()


class Item(BaseModel):  # 定义数据模型类
    title: str
    description: Optional[str] = None


@app.post('/items/', response_model=Item)  # 注册路由路径
async def create_item(item: Item,  # 定义路径操作函数，定义参数
                      rdb: Redis = Depends(get_rdb)):  # 指定依赖项数据库
    obj = rdb.set('item_name', json.dumps(item.dict()))  # 将对象转换成JSON字符串并获取集合
    return item


@app.get('/item/', response_model=Item)  # 注册路由路径
async def get_item(rdb: Redis = Depends(get_rdb)):  # 定义路径操作函数，指定依赖项
    obj = rdb.get('item_name')  # 获取集合
    return json.loads(obj)  # 将数据库中的对象转换成dict并返回


if __name__ == '__main__':
    uvicorn.run(app=app)
```

![image-20221110160858879](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211101609079.png)

![image-20221110160937939](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211101609702.png)

### 案例：卖海鲜

```python
from fastapi import FastAPI
# 连接SQLAlchemy
import pymysql
import uvicorn
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel  # 导入基础模型类
from fastapi import Depends
from sqlalchemy import Column, Integer, String, Float

pymysql.install_as_MySQLdb()
app = FastAPI()


class Goods(BaseModel):  # 定义数据模型类，继承自BaseModel类
    name: str  # 定义字段name，类型为str
    num: float  # 定义字段num，类型为float
    unit: str  # 定义字段unit，类型为str
    price: float  # 定义字段price，类型为float


# 创建数据引擎
engine = create_engine("mysql+pymysql://user:password@server/dbname", encoding="utf-8",
                       echo=True, max_overflow=5)

session = sessionmaker(autocommit=False, bind=engine)  # 创建本地会话


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()  # 创建数据模型基础类


class Order(Base):  # 数据库表模型
    __tablename__ = 't_order'  # 指定数据库中的表名
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20))
    num = Column(Float)
    unit = Column(String(4))
    price = Column(Float)


Base.metadata.create_all(bind=engine)


class OrderCreate(BaseModel):  # ORM模型读写字段
    id: int = 0
    name: str  # 定义字段name，类型为str
    num: float  # 定义字段num，类型为float
    unit: str  # 定义字段unit，类型为str
    price: float  # 定义字段price，类型为float

    class Config:
        orm_mode = True


def create_NewRecord(db: Session, good: Goods):  # 写入数据库表中
    db_order = Order(name=good.name, num=good.num, unit=good.unit, price=good.price)  # 将数据模型实例添加到会话
    db.add(db_order)
    db.commit()  # 提交会话
    db.refresh(db_order)  # 刷新实例，用于获取数据或者生成数据库中的ID
    return db_order


@app.post('/goods/', response_model=OrderCreate)  # 注册路由路径
async def findGoods(good: Goods, db: session = Depends(get_db)):  # 定义路径操作函数
    return create_NewRecord(db=db, good=good)


if __name__ == '__main__':
    uvicorn.run(app=app)
```

![image-20221111100022864](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211111000373.png)

![image-20221111100039366](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211111000790.png)

## 安全机制

### 安全机制基本功能

- OAuth2 令牌授权安全机制

  OAuth2 是 一个关于令牌授权的开放网络规范，具有非常广泛的应用。它的主要特点是在资源使用者与资源提供者之间，建立一个认证服务器。资源使用者不能直接访问资源服务器，而是登录到认证服务器，认证服务器发放“令牌”；然后资源使用者携带“令牌”访问资源服务器，服务器根据“令牌”的权限范围和有效期，向资源使用者开放资源。

  OAuth2的运行流程：

  - 资源使用者向资源提供者发起认证请求；
  - 资源提供者同意给予资源使用者授权；
  - 资源使用者使用上一步获得的授权，向认证服务器申请令牌；

  ![UML 图 (3)](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211111031826.jpg)

  - 认证服务器对资源使用者进行认证成功后，向资源使用者发放令牌；
  - 资源使用者借组令牌向资源服务器申请使用资源；
  - 资源服务器确认令牌无误后，向资源使用者开放受保护的资源。

### 添加基于OAuth2的安全机制

```
pip3 install python-multipart
```

```python
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer  # 导入安全模块类
import uvicorn

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')  # 创建依赖类实例


@app.get("/items/")  # 注册路由路径
async def read_items(  # 定义路径操作函数
        token: str = Depends(oauth2_scheme)):  # 设置依赖类
    return {'token': token}


if __name__ == '__main__':
    uvicorn.run(app=app)
```

![202211111046672](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211140906621.png)

以上代码中，使用参数tokenUrl='login'创建了依赖类OAuth2PasswordBearer的一个实例，然后再路径操作函数read_item中定义了依赖类，这样就把路径操作函数变成受保护的资源。

### 实现基于OAuth2的安全机制

**目录文件**

![image-20221111113900088](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211111139636.png)

**第一步：创建数据连接**

```python
# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# 第二步：创建数据引擎
engine = create_engine("mysql+pymysql://user:password@server/dbname", encoding="utf-8",
                       echo=True, max_overflow=5)
# 第三步：创建本地会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 第四步：创建数据库模型类
Base = declarative_base()
```

**第二步：添加数据模型**

```python
# models.py

from sqlalchemy import Column, String, Integer
from .database import Base


class UserInDB(Base):   # 定义用户数据库模型类，继承自Base
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column('username', String(50))
    full_name = Column('full_name', String(50))
    email = Column('email', String(100))
    hashed_password = Column('hashed_password', String(64))
```

**第三步：添加请求数据模型**

```python
# schemas.py

from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):  # 响应数据模型-令牌
    access_token: str
    token_type: str


class UserBase(BaseModel):  # 数据模型基类-用户信息
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None


class UserCreate(UserBase):  # 数据模型，创建用户，继承字UserBase
    password: str


class User(UserBase):  # 数据模型，用户，继承自UserBase
    class Config:
        orm_mode = True
```

**第四步：定义好数据库模型和增加数据操作函数**

```python
# services.py

from sqlalchemy.orm import Session
from . import models
from . import schemas
from .utils import get_password_hash, verify_password


def get_user(db: Session, username: str):  # 获取单个用户，用参数传入的用户名获取数据库中的相应的用户记录
    return db.query(models.UserInDB).filter(models.UserInDB.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):  # 创建一个用户 参数传入的用户数据保存到数据库中
    # 计算密码的哈希值
    hashed_password = get_password_hash(user.password)
    db_user = models.UserInDB(username=user.username, hashed_password=hashed_password, email=user.email,
                              full_name=user.full_name)
    db.add(db_user)  # 将实例添加到会话
    db.commit()  # 提交会话
    db.refresh(db_user)  # 刷新实例，用于获取数据或者生成数据库中的id
    return db_user


def authenticate_user(db, username: str, password: str):  # 验证用户和密码
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
```

在**create_user**函数的实现中，使用了函数**get_password_hash**，该函数定义在**utils.py**中，作用是使用bcrypt算法计算字符串的哈希值，这是最常见的保存密码方式。

**安装依赖库：**

```python
pip3 install passlib
pip3 install bcrypt
```

```python
# utils.py

from passlib.context import CryptContext

_pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


# 验证密码
def verify_password(plain_password, hashed_password):
    return _pwd_context.verify(plain_password, hashed_password)


# 生成密码
def get_password_hash(password):
    return _pwd_context.hash(password)
```

```python
# main.py

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from auth import schemas, services, database

# 第一步，创建安全模式：密码模式
OAuth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

app = FastAPI()


# 第二步，创建税局库依赖函数
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 第二步：定义路径操作函数，注册路由路径，定义依赖项为数据库
@app.post('/user/create/', response_model=schemas.User)
async def create_user(user: schemas.UserCreate,
                      db: Session = Depends(get_db)):
    dbuser = services.get_user(db, user.username)
    # 判断用户存在
    if dbuser:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='用户名不存在'
        )
    return services.create_user(db, user)  # 在数据库中创建用户


@app.get('/items/')
async def read_items(token: str = Depends(OAuth2_scheme)):
    return {'token': token, 'data': 'cool'}


if __name__ == '__main__':
    # 第四步：生成数据库中的表
    database.Base.metadata.create_all(bind=database.engine)
    uvicorn.run(app=app)
```

**首次创建新用户**

![image-20221111143617394](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211111436714.png)

**不修改任何数据，再次创建用户**

![image-20221111143634601](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211111436144.png)

### 生成令牌

```python
pip3 install python-jose
pip3 install cryptography
```

```python
# services.py

from datetime import timedelta, datetime
from jose import jwt
from sqlalchemy.orm import Session
from . import models
from . import schemas
from .utils import get_password_hash, verify_password

# 使用SECRET_KEY:
# openssl rand -hex 32

SECRET_KEY = '9018e1a691693fbb980e80627b977c0c5c5951fef21d36d6cf23f80fcabeb698'  # openssl rand -hex 32 生成密钥
ALGORITHM = 'HS256'  # 算法
ACCES_TOKEN_EXPIRE_MINUTES = 5  # 令牌有效期5分钟


# 获取单个用户，用参数传入的用户名获取数据库中的相应的用户记录
def get_user(db: Session, username: str):  
    return db.query(models.UserInDB).filter(models.UserInDB.username == username).first()


# 创建一个用户 参数传入的用户数据保存到数据库中
def create_user(db: Session, user: schemas.UserCreate):  
    # 计算密码的哈希值
    hashed_password = get_password_hash(user.password)
    db_user = models.UserInDB(username=user.username, hashed_password=hashed_password, email=user.email,
                              full_name=user.full_name)
    db.add(db_user)  # 将实例添加到会话
    db.commit()  # 提交会话
    db.refresh(db_user)  # 刷新实例，用于获取数据或者生成数据库中的id
    return db_user


# 验证用户和密码
def authenticate_user(db, username: str, password: str):  
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# 创建令牌，将用户名放入令牌
def create_token(data: dict):
    to_encode = data.copy()
    expire_delta = timedelta(minutes=ACCES_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now() + expire_delta
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 解析令牌，返回用户名
def extract_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])
    return payload.get('username')


```

### 增加用户登录功能

在main.py中定义安全模式下代码：

```python
OAuth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
```

```python
# main.py

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth import schemas, services, database

# 第一步，创建安全模式：密码模式
OAuth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

app = FastAPI()


# 第二步，创建税局库依赖函数
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 第二步：定义路径操作函数，注册路由路径，定义依赖项为数据库
@app.post('/user/create/', response_model=schemas.User)
async def create_user(user: schemas.UserCreate,
                      db: Session = Depends(get_db)):
    dbuser = services.get_user(db, user.username)
    # 判断用户存在
    if dbuser:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='用户名不存在'
        )
    return services.create_user(db, user)  # 在数据库中创建用户


@app.get('/items/')
async def read_items(token: str = Depends(OAuth2_scheme)):
    return {'token': token, 'data': 'cool'}


@app.post('/login', response_model=schemas.Token)
async def login(
        # 依赖项，登录表单
        form: OAuth2PasswordRequestForm = Depends(),
        # 依赖项，数据库会话
        db: Session = Depends(get_db)
):
    # 验证用户有效性
    user = services.authenticate_user(db, form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='用户名或密码无效',
            headers={"WWW-Authenticate": "Bearer"}
        )
    # 发放令牌
    access_token = services.create_token(data={'username': user.username})
    # 返回令牌
    return {'access_token': access_token, 'token_type': 'bearer'}


if __name__ == '__main__':
    # 第四步：生成数据库中的表
    database.Base.metadata.create_all(bind=database.engine)
    uvicorn.run(app=app)
```

![20221114091616531](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211140916339.png)

![20221114091646939](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211140916351.png)

![20221114091730403](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211140917344.png)

![20221114091810351](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211140918610.png)

可以看到认证窗口"Authorize"按钮中的图表已经变成了已锁状态。证明已经认证通过了，可以进行其他操作了。



### 获取用户当前信息

```python
# main.py

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from sqlalchemy.orm import Session
from auth import schemas, services, database

# 第一步，创建安全模式：密码模式
OAuth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

app = FastAPI()


# 第二步，创建税局库依赖函数
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 第二步：定义路径操作函数，注册路由路径，定义依赖项为数据库
@app.post('/user/create/', response_model=schemas.User)
async def create_user(user: schemas.UserCreate,
                      db: Session = Depends(get_db)):
    dbuser = services.get_user(db, user.username)
    # 判断用户存在
    if dbuser:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='用户名不存在'
        )
    return services.create_user(db, user)  # 在数据库中创建用户


@app.get('/items/')
async def read_items(token: str = Depends(OAuth2_scheme)):
    return {'token': token, 'data': 'cool'}


@app.post('/login', response_model=schemas.Token)
async def login(
        # 依赖项，登录表单
        form: OAuth2PasswordRequestForm = Depends(),
        # 依赖项，数据库会话
        db: Session = Depends(get_db)
):
    # 验证用户有效性
    user = services.authenticate_user(db, form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='用户名或密码无效',
            headers={"WWW-Authenticate": "Bearer"}
        )
    # 发放令牌
    access_token = services.create_token(data={'username': user.username})
    # 返回令牌
    return {'access_token': access_token, 'token_type': 'bearer'}


# 获取当前用户信息的依赖项
async def get_current_user(token: str = Depends(OAuth2_scheme),
                           db: Session = Depends(get_db)):
    invalid_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='无效的用户数据',
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        username: str = services.extract_token(token)
        if username is None:
            raise invalid_exception
    except JWTError as e:
        raise invalid_exception from e
    user = services.get_user(db, username=username)
    if user is None:
        raise invalid_exception
    return user


# 获取用户当前信息
@app.get('/user/', response_model=schemas.User)
async def read_current_user(current_user: schemas.User = Depends(get_current_user)):
    return current_user


if __name__ == '__main__':
    # 第四步：生成数据库中的表
    database.Base.metadata.create_all(bind=database.engine)
    uvicorn.run(app=app)
```

![20221114103518723](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211141035463.png)

以上代码包含两个函数：

第一个函数get_current_user是依赖注入函数，其作用是解析token字符串，获取其中包含的用户名，并根据用户名从数据库中查找对应的用户数据，如果找到用户，则返回用户数据，否则触发异常。

第二个函数read_current_user是路径操作函数，使用装饰器定义了路由/user/和响应模型User。函数的参数中使用依赖注入的方式获取当前登录用户的数据。

![20221114102914085](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211141029935.png)

最后，实现了FastApi中基于OAuth2的安全机制。任何新增加的路径操作函数，只需要在参数中添加OAuth2_scheme或get_current_user，就会被安全机制保护起来（就是上锁），只允许被授权的用户访问。

## 异步技术

### 什么是进程

进程是计算机中的程序在某数据集合上的一次运动活动，是系统进行资源分配和调度的基本单位，是操作系统结构的基础。如一个运行QQ软件就是一个进程，两个运行QQ软件就是两个进程。

### 什么是线程

线程是操作系统能够进行运算调度的最小单位。它被包含在进程之中。是进程中的实际运作单位。一条线程指的是进程中的一个单一顺序的控制流。一个进程中可以并发多个线程，每条线程并行执行不同的任务。如一个运行的QQ软件里通过线程通信发送一条信息，就是执行线程指令(往往是多线程同步执行)

### 线程和进程的关系：

![UML 图 (5)](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211141048822.jpg)

### 阻塞/非阻塞

多个线程并发运行时，会使用共同资源，资源只能同时被一个线程访问。

#### 阻塞

阻塞是指一个线程所访问的资源被其他线程占用时，需要等待其他线程完成操作，在等待期间该线程自身无法继续其他操作，这个状态称为阻塞。常见的阻塞形式有：网络I/O阻塞、磁盘I/O阻塞、用户输入阻塞等。

#### 非阻塞

非阻塞是指线程在等待其他线程过程中，自身不被阻塞，可以继续执行其他操作，此时称该程序在此操作上时非阻塞的。

### 同步/异步

#### 同步

同步是指为了完成某个操作，多个线程必须按照特定的通信方式协调一致，按顺序执行。比如，在车站购买火车票时需要排队，前面的人购买完成，后面才允许购买。

#### 异步

异步是指为了完成某个操作，无需特定的通信方式协调也可以完成任务的方式。比如：在快餐店吃饭时，排队点餐后，即可离开队列，回到座位等待，食物准备好以后，再去取餐。

### 并行/并发

#### 并行

并行描述的是程序的执行状态，指多个任务同时被执行。它主要以利用更多的计算资源快速完成多个任务为目的。

#### 并发

并发描述是程序的组织结构，指程序要被设计成多个可独立执行的子任务，它主要以利用有限的计算机资源使多个任务可以被实时或近实时执行为目的。

### GIL

GIL又叫全局解释器锁，是一种全局互斥锁，每个线程在执行的过程中都需要先获取GIL，保证同一时刻只有一个线程能够控制Python解释器。

### Asyncio库介绍

#### 协程

协程本质上是一个函数，其特点是在代码中可以将执行权交给其他协程。当调用协程函数时，不会立即执行该函数，而是会返回一个协程对象。需要将协程对象注册到事件循环中，由事件循环负责调用。

```python
import asyncio
from datetime import datetime


async def main():
    print(f'start:{datetime.now().strftime("%X")}')
    print('hello')
    await asyncio.sleep(1)
    print(f'end:{datetime.now().strftime("%X")}')
    print('你好啊,学习者')


asyncio.run(main())

# 输出结果如下
# start:11:32:53
# hello
# end:11:32:54
# 你好啊,学习者
```

从结果中来看，开始时间和结束时间之间有一秒的时间差，这说明代码中的语句是按顺序执行的。如果想要真正运行一个协程，需要将代码写道协程函数中

```python
import asyncio
from datetime import datetime


# 定义协程函数
async def my_print(timeout, txt):
    await asyncio.sleep(timeout)
    print(txt)


async def main():
    print(f'start:{datetime.now().strftime("%X")}')
    await my_print(1, 'hello')
    print(f'end:{datetime.now().strftime("%X")}')
    await my_print(2, '你好')
    print(f'end:{datetime.now().strftime("%X")}')


asyncio.run(main())

# 输出结果如下
# start:11:38:37
# hello
# end:11:38:38
# 你好
# end:11:38:40
```

以上代码中，定义了协程函数my_print，其作用是等待timeout秒后，打印txt内容。然后定义了主函数main，其作用是等待1秒后调用协程函数my_print，打印“hello”，在等待2秒后调用协程函数my_print，打印“你好”。最后，使用asyncio.run()方法，调用了代码中的主函数main，总执行了3秒。

还有另外一种办法，可以实现并发执行多个协程

```python
import asyncio
from datetime import datetime


# 定义协程函数
async def my_print(timeout, txt):
    await asyncio.sleep(timeout)
    print(txt)


async def main():
    # 把协程函数加入任务事件循环中
    task1 = asyncio.create_task(my_print(1, 'hello'))
    task2 = asyncio.create_task(my_print(1, '你好'))
    print(f"task start {datetime.now().strftime('%X')}")
    await task1
    await task2
    print(f"end {datetime.now().strftime('%X')}")


asyncio.run(main())

# 输出结果如下
# task start 11:47:50
# hello
# 你好
# end 11:47:51
```

以上代码中，使用asyncio.create_task()方法创建了2个任务，并将任务加入事件循环中，所以两个任务同时开始执行，分别执行1秒和2秒后打印文字。总执行时间为2秒。

### 案例：卖海鲜记账

```python
import asyncio
from pydantic import BaseModel  # 导入基础模型类


class Goods(BaseModel):  # 定义数据模型类，继承自BaseModel类
    name: str = '对虾'  # 定义name字段，类型为str
    num: float = 10  # 定义num字段，类型为float
    unit: str = '斤'  # 定义unit字段，类型为str
    price: float = 48  # 定义price字段，类型为float


async def stat(good: Goods):    # 定义协程函数，统计金额
    print(good.num * good.price, '元')
    return good.num * good.price


async def Count_users():    # 定义协程函数，写入提交次数
    with open(r"F:\c1.txt", "r+") as f:
        num = f.read()
        if num == '':
            num = 0
        f.write(str(int(num) + 1))
    print(f'{str(int(num) + 1)}次')


async def main():
    good = Goods()
    task1 = asyncio.create_task(stat(good))
    task2 = asyncio.create_task(Count_users())
    await task1
    await task2


asyncio.run(main())

# 输出结果如下
# 480 元
# 2次
```

## 企业应用架构

### 应用事件处理

#### 启动事件

FastAPI提供了on_event装饰器，用于管理应用级别的事件，当传递参数为“startup”时，便可以在装饰器绑定的函数中执行启动前的特定操作

```python
import datetime
import uvicorn
from fastapi import FastAPI

app = FastAPI()


def send_msg_manager(action):
    print(f'通知管理员,127.0.0.1主机的main程序于{datetime.datetime.now()}时间{action}了')


@app.on_event('startup')
async def startup_event():
    send_msg_manager('启动')


@app.get('/')
async def read_items():
    return {'Hello,管理员'}


if __name__ == '__main__':
    uvicorn.run(app=app)
```

![20221114153352610](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211141533866.png)

以上代码中，在操作函数上方使用装饰器@app.on_event("startup")，将函数startup_event定义为启动事件，启动事件调用另一个函数send_msg_manager。该函数中将一句文本打印到控制台上。

#### 停止事件

停止事件与启动事件的定义方式类似，需要在操作函数上方使用装饰器**@app.on_event("shutdown")**

```python
import datetime
import uvicorn
from fastapi import FastAPI

app = FastAPI()


def send_msg_manager(action):
    print(f'通知管理员,127.0.0.1主机的main程序于{datetime.datetime.now()}时间{action}了')


@app.on_event('startup')
async def startup_event():
    send_msg_manager('启动')


@app.on_event('shutdown')
def shutdown_event():
    send_msg_manager('关闭')


@app.get('/')
async def read_items():
    return {'Hello,管理员'}


if __name__ == '__main__':
    uvicorn.run(app=app)
```

![20221114153855572](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211141539234.png)

### 管理子应用

![UML 图 (4)](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211141543997.jpg)

FastAPI提供了一种方式，可以用一个主应用管理各个子应用，这个过程成为”挂载“。挂载通过app的mount()方法来实现

```python
from fastapi import FastAPI
import uvicorn

# 定义主应用
app = FastAPI()
# 定义第一个子应用
cat_app = FastAPI()
# 定义第二个子应用
dog_app = FastAPI()
# 在路径/cat下挂载子应用
app.mount('/cat', cat_app)
# 在路径/dog下挂载子应用
app.mount('/dog', dog_app)


# 在第一个子应用中定义路由
@app.get('/app')
def read_main():
    return {'message': 'hello world'}


# 在第二个子应用中定义路由
@cat_app.get('/hellocat')
def read_sub():
    return {'message': 'hello cat'}


# 在第三个子应用中定义路由
@dog_app.get('/hellodog')
def read_sub():
    return {'message': 'hello dog'}


if __name__ == '__main__':
    uvicorn.run(app=app)
```

![20221114171309835](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211141713158.png)

![20221114171332563](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211141713226.png)

FastAPI通过挂载的方式，将多个子应用通过不同的路径挂载到一个主应用上统一管理。每个子应用可以添加各自的路径操作函数、路由，既保证了整体应用的统一性，又保证了各子应用的独立性。

### 应用管理模块

#### 路由类

FastAPI提供了路由类APIRouter，使得代码可以写到不同py文件中进行调用。

```python
# code9_5.py

from fastapi import APIRouter

# 定义路由类的实例
router = APIRouter(
    prefix='/child',  # 路由的路径前缀
    tags=['child'],  # API文档中显示的名称
    dependencies=[],  # 给当前路由类实例指定依赖项
    responses={404: {'detail': '未找到项目'}}  # 自定义响应
)


# 使用router实例的装饰器定义路由
@router.get('/hello')
async def hello(name: str):  # 定义路径操作函数
    return {'message': f'Hello %s' % name}
```

- prefix，路径前缀
- tags，API文档中显示的标签名
- dependencies，依赖项列表
- response，自定义响应

```python
# main.py

from fastapi import FastAPI
import uvicorn
import code9_5  # 导入路由所在包

app = FastAPI()  # 定义应用实例

app.include_router(code9_5.router)  # 在应用中引用路由实例

if __name__ == '__main__':
    uvicorn.run(app=app)
```

![20221114173824653](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211141738087.png)

#### 应用目录结构

```
├── webapi	            	# 应用程序目录
│   ├── app             	# 应用配置目录
│   │   ├── __init__.py	
│   │   ├── database.py		# 公共依赖
│   │   └── settings.py 	# 全局配置文件
│   ├── dependencies		# 依赖包
│   │   ├── __init__.py
│   │   ├── dep_common.py 	# 公用的依赖
│   │   ├── dep_goods.py  	# 与商品相关的依赖
│   │   ├── dep_users.py  	# 与用户相关的依赖
│   │   └── auth.py		  	# 登录认证相关的依赖
│   ├── routers         	# 路由包
│   │   ├── __init_.py	
│   │   ├── router_goods.py	# 与商品相关的路由
│   │   ├── router_users.py	# 与用户相关的路由
│   │   └── router_auth.py	# 登录认证相关的路由
│   ├── models
│   │   ├── __init_.py
│   │   ├── db_goods.py		# 商品相关的数据库模型
│   │   └── db_users.py		# 用户相关的数据库模型
│   ├── schema
│   │   ├── __init_.py
│   │   ├── schema_goods.py	# 商品相关的数据模型
│   │   └── schema_users.py # 用户相关的数据模型
│   ├── services
│   │   ├── __init_.py
│   │   ├── svr_goods.py	# 商品相关的逻辑
│   │   └── svr_users.py 	# 用户相关的逻辑
│   ├── utils
│   │   ├── __init_.py
│   │   ├── crypt.py		# 加密相关工具
│   │   └── file.py 		# 文件相关的工具
│   ├── __init__.py			# 将当前目录定义为Python包       
│   └──main.py				# 主文件
```

#### 页面模板技术

要在FastAPI框架中使用Jinja2，首先要安装模块引擎库。

```python
pip3 install jinja2
```

```python
# code9_6.py

from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates  # 导入Jinja2模板
import uvicorn

app = FastAPI()

templates = Jinja2Templates(directory='templates')  # 定义模板引擎实例，并指定模板目录


@app.get('/', response_class=HTMLResponse)  # 定义路由路径，并指定响应类型为HTML
async def index(request: Request, name: Optional[str] = '! '):
    return templates.TemplateResponse('index.html',  # 返回模板响应
                                      {'request': request, 'name': name})  # 传递给模板的数据


if __name__ == '__main__':
    uvicorn.run(app=app)
```

以上代码中，首先导入Jinja2的模板引擎模块Jinja2Templates,然后定义模板引擎的实例，并指定模板目录为templates。然后再路径操作函数中返回模板响应对象，其参数是模板文件名称和传递给模板的数据。还需要在当前目录下创建一个目录：**templates**，并在目录中创建一个空白文件**index.html**

![20221115104635078](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211151046378.png)

编辑index.html，写入以下代码。

```html
# index.html

<html>
<head>
    <title>
        欢迎
    </title>
</head>
<body>
<h1>
    你好：{{name}}
</h1>
</body>
</html>
```

![20221115105253899](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211151052714.png)

#### 管理静态文件

第一步：使用模块之前，首先要安装第三方库aiofiles。

```python
pip3 install aiofiles
```

添加一个目录名static，并且在目录下创建一个空白的style.css

![20221115110719491](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211151107010.png)

第二步：打开style.css，写入内容

```css
h1 {
    font-style: italic;
    text-align: center;
}
```

第三步：修改templates目录下的index.html，引入style.css

```
# index.html

<html>
<head>
    <title>
        欢迎
    </title>
    <link href="{{ url_for('static',path='/style.css')}}" rel="stylesheet">
</head>
<body>
<h1>
    你好：{{name}}
</h1>
</body>
</html>
```

用Jinja2的url_for标签，指定要使用的静态资源文件style.css。在页面渲染时，url_for标签的内容会转为style.css的URL地址。

第四步：加入静态资源管理的代码

```python
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates  # 导入Jinja2模板
from fastapi.staticfiles import StaticFiles  # 导入静态资源文件
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name='static')  # 挂载静态资源

templates = Jinja2Templates(directory='templates')  # 定义模板引擎实例，并指定模板目录


@app.get('/', response_class=HTMLResponse)  # 定义路由路径，并指定响应类型为HTML
async def index(request: Request, name: Optional[str] = '! '):
    return templates.TemplateResponse('index.html',  # 返回模板响应
                                      {'request': request, 'name': name})  # 传递给模板的数据


if __name__ == '__main__':
    uvicorn.run(app=app)
```

![20221115172557307](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211160852187.png)

案例：卖海鲜页面展示

第一步：在根目录下创建个templates目录，并创建index.html文件

```html
# index.html

<html>
<head>
    <title>
        海鲜市场
    </title>
</head>
<body>
<h1>你好：{{name}}</h1>
<table border="1">
    <tr>
        <td>序号</td>
        <td>商品名称</td>
        <td>数量</td>
        <td>单位</td>
        <td>价格</td>
    </tr>
    {% for one in goods %}
    <tr>
        <td>{{one.id}}</td>
        <td>{{one.name}}</td>
        <td>{{one.num}}</td>
        <td>{{one.unit}}</td>
        <td>{{one.price}}</td>
    </tr>
    {%endfor%}

</table>
</body>
</html>
```

第二步：在根目录创建FromDBShowGoods.py文件

```python
# FromDBShowGoods.py

from fastapi import FastAPI, Request, Depends
# 连接SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel  # 导入基础模型类
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates  # 导入Jinja2模块
import uvicorn

app = FastAPI()


class Goods(BaseModel):  # 定义数据模型类，继承自BaseModel类
    name: str  # 定义字段name，类型为str
    num: float  # 定义字段num，类型为float
    unit: str  # 定义字段unit，类型为str
    price: float  # 定义字段price，类型为float


engine = create_engine("mysql+pymysql://user:password@server/dbname", encoding="utf-8",
                       echo=True, max_overflow=5)
session = sessionmaker(autocommit=False, bind=engine)  # 创建本地会话


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()  # 创建数据模型基础类


class Order(Base):
    __tablename__ = 't_order'
    id = Column(Integer, primary_key=True, index=True)  # 定义类的属性，对应表中的字段
    name = Column(String(20))
    num = Column(Float)
    unit = Column(String(4))
    price = Column(Float)


Base.metadata.create_all(bind=engine)


class OrderCreate_all(BaseModel):  # ORM模式读写字段
    # 配置项中启用ORM模式
    id: int = 0
    name: str  # 定义字段name，类型为str
    num: float  # 定义字段num，类型为float
    unit: str  # 定义字段unit，类型为str
    price: float  # 定义字段price，类型为float

    class Config:
        orm_mode = True


def get_goods(db: session, skip: int = 0, limit: int = 1000):
    return db.query(Order).offset(skip).limit(limit).all()


templates = Jinja2Templates(directory='../templates')  # 定义模版引擎实例，并指定模版目录


@app.get('/goods/', response_class=HTMLResponse)  # 设置路由路径，指定响应数据格式
def read_goods(request: Request, skip: int = 0, limit: int = 100, db: session = Depends(get_db)):  # 定义路径操作函数
    goods = get_goods(db, skip=skip, limit=limit)
    name = '你有新的订单，请及时查看！'
    return templates.TemplateResponse('index.html',  # 返回模型响应
                                      {"request": request, "name": name, "goods": goods})  # 传递给模版的数据


if __name__ == '__main__':
    uvicorn.run(app=app)
```

![20221116112309817](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211161123497.png)

## 测试与部署

### 测试工具

##### 常规测试

TestClient是FastAPI中提供的一套测试工具，基于Request库进行网络通信，支持Python中的Pytest测试框架。

```python
pip3 install requests
pip3 install pytest
```

```python
# main.py

from fastapi import FastAPI
from fastapi.testclient import TestClient
import uvicorn

app = FastAPI()


@app.get('/')  # 注册路由路径
async def index():  # 定义路径操作函数
    return {'name': '你好'}  # 返回一个对象


client = TestClient(app)  # 创建一个TestClient实例


def test_index():  # 定义测试函数
    response = client.get('/')  # 使用TestClient的实例发起请求，接收返回数据
    assert response.status_code == 200  # 断言：状态码
    assert response.json() == {'name': '你好'}  # 断言：返回对象


if __name__ == '__main__':
    uvicorn.run(app=app)
```

![20221116113759610](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211161138895.png)

##### 分离测试代码

在main.py同级目录下新建文件：main_test.py，将main.py中的测试代码抽离出来。

```python
# main_test.py

from fastapi.testclient import TestClient

import main

client = TestClient(main.app)  # 创建一个TestClient实例


def test_index():  # 定义测试函数
    response = client.get('/')  # 使用TestClient的实例发起请求，接收返回数据
    assert response.status_code == 200  # 断言：状态码
    assert response.json() == {'name': '你好'}  # 断言：返回对象
```

```python
# main.py

from fastapi import FastAPI

import uvicorn

app = FastAPI()


@app.get('/')  # 注册路由路径
async def index():  # 定义路径操作函数
    return {'name': '你好'}  # 返回一个对象


if __name__ == '__main__':
    uvicorn.run(app=app, reload=True)
```

在控制台中输入**pytest main_test.py**

![20221116114539795](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211161145905.png)

##### 应用事件测试

FastAPI通过@app.on_event('startup')，在应用启动前执行一些操作

```python
# main1.py

from fastapi import FastAPI
import uvicorn

app = FastAPI()

data = {  # 应用中的模拟数据
    'cat': '猫',
    'dog': '狗'
}


@app.get('/{name}')  # 注册路由路径，定义参数路径
async def index(name: str):  # 定义路径操作函数
    return {'name': data[name]}  # 返回数据


if __name__ == '__main__':
    uvicorn.run(app=app)
```

然后在main1.py同级下创建main1_test.py文件。

```python
# main1_test.py

from fastapi.testclient import TestClient
import main1


@main1.app.on_event('startup')
async def startup_event():
    main1.data['cat'] == '小猫'
    main1.data['dog'] == '小狗'


def test_index():
    with TestClient(main1.app) as client:
        response = client.get('/cat')
        assert response.status_code == 200
        assert response.json() == {'name': '猫'}
```

![20221116170644152](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211161706336.png)

以上代码中，定义了应用启动事件和相应的事件函数。在函数中，改变了data的默认值。在测试函数test_index()中，通过 with TestClient(main1.app) as client语句，创建了TestClient的实例，发起请求，将请求的返回值写到response对象，然后使用assert，验证response对象的属性。

##### 依赖项测试

```python
# main2.py

from fastapi import FastAPI, Depends
import uvicorn

app = FastAPI()


async def sms_sender(text: str):  # 定义以来注入函数
    print(f"调用短信平台发送短信，内容为{text}")  # 发送短信的代码
    return f'成功发送内容：{text}'  # 返回值


@app.get('/sendsms')  # 注册路由路径，定义路径参数
async def sendsms(sms=Depends(sms_sender)):  # 定义路径操作函数
    return {'data': sms}


if __name__ == '__main__':
    uvicorn.run(app=app)
```

在main2.py同级目录下，创建main2_test.py

```python
# main2_test.py

from fastapi.testclient import TestClient
import main2

client = TestClient(main2.app)  # 创建TestClient实例


async def override_sms_sender(text: str):  # 定义依赖注入函数，仅输出信息，不发送短信
    print(f'需发送短信内容为：{text}，仅记录，未发送')
    return f'成功发送内容：{text}'


main2.app.dependency_overrides[main2.sms_sender] = override_sms_sender


def test_sndsms():
    response = client.get('/sendsms?text=验证码')  # 使用TestClient的实例发起请求
    assert response.status_code == 200  # 断言：状态码
```

![20221116173545848](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211161735848.png)

以上代码中，定义了一个依赖注入函数**override_sms_sender**，其作用是打印内容，不真正发送短信。然后使用**app.dependency_overrides**方法，将应用原有的依赖项**sms_sender**替换成**override_sms_sender**。通过这种方式，可以在测试期间，替换原有的依赖项，不真正发送短信，仅打印内容，而不影响程序中原有的功能。

##### 测试数据库

在上面的数据库学习项目中，我们来进行数据库测试。在sql_app目录下创建**main_test.py**文件。

![20221117094130796](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211170941167.png)

```python
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sql_app.database import Base
from sql_app.main import app, get_db

# 第一部分，连接数据库
# 创建数据库引擎，用于测试
engine = create_engine("mysql+pymysql://user:password@server/dbname", encoding="utf-8",
                       echo=True, max_overflow=5)

TestingSessionLocal = sessionmaker(autocommit=False, bind=engine, autoflush=False)  # 创建本地会话
Base.metadata.create_all(bind=engine)


# 第二部分，替换依赖项
def get_test_db():  # 定义依赖函数
    try:
        db = TestingSessionLocal()  # 开启事务
        db.begin(subtransactions=True)
        yield db
    finally:
        db.rollback()  # 回滚事务
        db.close()


# 第三部分，写测试函数
client = TestClient(app)


def test_create_user():  # 测试函数
    response = client.post(  # 创建用户
        '/users/',
        json={'email': 'admin@admin1.com', 'password': '123456'}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['email'] == 'admin@admin1.com'
    assert 'id' in data
```

![20221117100145773](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211171001022.png)

数据原封不动再次执行一下pytest main_test.py，可以发现断言异常抛出

![20221117100413051](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211171004194.png)

##### 异步测试工具

在FastAPI中集成了pytest-asyncio库，这是一个支持异步的测试框架，使用之前需要进行库安装

```python
pip3 install pytest-asyncio
pip3 install HTTPX
```

```python
# main.py

from fastapi import FastAPI

import uvicorn

app = FastAPI()


@app.get('/')  # 注册路由路径
async def index():  # 定义路径操作函数
    return {'name': '你好'}  # 返回一个对象


if __name__ == '__main__':
    uvicorn.run(app=app)
```

```python
# async_test.py
import pytest
from httpx import AsyncClient  # 导入异步测试模块
import main


@pytest.mark.asyncio	# 将测试函数标记为异步函数
async def test_index():  # 定义测试方法
    async with AsyncClient(app=main.app, base_url='http://127.0.0.1:8000/') as ac:  # 创建异步客户端实例
        response = await ac.get('/')  # 发起异步请求，接收返回数据
        assert response.status_code == 200  # 断言：状态码
        assert response.json() == {'name': '你好'}  # 断言：返回值
```

![20221117101406185](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211171014290.png)

### 部署程序

第一步：安装venv虚拟环境，在根目录中可以发现venv的一个文件夹

```python
python -m venv venv
```

![20221117101853021](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211171018539.png)

第二步：激活虚拟环境（windows系统）

```shell
cd .\venv\Scripts\
 .\activate
```

![20221117101959383](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211171028156.png)

激活虚拟环境（mac系统）

```shell
source venv/bin/activate
```

第三步：生成依赖安装包库

```python
pip3 freeze > requirement.txt
```

![20221117102412186](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202211171024658.png)

第四步：一键安装项目所需依赖库

```python
pip3 install -r .\requirement.txt
```

