from celery import Celery
from django.conf import settings


app = Celery('rerotor2', broker='redis://', backend='redis://')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
