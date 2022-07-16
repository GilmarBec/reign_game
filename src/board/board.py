from src.board.board_constants import STATES
from src.board.card import Card
from src.reign.reign import Reign


class Board:
    __attacker: Reign
    __defender: Reign
    __cards: [[Card]] = []
    __vassals: [Reign]
    __difficulty: int
    __state: int
    __current_action_selector: Reign
    __remaining_rounds: int = 0

    def __init__(self, difficulty: int, attacker: Reign, defender: Reign):
        self.__attacker = attacker
        self.__defender = defender
        self.__vassals = attacker.vassals + defender.vassals
        self.__difficulty = difficulty
        self.__state = STATES.REVOLT

    def army_faith(self) -> [bool, int]:
        [win, die_result] = self.__attacker.army_faith(self.__difficulty)

        if win:
            if len(self.__vassals) > 0:
                self.__state = STATES.REVOLT
            else:
                self.__state = STATES.BATTLE
        else:
            self.__state = STATES.ARMY_BETRAYAL

        return [win, die_result]

    def army_betrayal(self) -> [bool, int]:
        [win, die_result] = self.__attacker.army_betrayal()

        if len(self.__vassals) > 0:
            self.__state = STATES.REVOLT
        else:
            self.__state = STATES.BATTLE

        return [win, die_result]

    def select_card(self) -> bool:
        pass

    def change_to_next_player(self) -> None:
        pass

    def revolt(self) -> [bool, int]:
        if self.__remaining_rounds == 0:
            self.__remaining_rounds = len(self.__vassals)

        response = [win, revolt_chance] = self.__current_action_selector.revolt()

        self.__remaining_rounds -= 1

        return response

    def not_revolt(self) -> [bool, int]:
        self.__vassals = [Reign(1), Reign(2)]
        if self.__remaining_rounds == 0:
            self.__remaining_rounds = len(self.__vassals)
            self.__current_action_selector = self.__vassals[0]

        response = self.__current_action_selector.not_revolt()

        self.__remaining_rounds -= 1

        if self.__remaining_rounds == 0:
            self.__state = STATES.BATTLE
            self.initialize_card_game()
        else:
            self.__current_action_selector = self.__vassals[len(self.__vassals) - self.__remaining_rounds]

        return response

    def handle_winner_vassals(self, winner: Reign) -> None:
        pass

    def get_current_card_selector(self) -> Reign:
        pass

    def decrement_remaining_rounds(self) -> None:
        pass

    def initialize_card_game(self) -> None:
        pass

    @property
    def attacker(self) -> Reign:
        return self.__attacker

    @property
    def defender(self) -> Reign:
        return self.__defender

    @property
    def state(self) -> int:
        return self.__state

    @property
    def vassals(self) -> [Reign]:
        return self.__vassals
