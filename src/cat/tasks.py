from celery import shared_task
from .models import Cat
from .services import CatService


@shared_task
def hungry_cat():
    queryset = Cat.objects.filter(die=False)
    for cat in queryset:
        cat_manager = CatService(cat)
        cat_manager.hungry()

