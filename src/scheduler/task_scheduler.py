from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


class TaskScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()

    def start(self):
        if not self.scheduler.running:
            self.scheduler.start()

    def schedule(self, job_id: str, cron_expr: str, fn, *args, **kwargs):
        minute, hour, day, month, dow = cron_expr.split()
        trigger = CronTrigger(minute=minute, hour=hour, day=day, month=month, day_of_week=dow)
        self.scheduler.add_job(fn, trigger=trigger, id=job_id, replace_existing=True, args=args, kwargs=kwargs)

    def remove(self, job_id: str):
        self.scheduler.remove_job(job_id)
