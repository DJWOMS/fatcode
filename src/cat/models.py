from django.db import models
from django.conf import settings
from src.courses.models import Lesson
import uuid


def cat_directory_path(instance: 'Cat', filename: str) -> str:
    """Generate path to file in upload"""
    return f'cat/avatar/user_{instance.id}/{str(uuid.uuid4())}.{filename.split(".")[-1]}'

def product_directory_path(instance: 'Product', filename: str) -> str:
    """Generate path to file in upload"""
    return f'product/image/product_{instance.id}/{str(uuid.uuid4())}.{filename.split(".")[-1]}'


class Cat(models.Model):
    fat = models.IntegerField(default=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cat'
    )
    avatar = models.ImageField(
        upload_to=cat_directory_path,
        null=True,
        blank=True,
    )
    xp = models.IntegerField(default=0, editable=False)
    level = models.IntegerField(default=0, editable=False)
    die = models.BooleanField(default=False)
    hp = models.IntegerField(default=100)
    next_level_xp = models.IntegerField(default=100)
    hungry = models.IntegerField(default=100, editable=False)
    name = models.CharField(max_length=500, default='Толик')
    color = models.CharField(max_length=500, default='#000000')
    help_count = models.IntegerField(default=3)


class Phrase(models.Model):
    text = models.TextField()
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)


class Inventory(models.Model):
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name='inventory')


class Hint(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='cat_hint')
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name='hint')


class Category(models.Model):
    name = models.CharField(max_length=30)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    TYPE_CHOICES = (
        ('toy', 'Игрушка'),
        ('hair', 'Прическа'),
        ('food', "Еда")
    )
    name = models.CharField(max_length=300)
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    genus = models.CharField(max_length=50, choices=TYPE_CHOICES)
    image = models.ImageField(upload_to=product_directory_path)
    json = models.JSONField()


class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='item')
    quantity = models.IntegerField()
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='item')


class Achievement(models.Model):
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name='achievement')
    text = models.TextField()