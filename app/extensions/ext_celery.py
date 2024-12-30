import os

import pytz
from celery import Celery

from app.configs import settings

'''
对目录要求很严格 不知道为什么 必须要起名为tasks.py 然后还要在下面注册 autodiscover_tasks
而且你不这么做 启动任务的时候还看不到你在tasks.py里面写的定时任务
目前日志问题还没解决 现在执行什么任务都不显示日志
'''
def init_celery():
    # 这个代码是防止报错ModuleNotFoundError: No module named 'MySQLdb' 老毛病了
    import pymysql
    pymysql.install_as_MySQLdb()

    celery_app = Celery(
        "fastworker",
        broker=settings.CELERY_BROKER_URL,
        # 是用于存储任务结果的后端。Celery 支持多种结果存储方式（例如数据库、Redis、RabbitMQ等）。这个配置项指定了存储任务结果的后端系统。
        # 如果任务需要返回结果，Celery 会将其存储在这个后端，并且可以在任务执行完成后从后端中获取结果。
        # backend=DefaultConfig.CELERY_BACKEND,  # 4.x开始弃用
        backend=settings.CELERY_RESULT_BACKEND,
        task_ignore_result=True,  # 忽略任务的返回结果
    )

    celery_app.conf.update(
        result_backend=settings.CELERY_RESULT_BACKEND,
        broker_connection_retry_on_startup=True,  # 连接重试 启动时自动重试连接到消息队列。
        worker_log_format=settings.LOG_FORMAT,
        worker_task_log_format=settings.LOG_FORMAT,
        worker_hijack_root_logger=False,
        timezone=pytz.timezone(settings.LOG_TZ),
        task_track_started=True,  # 启用任务跟踪
    )

    if settings.LOG_FILE:
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        celery_app.conf.update(
            worker_logfile=settings.LOG_FILE,
        )

    # Load task modules
    celery_app.autodiscover_tasks([
        'app.tasks'
    ])  
    celery_app.set_default()  # 设置 Celery 应用的默认配置。


    return celery_app


celery_app: Celery = init_celery()
