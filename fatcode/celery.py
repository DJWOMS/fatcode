import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fatcode.settings')

app = Celery('fatcode')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'everyday-task': {
      'task': 'src.team.tasks.check_invitations',
      'schedule': crontab(minute=0, hour=0)
    }
}
