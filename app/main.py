from fastapi import FastAPI

from app.configs import settings


app = FastAPI(
    title=settings.PROJECT_NAME,  # 这个项目的名称
    openapi_url=f"{settings.API_V1_STR}/openapi.json",  # 将 API 文档放在自定义路径以避免默认路径被暴露
    # generate_unique_id_function=custom_generate_unique_id,  # TODO 通过自定义逻辑增强路由唯一性或实现更符合业务需求的 ID。
    # docs_url=None,  # 关闭默认的文档路由 TODO 有方法关闭部分接口
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


# 项目启动 uvicorn app.main:app --reload
# swagger ui http://127.0.0.1:8000/docs#/