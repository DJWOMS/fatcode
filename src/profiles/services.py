from django.db.models import F

from src.profiles.models import FatUser


def add_experience(user_id: int, exp: int):
    new_exp = FatUser.objects.filter(id=user_id).update(expirience=F('experience') + exp)
    return new_exp


def add_coins(user_id: int, coin: int):
    user = FatUser.objects.get(id=user_id)
    user.coins += coin
    user.save()
    return user


def buy_with_coins(user_id: int, price: int):
    user = FatUser.objects.get(id=user_id)

    if user.coins >= price:
        user.coins -= price
        user.save()

    if user.coins < price:
        raise ValueError("Недостаточно монет")

    return user
