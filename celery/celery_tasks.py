from celery_config import celery_app


@celery_app.task
def fetch_data_task():
    pass
