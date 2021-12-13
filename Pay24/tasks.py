from trading_django.celery import app

from .models import Category, Service
from celery.schedules import crontab

import requests


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=0, hour=0)
    )


@app.task(name='yield_categories_and_services')
def yield_categories_and_services():

    return
