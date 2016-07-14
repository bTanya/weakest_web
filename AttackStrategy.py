import random
from abc import ABCMeta, abstractmethod


class AttackStrategy:
    __metaclass__ = ABCMeta

    @abstractmethod
    def select_squad(self, army):
        pass


class Random(AttackStrategy):

    def select_squad(self, army):
        squads = army.get_squads
        random_squad = random.randint(0, len(squads) - 1)
        return squads[random_squad]


class Weakest(AttackStrategy):

    def select_squad(self, army):
        res = None
        squads = army.get_squads
        min_experience = min([i.get_experience for i in squads])
        for i in squads:
            if i.get_experience == min_experience:
                res = i
                break
            else:
                res = None
        return res


class Strongest(AttackStrategy):

    def select_squad(self, army):
        res = None
        squads = army.get_squads
        max_experience = max([i.get_experience for i in squads])
        for i in squads:
            if i.get_experience == max_experience:
                res = i
                break
            else:
                res = None
        return res

