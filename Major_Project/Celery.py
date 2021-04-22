from __future__ import absolute_import,unicode_literals
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Major_Project.settings')
app = Celery('Major_Project')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')

#app.timezone = 'Asia/Kolkata'

app.conf.beat_schedule = {
    "add_to_db":{
        "task":"Portfolio.views.update_real_time",
        "schedule":30,
    }
}

app.autodiscover_tasks()

@app.task(bind = True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))

