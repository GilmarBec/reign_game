from src.board.card import Card
from src.reign.reign import Reign


class Board:
    __attacker: Reign
    __defender: Reign
    __cards: [[Card]] = []
    __vassals: [Reign]
    __difficulty: int
    __state: int = 0
    __current_card_selector: Reign
    __remaining_rounds: int = 0

    def __init__(self, difficulty: int, attacker: Reign, defender: Reign):
        self.__attacker = attacker
        self.__defender = defender
        self.__vassals = attacker.vassals + defender.vassals
        self.__difficulty = difficulty

    def army_faith(self) -> [bool, int]:
        pass

    def army_betrayal(self) -> [bool, int]:
        pass

    def select_card(self) -> bool:
        pass

    def change_to_next_player(self) -> None:
        pass

    def revolt(self) -> [bool, int]:
        pass

    def not_revolt(self) -> [bool, int]:
        pass

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
