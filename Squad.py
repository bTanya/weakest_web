import Units


class Squad:
    __units = None
    __health = None

    def __init__(self, **kwargs):
        self.__units = [Units.Solder() for _ in range(1, kwargs['soldiers']+1)]
        self.__units += [Units.Vehicles() for _ in range(1, kwargs['vehicles']+1)]

    @property
    def get_experience(self):
        return sum([i.get_experience for i in self.__units])

    @property
    def get_health(self):
        self.__health = sum([i.get_health for i in self.__units])
        return self.__health

    @property
    def do_attack(self):
        return sum([i.do_attack for i in self.__units]) / len(self.__units)

    def take_damage(self, damage):
        damage /= len(self.__units)
        for i in self.__units:
            i.take_damage(damage)

