from time import sleep
import logging

from celery import current_task, shared_task
from app.extensions.ext_celery import celery_app

# @shared_task(acks_late=True)  # acks_late=True保任务可靠性的重要选项。防止任务因 worker 异常退出而丢失，但需要任务逻辑幂等并考虑对队列性能的影响。
@celery_app.task  # 这一块最好只用celery app去建任务 不然的话不会存到表里面
def long_task() -> str:
    for i in range(1, 11):
        sleep(1)
        current_task.update_state(
            # 这是任务的当前状态。
            # 默认情况下，Celery 任务只有两个状态：PENDING（任务被创建但尚未执行）和 SUCCESS（任务成功完成）。
            state='PROGRESS',
            # 传递任务的附加信息，比如进度百分比、运行结果、日志等
            meta={
                'process_percent': i*10
                }
            )
    # logging.info("task success")
    return "time task return"


# 不知道为什么 shared_task建的任务不会到表里面
@shared_task
def shot_task() -> str:
    sleep(20)  # 模拟耗时操作
    logging.info("task success")
    return "time task return"
