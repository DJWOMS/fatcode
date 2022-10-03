from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cat, Inventory


@receiver(post_save, sender=Cat)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Inventory.objects.create(cat=instance)