from .reign_constants import SYMBOLS, COLORS


class Reign:
    __DEFAULT_ARMY = 5

    __army: int = 5
    __color: str
    __id: int
    __overlord: any = None  # Auto reference
    __revolt_chance: int = 0  # Min: 0, Max: 15
    __symbol: str
    __vassals: [any] = []

    def __init__(self, identifier: int):
        self.__id = identifier
        self.__color = COLORS[identifier]
        self.__symbol = SYMBOLS[identifier]

    def reset_army(self) -> None:
        self.__army = self.__DEFAULT_ARMY

    def revolt(self) -> [bool, int]:
        pass

    def not_revolt(self) -> [bool, int]:
        pass

    def test_army_betrayal(self) -> [bool, int]:
        pass

    def test_army_faith(self) -> [bool, int]:
        pass

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
        return self.__id

    @property
    def symbol(self) -> str:
        return self.__symbol

    @property
    def vassals(self) -> [any]:
        return self.__vassals

    @vassals.setter
    def vassals(self, vassals: [any]):
        self.__vassals = vassals
