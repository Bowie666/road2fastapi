import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.configs import settings

# 第一种定时任务方式 简易的后台运行 !!! 要在 lifespan 的最后加上 scheduler.shutdown()，lifespan的前面的 scheduler.start() 要去掉
# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.triggers.cron import CronTrigger
# from apscheduler.triggers.interval import IntervalTrigger
# def my_daily_task():
#     print(f"Task is running")

# scheduler = BackgroundScheduler()
# # trigger = CronTrigger(hour=0, minute=0)  # midnight every day
# trigger = IntervalTrigger(seconds=2)  # 任务每2秒执行一次
# scheduler.add_job(my_daily_task, trigger)
# scheduler.start()

@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.extensions.ext_redis import redis_client
    # 第二种定时任务方式
    # from app.extensions.ext_task import scheduler
    # from app.tasks.aps_tasks import get_task
    # 应用启动逻辑：初始化 Redis 连接池
    print("App is starting and initializing Redis pool...")
    await redis_client
    # get_task(scheduler)
    # scheduler.start()

    yield  # 应用主逻辑在这里运行

    # 应用关闭逻辑：释放 Redis 连接池
    print("App is shutting down and closing Redis pool...")
    await redis_client.close()
    # scheduler.shutdown()


def create_app():
    app = FastAPI(
        title=settings.PROJECT_NAME,  # 这个项目的名称
        openapi_url=f"{settings.API_V1_STR}/openapi.json",  # 将 API 文档放在自定义路径以避免默认路径被暴露
        # generate_unique_id_function=custom_generate_unique_id,  # TODO 通过自定义逻辑增强路由唯一性或实现更符合业务需求的 ID。
        # docs_url=None,  # 关闭默认的文档路由 TODO 有方法关闭部分接口
        # redoc_url=None,
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