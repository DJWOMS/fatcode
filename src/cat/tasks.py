from fatcode.celery import app
from celery import shared_task


@shared_task
def example():
    print('test')
