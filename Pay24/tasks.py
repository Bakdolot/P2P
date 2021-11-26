from trading_django.celery import app
from .models import Category, Service
import requests


@app.task(name='yield_categories_and_services')
def yield_categories_and_services():

    return