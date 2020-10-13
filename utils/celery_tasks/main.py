from celery import Celery


celery_app = Celery('tensquare')
celery_app.config_from_object('utils.celery_tasks.config')
celery_app.autodiscover_tasks([
    'utils.celery_tasks.sms',
])



