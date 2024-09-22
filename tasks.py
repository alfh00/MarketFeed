from celery_config import celery_app
from data_fetcher import fetch_and_store_data

@celery_app.task
def fetch_data_task():
    fetch_and_store_data()
