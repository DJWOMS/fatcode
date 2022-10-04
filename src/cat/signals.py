from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Cat, Inventory
from src.profiles.models import FatUser


@receiver(post_save, sender=FatUser)
def create_cat(sender, instance, created, **kwargs):
    if created:
        Cat.objects.create(user=instance)


@receiver(post_save, sender=Cat)
def create_inventory(sender, instance, created, **kwargs):
    if created:
        Inventory.objects.create(cat=instance)
