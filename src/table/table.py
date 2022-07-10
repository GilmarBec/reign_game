from src.reign.reign import Reign


class Table:
    __reigns: [Reign]
    __difficulty: int

    def __init__(self, n_players: int, difficulty: int):
        self.__reigns = [Reign(i) for i in range(n_players)]
        self.__difficulty = difficulty

    def attack(self) -> None:
        pass

    def change_current_player(self) -> None:
        pass

    def end_turn(self) -> None:
        pass

    def get_current_reign(self) -> Reign:
        pass

    def get_reign(self, reign_id: int) -> Reign:
        pass

    def verify_end_game(self) -> bool:
        pass
