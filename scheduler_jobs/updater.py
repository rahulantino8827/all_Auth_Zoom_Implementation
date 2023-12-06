from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from .jobs import schedule_task

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(schedule_task, 'interval', seconds = 1)
    scheduler.start()


# @sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# def scheduled_job():
#     print('This job is run every weekday at 5pm.')

