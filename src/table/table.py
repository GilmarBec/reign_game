from src.common.utils.array import rotate
from src.reign.reign import Reign


class Table:
    __reigns: [Reign]
    __current_reign: Reign
    __difficulty: int

    def __init__(self, n_players: int, difficulty: int):
        self.__reigns = [Reign(i) for i in range(n_players)]
        self.__current_reign = self.__reigns[0]
        self.__difficulty = difficulty

    @property
    def reigns(self) -> [Reign]:
        return [self.get_reign(i) for i in range(len(self.__reigns))]

    def attack(self) -> None:
        pass

    def change_current_player(self) -> None:
        pass

    def end_turn(self) -> None:
        ordered_reigns = rotate(self.reigns, self.current_reign.id + 1)

        for reign in ordered_reigns:
            if reign.overlord is None:
                self.__current_reign = reign
                break

    @property
    def current_reign(self) -> Reign:
        return self.__current_reign

    def get_reign(self, reign_id: int) -> Reign:
        for reign in self.__reigns:
            if reign.id == reign_id:
                return reign

        raise AssertionError(f'Reign with ID[{reign_id}] not exists')

    def verify_end_game(self) -> bool:
        pass
