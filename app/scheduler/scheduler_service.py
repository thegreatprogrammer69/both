from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


class SchedulerService:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()

    def start(self):
        self.scheduler.start()

    def add_cron_job(self, job_id: str, func, cron_expr: str, **kwargs):
        minute, hour, day, month, dow = cron_expr.split()
        trigger = CronTrigger(minute=minute, hour=hour, day=day, month=month, day_of_week=dow)
        self.scheduler.add_job(func, trigger=trigger, id=job_id, kwargs=kwargs, replace_existing=True)

    def remove_job(self, job_id: str):
        self.scheduler.remove_job(job_id)
