from tkinter import Button, Frame, Label, Canvas, Event
from tkinter.font import BOLD, Font
from src.common.pages import AbstractPage
from src.table.table import Table


class PageTable(AbstractPage):
    __table: Table

    def __init__(self, window):
        super().__init__(window)

    @property
    def page_name(self) -> str:
        return 'TABLE'

    def build(self, data: Table or None = None) -> None:
        self._build_frame()

        if data:
            self.__table = data

        self.__build_frame_players_list(self.__table.current_reign.id)
        self.__build_frame_table()

        Button(self._frame, text='🔙', command=self._go_to_menu, font=("Arial", 25))\
            .grid(row=0, column=5, padx=10, pady=10, ipady=0)

        Button(self._frame, text='Passar a Vez ⏩', command=self.__end_turn, font=("Arial", 20))\
            .grid(row=4, column=4, padx=10, pady=10, sticky='e')

        self._frame.pack()

    def __build_frame_players_list(self, current_reign_id: int) -> None:
        font_simple = Font(family="Arial", size=20)
        font_bold = Font(family="Arial", size=20, weight=BOLD)
        frame = Frame(self._frame, pady=10)
        frame.grid(row=1, column=0, padx=10, rowspan=2)

        for reign in self.__table.reigns:
            font = font_simple
            if reign.id == current_reign_id:
                font = font_bold

            Label(frame, text=reign.symbol, font=font, fg=reign.color).grid(row=reign.id, column=0, padx=10, pady=20)
            Label(frame, text='Reino', font=font, fg=reign.color).grid(row=reign.id, column=1, padx=10, pady=20)

    def __build_frame_table(self) -> None:
        frame = Frame(self._frame, pady=50, padx=50)
        frame.grid(row=1, column=1, padx=10, rowspan=2, columnspan=4)

        canvas = Canvas(frame, height=600, width=1100, bg="#5A3828")
        self.__draw_map(canvas)

        canvas.pack()

    def __draw_map(self, canvas: Canvas) -> None:
        reign_width: int = 250
        reign_height: int = 250

        reigns_to_create = self.__table.reigns

        for row in range(2):
            for column in range(4):
                if not len(reigns_to_create):
                    break

                reign = reigns_to_create.pop(0)
                pad_left = 50 + column * reign_width
                pad_up = 50 + row * reign_height
                canvas.create_rectangle(
                    pad_left, pad_up,
                    reign_width + pad_left, reign_height + pad_up,
                    fill=reign.color,
                    tags="reign"
                )

        canvas.tag_bind('reign', "<Button-1>", self.__attack)

    def __attack(self, event: Event) -> None:
        self._select_page('BOARD')

    def __end_turn(self) -> None:
        self.__table.end_turn()
        self.__select_player()

    def __select_player(self) -> None:
        reign = self.__table.current_reign

        self._notify_message(f"Turno do reino {reign.id}")
        self.__indicate_reign(reign.id)

    def __indicate_reign(self, reign_id: int) -> None:
        self.__build_frame_players_list(reign_id)

    def end_game(self) -> None:
        pass

    def change_current_player(self) -> None:
        pass
