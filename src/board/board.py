from random import randint
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
    __current_action_selector: Reign = None
    __remaining_rounds: int = 0

    def __init__(self, difficulty: int, attacker: Reign, defender: Reign):
        self.__attacker = attacker
        self.__defender = defender
        self.__vassals = attacker.vassals + defender.vassals
        self.__difficulty = difficulty
        self.__state = STATES.ARMY_FAITH

    def army_faith(self) -> [bool, int]:
        [win, die_result] = self.__attacker.army_faith(self.__difficulty)

        if win:
            if len(self.__vassals) > 0:
                self.__state = STATES.REVOLT
                self.__remaining_rounds = len(self.__vassals)
                self.__current_action_selector = self.__vassals[0]
            else:
                self.__state = STATES.BATTLE
                self.initialize_card_game()
        else:
            self.__state = STATES.ARMY_BETRAYAL

        return [win, die_result]

    def army_betrayal(self) -> [bool, int]:
        [win, die_result] = self.__attacker.army_betrayal()

        if len(self.__vassals) > 0:
            self.__state = STATES.REVOLT
            self.__remaining_rounds = len(self.__vassals)
            self.__current_action_selector = self.__vassals[0]
        else:
            self.__state = STATES.BATTLE
            self.initialize_card_game()

        return [win, die_result]

    def select_card(self, row: int, column: int) -> bool:
        is_joker = self.__cards[row][column].reveal()
        self.__remaining_rounds -= 1

        if is_joker:
            winner = self.__current_action_selector
            if winner.overlord:
                winner = winner.overlord
            self.__vassals += [self.__defender]
        elif self.__remaining_rounds > 0:
            return False
        elif len(self.__attacker.vassals) and not (self.__current_action_selector == self.__attacker.vassals[-1]):
            if self.__current_action_selector == self.__attacker:
                index = 0
            else:
                index = self.__attacker.vassals.index(self.__current_action_selector) + 1

            self.__current_action_selector = self.__attacker.vassals[index]
            return False
        else:
            winner = self.__defender
            self.__vassals += [self.__attacker]

        self.handle_winner_vassals(winner)

        winner.vassals = self.__vassals
        winner.reset_army()

        self.__state = STATES.ENDED

        return is_joker

    def revolt(self) -> [bool, int]:
        response = [win, _] = self.__current_action_selector.revolt()

        self.__remaining_rounds -= 1

        if win:
            self.__vassals = list(filter(lambda vassal: vassal != self.__current_action_selector, self.__vassals))

        if self.__remaining_rounds == 0:
            self.__state = STATES.BATTLE
            self.initialize_card_game()
        else:
            self.__current_action_selector = self.__vassals[len(self.__vassals) - self.__remaining_rounds]

        return response

    def not_revolt(self) -> [bool, int]:
        response = self.__current_action_selector.not_revolt()

        self.__remaining_rounds -= 1

        if self.__remaining_rounds == 0:
            self.__state = STATES.BATTLE
            self.initialize_card_game()
        else:
            self.__current_action_selector = self.__vassals[len(self.__vassals) - self.__remaining_rounds]

        return response

    def handle_winner_vassals(self, winner: Reign) -> None:
        for vassal in self.__vassals:
            vassal.overlord = winner
            vassal.vassals = []
            vassal.reset_army()

    @property
    def current_action_selector(self) -> Reign:
        return self.__current_action_selector

    def initialize_card_game(self) -> None:
        overlords_cards = [[Card() for _ in range(5)], [Card()]]
        if self.__attacker.army + self.__defender.army == 10:
            overlords_cards = [[Card() for _ in range(5)] for _ in range(2)]

        self.__cards = ([[Card() for _ in range(5)] for _ in range(len(self.vassals))]) + overlords_cards

        joker_line = randint(0, len(self.__cards) - 1)
        joker_column = randint(0, len(self.__cards[joker_line]) - 1)
        self.__cards[joker_line][joker_column] = Card(is_joker=True)

        self.__remaining_rounds = self.__attacker.army
        self.__current_action_selector = self.__attacker

    @property
    def attacker(self) -> Reign:
        return self.__attacker

    @property
    def cards(self) -> [[Card]]:
        return self.__cards

    @property
    def defender(self) -> Reign:
        return self.__defender

    @property
    def state(self) -> int:
        return self.__state

    @property
    def vassals(self) -> [Reign]:
        return self.__vassals

    @property
    def difficulty(self) -> int:
        return self.__difficulty
