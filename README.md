# road2fastapi

- 写的sql必须要兼容大部分关系型数据库 不要使用某种数据库的特性

## structure
'''
├── app                  # 「app」是一个 Python 包
│   ├── __init__.py      # 这个文件使「app」成为一个 Python 包
│   ├── main.py          # 「main」模块，例如 import app.main
│   ├── dependencies.py  # 「dependencies」模块，例如 import app.dependencies
│   └── routers          # 「routers」是一个「Python 子包」
│   │   ├── __init__.py  # 使「routers」成为一个「Python 子包」
│   │   ├── items.py     # 「items」子模块，例如 import app.routers.items
│   │   └── users.py     # 「users」子模块，例如 import app.routers.users
│   └── extensions                  # 这里面放扩展
│   │   ├── ext_logging.py          # 这个是日志的处理方式 甚至可以用到其它的脚本里面 不过需要改一些东西
│   │   ├── ext_routers.py          # 这个是注册的路由
│   │   ├── ext_db.py               # 数据库连接及初始化建表
│   │   └── users.py     # 「users」子模块，例如 import app.routers.users
│   └── internal         # 「internal」是一个「Python 子包」
│       ├── __init__.py  # 使「internal」成为一个「Python 子包」
│       └── admin.py     # 「admin」子模块，例如 import app.internal.admin
'''