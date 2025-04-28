

async def cron_job():
    print('12345')


def get_task(scheduler):
    scheduler.add_job(cron_job, 'interval', seconds=5)
