from celery import Celery
from celery.schedules import crontab
import os

# Configure Celery
celery_app = Celery(
    'tasks',
    broker=os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0'),
    backend=os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')
)

celery_app.conf.beat_schedule = {
    'run-every-day-at-midnight': {
        'task': 'tasks.your_task',
        'schedule': crontab(hour=0, minute=0),
        'args': ()
    },
}
celery_app.conf.timezone = 'UTC'