from src.board.board import Board
from src.common.utils.array import rotate
from src.reign.reign import Reign


class Table:
    __current_reign: Reign
    __difficulty: int
    __reigns: [Reign]

    def __init__(self, n_players: int, difficulty: int):
        self.__reigns = [Reign(i) for i in range(n_players)]
        self.__current_reign = self.__reigns[0]
        self.__difficulty = difficulty

    @property
    def reigns(self) -> [Reign]:
        return [self.get_reign(i) for i in range(len(self.__reigns))]

    def attack(self, defender_reign_id: int) -> Board:
        self.__current_reign.times_omitted = 0

        return Board(
            difficulty=self.__difficulty,
            attacker=self.__current_reign,
            defender=self.get_reign(defender_reign_id)
        )

    def __change_current_player(self) -> None:
        ordered_reigns = rotate(self.reigns, self.current_reign.id + 1)
        ordered_reigns = [reign for reign in ordered_reigns if reign.overlord is None]

        self.__current_reign = ordered_reigns[0]

    def end_turn(self) -> bool:
        if self.__current_reign.times_omitted >= 2:
            return False

        self.__current_reign.times_omitted += 1
        self.__change_current_player()
        return True

    @property
    def current_reign(self) -> Reign:
        return self.__current_reign

    def get_reign(self, reign_id: int) -> Reign:
        for reign in self.__reigns:
            if reign.id == reign_id:
                return reign

        raise AssertionError(f'Reign with ID[{reign_id}] not exists')

    def verify_end_game(self) -> bool:
        reign = self.__current_reign
        if reign.overlord:
            reign = reign.overlord

        if len(reign.vassals) == len(self.__reigns) - 1:
            return True

        self.__change_current_player()
        return False
