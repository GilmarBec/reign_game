class Card:
    __was_chosen: bool = False
    __is_joker: bool

    def __init__(self, is_joker: bool = False):
        self.__is_joker = is_joker

    def reveal(self):
        if self.__was_chosen:
            raise AssertionError("Card Already chosen")

        self.__was_chosen = True
        if self.__is_joker:
            print("vo mata a mãe do batman")
        return self.__is_joker

    @property
    def is_joker(self):
        return self.__is_joker
