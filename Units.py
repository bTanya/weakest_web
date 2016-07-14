import random
import time
from abc import ABCMeta, abstractmethod, abstractproperty


class Unit:
    __metaclass__ = ABCMeta
    __health = None
    __recharge = None
    __next_attack_time = 0
    prev_time = None

    @abstractproperty
    def do_attack(self):
        # атака
        pass

    @abstractmethod
    def take_damage(self, *args):
        # получение атаки и блок
        pass

    @property
    def get_recharge(self):
        return self.__recharge

    def set_recharge(self, recharge):
        self.__recharge = recharge

    @property
    def get_health(self):
        return self.__health

    def set_health(self, health):
        self.__health = health

    @abstractproperty
    def get_experience(self):
        pass

    @property
    def get_next_attack_time(self):
        return self.__next_attack_time

    def set_next_attack_time(self, next_attack_time):
        self.__next_attack_time = next_attack_time

    def check_attack(self):
        now = time.time() * 1000
        if self.prev_time is None:
            return True
        else:
            next_time = self.prev_time + self.get_recharge
            if now >= next_time:
                return True
            else:
                return False


class Solder(Unit):
    __experience = 0

    def __init__(self):
        self.set_health(100)
        self.set_recharge(random.randint(100, 2000) / 10000)

    @property
    def get_experience(self):
        return self.__experience

    def set_experience(self):
        if self.__experience < 50:
            self.__experience += 1

    @property
    def do_attack(self):
        if self.get_health > 0 and self.check_attack():
            soldiers_attack = 0.5 * (1 + self.get_health) * \
                random.randint(50 + self.__experience, 100) / 100
            self.set_experience()
            self.prev_time = time.time() * 1000
            return soldiers_attack
        else:
            return 0

    def take_damage(self, damage):
        attack = damage - (0.05 + self.__experience / 1000)
        self.set_health(self.get_health - attack)


class Vehicles(Unit):
    operators = []

    def __init__(self):
        self.set_recharge(random.randint(1000, 2000) / 10000)
        operator_count = random.randint(1, 3)
        self.operators = [Solder() for _ in range(0, operator_count)]
        list_operators = [i.get_health for i in self.operators]
        self.set_health(sum(list_operators) / len(list_operators))

    def get_operators(self):
        return self.operators

    @property
    def get_experience(self):
        return sum([i.get_experience for i in self.operators])

    @staticmethod
    def alive(units):
        res = False
        for i in units:
            if i.get_health > 0:
                res = True
                break
        return res

    @property
    def do_attack(self):
        if self.get_health > 0 and self.check_attack() \
                and self.alive(self.operators):
            list_attack_soldiers = [i.do_attack for i in
                                    self.operators]
            vehicles_attack = 0.5 * (1 + self.get_health / 100) * (
                sum(list_attack_soldiers) / len(list_attack_soldiers))
            self.prev_time = time.time() * 1000
            return vehicles_attack
        else:
            return 0

    def take_damage(self, damage):
        list_operators_experience = [i.get_experience / 1000 for i in
                                     self.operators]
        damage -= 0.1 + sum(list_operators_experience)
        # 60% урона на машину
        self.set_health(self.get_health - damage * 0.6)
        # случайный оператор, который получит 20% урона
        random_operator = random.randint(0, len(self.operators) - 1)
        j = 0
        while j < len(self.operators):
            if j == random_operator:
                self.operators[j].take_damage(damage * 0.2)
            else:
                self.operators[j].take_damage(damage * 0.1)
            j += 1

