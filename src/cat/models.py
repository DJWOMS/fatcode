from django.db import models
from django.conf import settings

from src.courses.models import Lesson
from src.base.generate_path import cat_directory_path, product_directory_path


class Cat(models.Model):
    fat = models.IntegerField(default=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cat')
    avatar = models.ImageField(upload_to=cat_directory_path, null=True, blank=True)
    xp = models.IntegerField(default=0, editable=False)
    level = models.IntegerField(default=0, editable=False)
    die = models.BooleanField(default=False)
    hp = models.IntegerField(default=100)
    next_level_xp = models.IntegerField(default=100)
    hungry = models.IntegerField(default=100, editable=False)
    name = models.CharField(max_length=500, default='Толик')
    color = models.CharField(max_length=500, default='#000000')
    help_count = models.IntegerField(default=3)

    def __str__(self):
        return f"User id: {self.user_id}, Cat id: {self.id}"


class Phrase(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    text = models.TextField()
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name='inventory')

    def __str__(self):
        return f"Cat id: {self.cat.id}"


class Hint(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='cat_hint')
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name='hint')

    def __str__(self):
        return f"Cat id: {self.cat.id}"


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

    def __str__(self):
        return self.name


class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='item_product')
    quantity = models.IntegerField()
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='item')

    def __str__(self):
        return f"Product: {self.product.name}, inventory: {self.inventory.cat.id}"


class Achievement(models.Model):
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name='achievement')
    text = models.TextField()

    def __str__(self):
        return f"Cat ID: {self.cat.id}"
