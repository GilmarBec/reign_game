from tkinter import Button, Label
from tkinter.ttk import Combobox

from src.common.pages import AbstractPage
from src.table.table import Table


class PageMenu(AbstractPage):
    __combobox: dict = {}

    def __init__(self, window):
        super().__init__(window)

    @property
    def page_name(self):
        return 'MENU'

    def build(self, data: any = None):
        self._build_frame()

        Label(self._frame, text='Jogo dos Reinos', font=("Arial", 100)).grid(
            row=1, column=1, padx=10, pady=50, columnspan=2
        )

        self.__combobox['n_players'] = self.__build_combobox(
            'Nº de Jogadores', [n_players for n_players in range(4, 9)],
            grid={'row': 2, 'column': 2, 'padx': 10, 'pady': 10}
        )
        self.__combobox['difficulty'] = self.__build_combobox(
            'Dificuldade', ['fácil', 'médio', 'difícil'],
            grid={'row': 3, 'column': 2, 'padx': 10, 'pady': 10}
        )

        Button(self._frame, text='Start', font=("Arial", 20), command=self.__start_game).grid(
            row=4, column=1, padx=10, pady=10, columnspan=2
        )

        self._frame.pack(padx=50, pady=50)

    def __build_combobox(self, title: str, values: list, grid):
        combobox = Combobox(self._frame, values=values, state='readonly', font=("Arial", 20))
        combobox.grid(grid)
        combobox.current(0)
        grid["column"] = grid["column"] - 1
        Label(self._frame, text=title, font=("Arial", 20)).grid(grid)

        return combobox

    def __start_game(self):
        self._select_page('TABLE', Table(
            n_players=int(self.__combobox['n_players'].get()),
            difficulty=self.__combobox['difficulty'].get(),
        ))
