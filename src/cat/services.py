from .models import Cat


class CatService:

    def __init__(self, cat: Cat):
        self.cat = cat

    def _level_up(self):
        self.cat.level += 1
        return self.cat.save()

    def level_up(self):
        if self.cat.xp == 100:
            return self._level_up()

    def _kill(self):
        self.cat.die = True
        return self.cat.save()

    def _increase_xp(self,  xp):
        self.cat.xp = xp
        return self.cat.save()

