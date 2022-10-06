from celery import shared_task
from .models import Cat
from .services import CatService


@shared_task
def hungry_cat():
    queryset = Cat.objects.filter(die=False)
    for cat in queryset:
        cat_service = CatService(cat)
        cat_service.hungry()


@shared_task
def update_hint():
    queryset = Cat.objects.all()
    for cat in queryset:
        cat.help_count = 3
        cat.save()
