from .models import Cat, Product, Item
from .settings import CatSettings
from src.profiles.services import CoinService


class CatService:
    settings = CatSettings

    def __init__(self, cat: Cat):
        self.cat = cat

    def _level_up(self):
        self.cat.level += 1
        self.cat.xp = 0

    def _kill_cat(self):
        self.cat.die = True
        return self.cat.save()

    def _increase_xp(self,  xp):
        self.cat.xp += xp
        if self.cat.xp >= self.cat.next_level_xp:
            self._level_up()
        return self.cat.save()

    def remove_hp(self):
        if self.cat.hp != 0:
            self.cat.hp -= self.settings.hungry_hp
        else:
            self._kill_cat()

    def hungry(self):
        if self.cat.hungry != 0:
            self.cat.hungry -= self.settings.every_day_hungry
        else:
            self.remove_hp()
        return self.cat.save()

    def buy_item(self, product: Product, quantity: int):
        coin_manager = CoinService(self.cat.user)
        if coin_manager.buy(product.price * quantity):
            item = Item.objects.create(product=product, inventory=self.cat.user.inventory, quantity=quantity)
            return item

    def check_inventory(self):
        queryset = Item.objects.filter(inventory=self.cat.user.inventory)
        return queryset
