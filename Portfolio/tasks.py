from __future__ import absolute_import, unicode_literals

from celery import shared_task


from celery import Celery

import time

celery = Celery('Major_Project')


@shared_task
def print_data(a):
    print("A sample is sent to {}".format(a))