from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./backend/)
        env_file="../.env",  # .env 文件位于项目的顶层目录（../ 表示比当前目录高一级）。
        env_ignore_empty=True,  # 当这个选项设置为 True 时，空的环境变量会被忽略。如果某个环境变量的值是空字符串（"" 或 None），不会将其加载到配置中
        extra="ignore",  # 如果在 .env 文件或环境变量中存在未在 Settings 类中定义的字段，这些字段会被忽略。这可以避免意外加载无关的环境变量。
    )
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "A Structure Code"

    DB_USERNAME: str = 'goboy'
    DB_PASSWORD: str = '123456'
    DB_HOST: str = 'localhost'
    DB_PORT: str = '13306'
    DB_DATABASE: str = 'fastest'
    DB_CHARSET: str = 'utf8mb4'
    SQLALCHEMY_DATABASE_URI: str = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}?charset={DB_CHARSET}'

    # 配置Redis连接
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 16379
    REDIS_DB: int = 1
    REDIS_PASSWORD: Optional[str] = None  # 如果没有密码则为 None
    REDIS_POOL_MAX: int = 10
    REDIS_URL: str = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'

    # celery
    CELERY_BROKER_URL: str = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'
    CELERY_RESULT_BACKEND: str = f'db+mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}'

    LOG_FILE: str = 'logs/work.log'
    LOG_TZ: str = "Asia/Shanghai"
    LOG_FORMAT: str = '%(asctime)s,%(msecs)d %(levelname)-2s [%(filename)s:%(lineno)d] %(req_id)s %(message)s'


settings = Settings()  # type: ignore
