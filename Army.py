import Squad
import AttackStrategy


class Army:
    __squads = None
    __health = None
    __name_army = None

    def __init__(self, **kwargs):
        self.__name_army = str(kwargs.pop('name'))
        self.__squads = [Squad.Squad(**kwargs)
                         for _ in range(1, kwargs.pop('squads')+1)]

    def get_health(self):
        self.__health = sum([i.get_health for i in self.__squads])
        return self.__health

    def get_name(self):
        return self.__name_army

    @property
    def get_squads(self):
        return self.__squads

    def attack(self, army, strategy_):
        damage = sum([i.do_attack for i in self.__squads]) / \
                 len(self.__squads)
        if damage > 0:
            army.take_damage(damage, strategy_, army)

    @staticmethod
    def take_damage(damage, strategy_name, army):
        if strategy_name == 'random':
            strategy_ = AttackStrategy.Random()
        elif strategy_name == 'weakest':
            strategy_ = AttackStrategy.Weakest()
        else:
            strategy_ = AttackStrategy.Strongest()
        squad = strategy_.select_squad(army)
        squad.take_damage(damage)

