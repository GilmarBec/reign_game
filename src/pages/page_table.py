from tkinter import Button, Frame, Label, Canvas, Event

from src.constants.reign import SYMBOLS, COLORS
from src.pages.abstract_page import AbstractPage


class PageTable(AbstractPage):
    def __init__(self, window):
        super().__init__(window)

    @property
    def page_name(self):
        return 'TABLE'

    def build(self, data: any = None):
        self.build_frame()

        # n_players = data['n_players']
        # difficulty = data['difficulty']

        self.build_frame_players_list()
        self.build_frame_table()

        Button(self._frame, text='🔙', command=self._go_to_menu, font=("Arial", 25))\
            .grid(row=0, column=5, padx=10, pady=10, ipady=0)

        Button(self._frame, text='Passar a Vez ⏩', command=self.__pass_round, font=("Arial", 20))\
            .grid(row=4, column=4, padx=10, pady=10, sticky='e')

        self._frame.pack()

    def build_frame_players_list(self):
        frame = Frame(self._frame, pady=10)
        frame.grid(row=1, column=0, padx=10, rowspan=2)

        for i in range(8):
            Label(frame, text=SYMBOLS[i], font=("Arial", 20)).grid(row=i, column=0, padx=10, pady=20)
            Label(frame, text='Reino', font=("Arial", 20)).grid(row=i, column=1, padx=10, pady=20)

    def build_frame_table(self):
        frame = Frame(self._frame, pady=50, padx=50)
        frame.grid(row=1, column=1, padx=10, rowspan=2, columnspan=4)

        canvas = Canvas(frame, height=600, width=1100, bg="#5A3828")
        self.__draw_map(canvas)

        canvas.pack()

    def __draw_map(self, canvas: Canvas):
        reign_width: int = 250
        reign_height: int = 250

        for row in range(2):
            for column in range(4):
                pad_left = 50 + column * reign_width
                pad_up = 50 + row * reign_height
                canvas.create_rectangle(
                    pad_left, pad_up,
                    reign_width + pad_left, reign_height + pad_up,
                    fill=COLORS[column+(row * 4)],
                    tags="reign"
                )

        canvas.tag_bind('reign', "<Button-1>", self.__attack)

    def __attack(self, event: Event):
        self.select_page('BOARD')

    def __pass_round(self):
        print('Passar a Vez')
