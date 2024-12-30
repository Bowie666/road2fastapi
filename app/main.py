import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.configs import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.extensions.ext_redis import redis_client
    # 应用启动逻辑：初始化 Redis 连接池
    print("App is starting and initializing Redis pool...")
    await redis_client
    
    yield  # 应用主逻辑在这里运行

    # 应用关闭逻辑：释放 Redis 连接池
    print("App is shutting down and closing Redis pool...")
    await redis_client.close()


def create_app():
    app = FastAPI(
        title=settings.PROJECT_NAME,  # 这个项目的名称
        openapi_url=f"{settings.API_V1_STR}/openapi.json",  # 将 API 文档放在自定义路径以避免默认路径被暴露
        # generate_unique_id_function=custom_generate_unique_id,  # TODO 通过自定义逻辑增强路由唯一性或实现更符合业务需求的 ID。
        # docs_url=None,  # 关闭默认的文档路由 TODO 有方法关闭部分接口
        lifespan=lifespan
    )
    return app

def initialize_extensions(app: FastAPI):
    from app.extensions.ext_db import init_db, engine
    from app.extensions.ext_logging import init_logging
    from app.extensions.ext_routers import init_routers

    init_db(engine)  # 只是测试数据库有没有连接上 fastapi不需要上下文的绑定
    init_logging()
    init_routers(app)


app = create_app()
initialize_extensions(app)


@app.get(path="/url_map")
async def list_routes():
    print("Registered Routes:")
    # for route in app.routes:
    #     print(f"Path: {route.path}, Methods: {route.methods}, Name: {route.name}")
    # return {"message": "Hello World"}
    return {f'Path: {route.path}': f'Methods: {route.methods}, Name: {route.name}' for route in app.routes if hasattr(route, "methods") and route.name not in ["openapixxx"]}


# 项目启动 uvicorn app.main:app --reload
# swagger ui http://127.0.0.1:8000/docs#/
if __name__ == '__main__':
    # uvicorn.run(app, log_config=settings.LOGGING_CONFIG)
    uvicorn.run(app)