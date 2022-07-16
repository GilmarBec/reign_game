from random import randint

from .reign_constants import SYMBOLS, COLORS


class Reign:
    __DEFAULT_ARMY = 5

    __army: int = 5
    __color: str
    __id: int
    __overlord: any = None  # Auto reference
    __revolt_chance: int = 0  # Min: 0, Max: 15
    __symbol: str
    __vassals: [any]
    __times_omitted: int = 0

    def __init__(self, identifier: int):
        self.__id = identifier
        self.__color = COLORS[identifier]
        self.__symbol = SYMBOLS[identifier]
        self.__vassals = []

    def reset_army(self) -> None:
        self.__army = self.__DEFAULT_ARMY

    def revolt(self) -> [bool, int]:
        random_n = randint(0, 20)

        if random_n >= 20 - self.__revolt_chance:
            self.__revolt_chance = 0
            self.__overlord.vassals = list(filter(lambda vassal: vassal != self, self.__overlord.vassals))
            self.__overlord = None
            return [True, random_n]

        if self.__revolt_chance >= 9:
            self.__revolt_chance -= 3

        return [False, self.__revolt_chance]

    def not_revolt(self) -> [bool, int]:
        if self.__revolt_chance >= 15:
            self.__revolt_chance = 9
            return [False, self.__revolt_chance]

        self.__revolt_chance += 3
        return [True, self.__revolt_chance]

    def army_betrayal(self) -> [bool, int]:
        random_n = randint(0, 20)

        if random_n >= 14:
            self.__army += 4
            return [True, random_n]

        return [False, random_n]

    def army_faith(self, difficulty) -> [bool, int]:
        loose_chance = (difficulty * 2) + len(self.vassals)
        random_n = randint(0, 20)

        if random_n >= loose_chance:
            return [True, random_n]

        self.__army = 1
        return [False, random_n]

    @property
    def army(self):
        return self.__army

    @property
    def color(self) -> str:
        return self.__color

    @property
    def id(self) -> int:
        return self.__id

    @property
    def overlord(self) -> any:
        return self.__overlord

    @property
    def revolt_chance(self) -> int:
        return self.__revolt_chance

    @property
    def symbol(self) -> str:
        return self.__symbol

    @property
    def vassals(self) -> [any]:
        return self.__vassals

    @vassals.setter
    def vassals(self, vassals: [any]):
        self.__vassals = vassals

    @overlord.setter
    def overlord(self, overlord: any):
        self.__overlord = overlord

    @property
    def times_omitted(self):
        return self.__times_omitted

    @times_omitted.setter
    def times_omitted(self, number: int):
        self.__times_omitted = number
