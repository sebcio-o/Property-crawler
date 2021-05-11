import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "properties.settings")
app = Celery("properties", broker="'redis://redis:6379/0'")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "onthemarket": {
        "task": "crawlers.tasks.run_all_crawlers",
        "schedule": crontab(minute=0, hour=0),
    },
}
