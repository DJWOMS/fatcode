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
            return self.user.save()
