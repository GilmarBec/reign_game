class Card:
    __was_chosen: bool
    __is_joker: bool

    def reveal(self):
        if self.__was_chosen:
            raise AssertionError("Card Already chosen")

        self.__was_chosen = True
        return self.__is_joker
