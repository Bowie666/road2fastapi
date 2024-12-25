import os
import logging
import logging.config


def init_logging():
    '''
    这里目录配置比较复杂
    handlers 代表处理方式，一个是控制台 一个是文件，文件这块分两种，我用的是自动分割的功能
    loggers 代表日志器，这里配置了默认的日志器
    还有uvicorn的日志，它这一块有自带的日志，所以想要把控制台的日志打印出来，必须要替换它原来的配置
    handlers里面的console和file对应上文的配置
    '''
    # 确保日志目录存在
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": "DEBUG",
            },
            # "file": {
            #     "class": "logging.FileHandler",
            #     "filename": "logs/app.log",
            #     "formatter": "detailed",
            #     "level": "DEBUG",
            # },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",  # 使用轮转文件处理器
                "filename": os.path.join(log_dir, "app.log"),  # 日志文件路径
                "maxBytes": 1024 * 1024 * 5,  # 最大文件大小 5MB
                "backupCount": 3,  # 保留的历史文件数量
                "formatter": "default",  # 使用 default 格式化器
                "level": "DEBUG",  # 设置日志级别
            },
        },
        "loggers": {
            "app_logger": {
                "handlers": ["console", "file"],
                "level": "DEBUG",
                "propagate": False,
            },
            "uvicorn": {  # Add this block for uvicorn logs
                "handlers": ["console", "file"],
                "level": "DEBUG",  # Adjust based on your needs
                "propagate": False,
            },
            'uvicorn.access': {
                'handlers': ["console", "file"],
                'level': 'TRACE',
                'propagate': False
            },
            'uvicorn.error': { 
                'handlers': ["console", "file"],
                'level': 'TRACE',
                'propagate': False
            },
            'uvicorn.asgi': {
                'handlers': ["console", "file"],
                'level': 'TRACE',
                'propagate': False
            },
        },
        "root": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
        },
    }


    logging.config.dictConfig(LOGGING_CONFIG)
    # logger = logging.getLogger("fastapi_app")
    # logger.info("Logging configured successfully.")