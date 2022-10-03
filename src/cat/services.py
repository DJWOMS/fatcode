from .models import Cat


class CatService:
    every_day_hungry = 10

    def __init__(self, cat: Cat):
        self.cat = cat

    def _level_up(self):
        self.cat.level += 1
        return self.cat.save()

    def level_up(self):
        if self.cat.xp == 100:
            return self._level_up()

    def _kill_cat(self):
        self.cat.die = True
        return self.cat.save()

    def _increase_xp(self,  xp):
        self.cat.xp = xp
        return self.cat.save()

    def hungry(self):
        if self.cat.hungry != 0:
            self.cat.hungry -= self.every_day_hungry
        else:
            if self.cat.hp != 0:
                self.cat.hp -= 10
            else:
                self._kill_cat()
        return self.cat.save()

