from apscheduler.schedulers.blocking import BlockingScheduler
import collect_data

sched = BlockingScheduler()

@sched.scheduled_job('cron', minute=0)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

sched.start()
