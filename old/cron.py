from apscheduler.schedulers.blocking import BlockingScheduler
import collect_data

sched = BlockingScheduler()

@sched.scheduled_job('cron', minute=0)
def scheduled_job():
    collect_data.get_doomhammer()

sched.start()
