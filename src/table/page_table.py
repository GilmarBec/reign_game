from tkinter import Button, Frame, Label, Canvas, Event
from tkinter.font import BOLD, Font
from src.common.pages import AbstractPage
from src.table.table import Table


class PageTable(AbstractPage):
    __table: Table

    @property
    def page_name(self) -> str:
        return 'TABLE'

    def build(self, data: Table or None = None) -> None:
        self._build_frame()

        if data:
            self.__table = data
        else:
            end_game = self.__table.verify_end_game()
            if end_game:
                self._notify_message(f"Game Over")
                self._go_to_menu()
                return
            self._notify_message("Vassalo(s) adicionado(s) ao novo suserano")

        self.__build_frame_players_list(self.__table.current_reign.id)
        self.__build_frame_table(self.__table.current_reign.id)

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
            background = "gray"
            relief = "raised"
            if reign.id == current_reign_id:
                font = font_bold
                relief = "sunken"
            if reign.overlord is not None:
                font = Font(family="Arial", size=20, overstrike=True)
                background = "light gray"
                relief = "ridge"

            Label(frame,
                  text=reign.symbol,
                  font=font,
                  fg=reign.color,
                  bg=background,
                  relief=relief,  # Label object accept str, but it's not documented
                  borderwidth=2).grid(row=reign.id, column=0, padx=10, pady=20)

            Label(frame,
                  text='Reino',
                  font=font,
                  fg=reign.color,
                  bg=background,
                  relief=relief,  # Label object accept str, but it's not documented
                  borderwidth=2).grid(row=reign.id, column=1, padx=10, pady=20)

    def __build_frame_table(self, current_reign_id: int) -> None:
        frame = Frame(self._frame, pady=50, padx=50)
        frame.grid(row=1, column=1, padx=10, rowspan=2, columnspan=4)

        canvas = Canvas(frame, height=600, width=1100, bg="#5A3828")
        self.__draw_map(canvas, current_reign_id)

        canvas.pack()

    def __draw_map(self, canvas: Canvas, current_reign_id: int) -> None:
        reign_width: int = 250
        reign_height: int = 250

        reigns_to_create = self.__table.reigns

        for row in range(2):
            for column in range(4):
                if not len(reigns_to_create):
                    canvas.tag_bind('reign', "<Button-1>", self.__attack)
                    return

                reign = reigns_to_create.pop(0)
                pad_left = 50 + column * reign_width
                pad_up = 50 + row * reign_height

                if reign.id == current_reign_id:
                    symbol_color = reign.color
                    symbol_size = 50
                else:
                    symbol_color = "dark gray"
                    symbol_size = 30

                canvas.create_rectangle(
                    pad_left, pad_up,
                    reign_width + pad_left, reign_height + pad_up,
                    fill=reign.color,
                    tags="reign"
                )

                start_left = pad_left + reign_width / 4
                start_up = pad_up + reign_height / 4
                width = 0
                outline = ''

                if reign.overlord is not None:
                    canvas.create_text(
                        (pad_left + 30, pad_up + 30),
                        text=reign.overlord.symbol,
                        font=Font(family="Arial", size=30),
                        fill=reign.overlord.color
                    )

                    width = 10
                    outline = reign.overlord.color

                canvas.create_rectangle(
                    start_left, start_up,
                    start_left + reign_width / 2, start_up + reign_height / 2,
                    fill="gray",
                    tags="reign",
                    width=width,
                    outline=outline,
                )

                canvas.create_text(
                    (pad_left + reign_width / 2, pad_up + reign_height / 2),
                    text=reign.symbol, font=Font(family="Arial", size=symbol_size),
                    fill=symbol_color, tags="reign"
                )

        canvas.tag_bind('reign', "<Button-1>", self.__attack)

    def __attack(self, event: Event) -> None:
        column, line = [((event.x - 50) // 250), ((event.y - 50) // 250)]
        defender_id = column + (line * 4)

        current_reign = self.__table.current_reign
        defender = self.__table.get_reign(defender_id)

        if defender.overlord is not None:
            defender = defender.overlord

        if defender.id == current_reign.id:
            self._notify_message("Reino inválido")
            return

        board = self.__table.attack(defender.id)
        self._select_page('BOARD', board)

    def __end_turn(self) -> None:
        end_turn = self.__table.end_turn()

        if not end_turn:
            self._notify_message(f"Ação impossível, o jogador já pulou 2 turnos!")
            return

        self.__select_player()

    def __select_player(self) -> None:
        reign = self.__table.current_reign

        self._notify_message(f"Turno do reino {reign.symbol}")
        self.__indicate_reign(reign.id)

    def __indicate_reign(self, reign_id: int) -> None:
        self.__build_frame_players_list(reign_id)
        self.__build_frame_table(reign_id)
