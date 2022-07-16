from random import randint
from tkinter import Button, Canvas, Frame, Label
from tkinter.messagebox import showinfo
from .board import Board
from .board_constants import STATES, CARDS
from src.common.pages import AbstractPage


class PageBoard(AbstractPage):
    __state: int
    __action_frame: Frame
    __board: Board

    def __init__(self, window):
        super().__init__(window)

    @property
    def page_name(self) -> str:
        return 'BOARD'

    def build(self, data: any = None) -> None:
        if data is not None:
            self.__board = data

        self._build_frame()
        self.__draw_attacker_side()
        self.__draw_defender_side()

        self.__action_frame = Frame(self._frame, pady=10, padx=10)
        self.__action_frame.grid(row=0, column=1, padx=10, rowspan=2)

        self.__update_phase_frame()

        Button(self._frame, text='🔙', command=self._go_to_menu, font=("Arial", 25))\
            .grid(row=0, column=3, padx=10, pady=10, sticky='ne')

        self._frame.pack(padx=50, pady=50)

    def __draw_attacker_side(self) -> None:
        frame = Frame(self._frame, pady=10, padx=10)
        frame.grid(row=0, column=0, padx=10, rowspan=2)

        canvas = Canvas(frame, height=600, width=250)

        self.__draw_attacker(canvas)

        canvas.pack()

    def __draw_attacker(self, canvas) -> None:
        attacker = self.__board.attacker
        attacker_vassals = attacker.vassals

        reign_width: int = 200
        reign_height: int = 200
        pad_left = 25
        pad_up = 25

        canvas.create_rectangle(
            pad_left, pad_up,
            reign_width + pad_left, reign_height + pad_up,
            fill=attacker.color
        )

        pad_up += 25 + reign_height

        for i in range(len(attacker_vassals)):
            line_end = False
            reign_height = 75
            reign_width = 75

            if i % 2 != 0 and i != 0:
                pad_left += (reign_width + 50)
                line_end = True
                canvas.create_rectangle(
                    pad_left, pad_up,
                    reign_width + pad_left, reign_height + pad_up,
                    fill=attacker_vassals[i].color
                )
            else:
                pad_left = 25
                line_end = False
                canvas.create_rectangle(
                    pad_left, pad_up,
                    reign_width + pad_left, reign_height + pad_up,
                    fill=attacker_vassals[i].color
                )

            if line_end:
                pad_up += 25 + reign_height

    def __draw_defender_side(self) -> None:
        frame = Frame(self._frame, pady=10, padx=10)
        canvas = Canvas(frame, height=600, width=250)

        self.__draw_defender(canvas)

        canvas.pack()
        frame.grid(row=0, column=2, padx=10, rowspan=2)

    def __draw_defender(self, canvas) -> None:
        defender = self.__board.defender
        defender_vassals = defender.vassals

        reign_width: int = 200
        reign_height: int = 200
        pad_left = 25
        pad_up = 600 - 25 - reign_height

        canvas.create_rectangle(
            pad_left, pad_up,
            reign_width + pad_left, reign_height + pad_up,
            fill=defender.color
        )

        pad_up = pad_up - 100

        for i in range(len(defender_vassals)):
            line_end = False
            reign_height = 75
            reign_width = 75

            if i % 2 != 0 and i != 0:
                pad_left += (reign_width + 50)
                line_end = True
                canvas.create_rectangle(
                    pad_left, pad_up,
                    reign_width + pad_left, reign_height + pad_up,
                    fill=defender_vassals[i].color
                )
            else:
                pad_left = 25
                line_end = False
                canvas.create_rectangle(
                    pad_left, pad_up,
                    reign_width + pad_left, reign_height + pad_up,
                    fill=defender_vassals[i].color
                )

            if line_end:
                pad_up = pad_up - 25 - reign_height

    def __build_army_faith(self) -> None:
        self.__build_dice_test('Teste de Exército Nativo')

    def __build_army_betrayal(self) -> None:
        self.__build_dice_test('Teste de Conquista de Exército Inimigo')

    def __build_dice_test(self, title: str) -> None:
        Label(self.__action_frame, text=title, font=("Arial", 20)).pack()

        dice = Label(self.__action_frame, text='🎲', font=("Arial", 200))
        dice.bind('<Button-1>', self.__roll_dice)
        dice.pack()

        Label(self.__action_frame, text='Precisa tirar maior que 10 para Vitória.', font=("Arial", 20)).pack()

    def __build_revolt_option(self) -> None:
        Label(self.__action_frame, text='Chance de Rebelião', font=("Arial", 20)).pack()

        sword = Label(self.__action_frame, text='⚔  45% de sucesso', cursor='hand2', font=("Arial", 30))
        sleep = Label(self.__action_frame, text='⏳ +15% de sucesso', cursor='exchange', font=("Arial", 30))

        sword.bind('<Button-1>', self.__revolt)
        sleep.bind('<Button-1>', self.__omit)

        sword.pack()
        sleep.pack()

        Label(self.__action_frame, text='Precisa tirar maior que 9 para Vitória.', font=("Arial", 20)).pack()

    def __build_card_game(self) -> None:
        joker_position = (0, 0)

        for i in range(5):
            for j in range(5):
                is_joker = i == joker_position[0] and j == joker_position[1]

                label = Label(self.__action_frame, text='🂠', font=("Arial", 80))
                label.grid(row=i, column=j)

                if is_joker:
                    label.bind('<Button-1>', (
                        lambda event, row=i, column=j: self.__turn_joker(row, column)
                    ))
                else:
                    label.bind('<Button-1>', (
                        lambda event, row=i, column=j: self.__turn_card(row, column)
                    ))

    def __turn_card(self, row, column) -> None:
        card = CARDS[randint(0, len(CARDS) - 1)]

        label = Label(self.__action_frame, text=card, font=("Arial", 80))
        label.grid(row=row, column=column)

    def __turn_joker(self, row, column) -> None:
        label = Label(self.__action_frame, text='🃏', font=("Arial", 60))
        label.grid(row=row, column=column)
        showinfo('Vitória', 'Ataque bem sucedido!')
        self.__go_to_table()

    def __revolt(self, event) -> None:
        self.__update_phase_frame()

        if self.__state == STATES.REVOLT:
            self.__build_card_game()
            showinfo(
                'Resultado 🎲 = 8',
                'O teste resultou em 🎲8.\nVocê falhou em se rebelar.\nAgora seu suserano está de olho em você.'
                '\n\n-15% de chance de Rebelião!'
            )

    # not_revolt
    def __omit(self, event) -> None:
        [win, revolt_chance] = self.__board.not_revolt()

        message = 'Você decidiu esperar, você esperou de mais!\n' \
                  'Rumores de que você não está apto para ser rei se espalham.\n'

        if win:
            message = 'Você decidiu esperar, ganhando confiança do seu suserano.\n'

        showinfo('Decidiu esperar', message + f'Sua chance de revolta agora é {revolt_chance}.')

        self.__update_phase_frame()

    def __roll_dice(self, event) -> None:
        self.__update_phase_frame(False)

        if self.__state == STATES.ARMY_FAITH:
            [win, die_result] = self.__board.army_faith()

            message = 'Seu exército não acredita que você fez a escolha certa ao declarar este ataque!'
            if win:
                message = 'Seu exército estará com você nessa batalha!'

            self._notify_message(f'Resultado 🎲 = {die_result}\n\n{message}')
        elif self.__state == STATES.ARMY_BETRAYAL:
            [win, die_result] = self.__board.army_faith()

            message = 'Você não conseguiu convencer o exército neutro a se juntar a você nessa batalha!'
            if win:
                message = 'O exército neutro adentrou a sua causa temporariamente!'

            self._notify_message(f'Resultado 🎲 = {die_result}\n\n{message}')

        self.__update_phase_frame()

    def __update_phase_frame(self, update_state: bool = True) -> None:
        if update_state:
            self.__state = self.__board.state

        self.__action_frame.destroy()
        self.__action_frame = Frame(self._frame, pady=10, padx=10)
        self.__action_frame.grid(row=0, column=1, padx=10, rowspan=2)

        if self.__state == STATES.ARMY_FAITH:
            self.__build_army_faith()

        elif self.__state == STATES.ARMY_BETRAYAL:
            self.__build_army_betrayal()

        elif self.__state == STATES.REVOLT:
            self.__build_revolt_option()

        elif self.__state == STATES.BATTLE:
            self.__build_card_game()

    def __go_to_table(self) -> None:
        self._select_page('TABLE')
        self._reset_board()

    def _reset_board(self) -> None:
        self.__state = STATES.ARMY_FAITH
