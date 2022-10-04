import decimal
from django.db.models import F
from src.profiles.models import FatUser


def add_experience(user_id: int, exp: int):
    new_exp = FatUser.objects.filter(id=user_id).update(expirience=F('experience') + exp)
    return new_exp


class CoinService:

    def __init__(self, user: FatUser):
        self.user = user

    def check_balance(self):
        return self.user.coins

    def buy(self, price):
        balance = self.check_balance()
        if balance > price:
            self.user.coins -= price
            self.user.save()
            return self.user
        raise ValueError('Недостаточно средств')


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
