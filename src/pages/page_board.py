from random import randint
from tkinter import Button, Canvas, Frame, Label, Message
from tkinter.messagebox import showinfo

from src.constants.board import STATES, CARDS
from src.constants.reign import COLORS
from src.pages.abstract_page import AbstractPage


class PageBoard(AbstractPage):
    __phase: str
    __phase_frame: Frame

    def __init__(self, window):
        super().__init__(window)
        self.__phase = STATES[0]

    @property
    def page_name(self):
        return 'BOARD'

    def build(self, data: any = None):
        self.build_frame()
        self.__draw_attacker_side()
        self.__draw_defensor_side()

        self.__phase_frame = Frame(self._frame, pady=10, padx=10)
        self.__phase_frame.grid(row=0, column=1, padx=10, rowspan=2)

        self.__build_army_faith()

        Button(self._frame, text='🔙', command=self._go_to_menu, font=("Arial", 25))\
            .grid(row=0, column=3, padx=10, pady=10, sticky='ne')

        self._frame.pack(padx=50, pady=50)

    def __draw_attacker_side(self):
        frame = Frame(self._frame, pady=10, padx=10)
        frame.grid(row=0, column=0, padx=10, rowspan=2)

        canvas = Canvas(frame, height=600, width=250)

        self.__draw_attacker(canvas)

        canvas.pack()

    def __draw_attacker(self, canvas):
        reign_width: int = 200
        reign_height: int = 200
        pad_left = 25
        pad_up = 25

        canvas.create_rectangle(
            pad_left, pad_up,
            reign_width + pad_left, reign_height + pad_up,
            fill=COLORS[0]
        )

        pad_up += 25 + reign_height
        reign_height = int(reign_height / 2) - 25
        reign_width = int(reign_width / 2) - 25
        canvas.create_rectangle(
            pad_left, pad_up,
            reign_width + pad_left, reign_height + pad_up,
            fill=COLORS[1]
        )

        pad_left += reign_width + 50
        canvas.create_rectangle(
            pad_left, pad_up,
            reign_width + pad_left, reign_height + pad_up,
            fill=COLORS[2]
        )

    def __draw_defensor_side(self):
        frame = Frame(self._frame, pady=10, padx=10)
        canvas = Canvas(frame, height=600, width=250)

        self.__draw_defensor(canvas)

        canvas.pack()
        frame.grid(row=0, column=2, padx=10, rowspan=2)

    def __draw_defensor(self, canvas):
        reign_width: int = 200
        reign_height: int = 200
        pad_left = 25
        pad_up = 600 - 25 - reign_height

        canvas.create_rectangle(
            pad_left, pad_up,
            reign_width + pad_left, reign_height + pad_up,
            fill=COLORS[3]
        )

        reign_height = int(reign_height / 2) - 25
        reign_width = int(reign_width / 2) - 25
        pad_up = pad_up - 25 - reign_height
        canvas.create_rectangle(
            pad_left, pad_up,
            reign_width + pad_left, reign_height + pad_up,
            fill=COLORS[4]
        )

        pad_left += reign_width + 50
        canvas.create_rectangle(
            pad_left, pad_up,
            reign_width + pad_left, reign_height + pad_up,
            fill=COLORS[5]
        )

    def __build_army_faith(self):
        self.__build_dice_test('Teste de Exército Nativo')

    def __build_army_betrayal(self):
        self.__build_dice_test('Teste de Conquista de Exército Inimigo')

    def __build_dice_test(self, title: str):
        Label(self.__phase_frame, text=title, font=("Arial", 20)).pack()

        dice = Label(self.__phase_frame, text='🎲', font=("Arial", 200))
        dice.bind('<Button-1>', self.__roll_dice)
        dice.pack()

        Label(self.__phase_frame, text='Precisa tirar maior que 10 para Vitória.', font=("Arial", 20)).pack()

    def __build_revolt_option(self):
        Label(self.__phase_frame, text='Chance de Rebelião', font=("Arial", 20)).pack()

        sword = Label(self.__phase_frame, text='⚔  45% de sucesso', cursor='hand2', font=("Arial", 30))
        sleep = Label(self.__phase_frame, text='⏳ +15% de sucesso', cursor='exchange', font=("Arial", 30))

        sword.bind('<Button-1>', self.__try_revolt)
        sleep.bind('<Button-1>', self.__try_sleep)

        sword.pack()
        sleep.pack()

        Label(self.__phase_frame, text='Precisa tirar maior que 9 para Vitória.', font=("Arial", 20)).pack()

    def __build_card_game(self):
        joker_position = (0, 0)

        def is_joker():
            return i == joker_position[0] and j == joker_position[1]

        for i in range(5):
            for j in range(5):
                label = Label(self.__phase_frame, text='🂠', font=("Arial", 80), name=f'{i}-{j}')
                label.grid(row=i, column=j)

                if is_joker():
                    label.bind('<Button-1>', self.__turn_joker)
                else:
                    label.bind('<Button-1>', self.__turn_card)

    def __turn_card(self, event):
        card = CARDS[randint(0, len(CARDS) - 1)]

        position = event.widget._name.split('-')
        label = Label(self.__phase_frame, text=card, font=("Arial", 80))
        label.grid(row=position[0], column=position[1])

    def __turn_joker(self, event):
        [row, column] = event.widget._name.split('-')
        label = Label(self.__phase_frame, text='🃏', font=("Arial", 60))
        label.grid(row=row, column=column)
        showinfo('Vitória', 'Ataque bem sucedido!')
        self.__go_to_table()

    def __try_revolt(self, event):
        self.__reset_phase_frame()

        if self.__phase == STATES[2]:
            self.__phase = STATES[3]
            self.__build_card_game()
            showinfo('Resultado 🎲 = 8', 'O teste resultou em 🎲8.\nVocê falhou em se rebelar.\nAgora seu suserano está de olho em você.\n\n-15% de chance de Rebelião!')

    def __try_sleep(self, event):
        self.__reset_phase_frame()

        if self.__phase == STATES[2]:
            self.__phase = STATES[3]
            self.__build_card_game()
            showinfo('Decidiu esperar', 'Você decidiu esperar, ganhando confiança do seu suserano.\nAumentou as chances de revolta com sucesso em +15%.')

    def __roll_dice(self, event):
        self.__reset_phase_frame()

        if self.__phase == STATES[0]:
            self.__phase = STATES[1]
            self.__build_army_betrayal()
            showinfo('Resultado 🎲 = 4', 'O teste resultou em 🎲4.\nSeu exército não acredita que você fez a escolha certa ao declarar este ataque!')
        elif self.__phase == STATES[1]:
            self.__phase = STATES[2]
            self.__build_revolt_option()
            showinfo('Resultado 🎲 = 3', 'O teste resultou em 🎲3.\nVocê não conseguiu convencer o exército neutro a se juntar a você nessa batalha!')

    def __reset_phase_frame(self):
        self.__phase_frame.destroy()
        self.__phase_frame = Frame(self._frame, pady=10, padx=10)
        self.__phase_frame.grid(row=0, column=1, padx=10, rowspan=2)

    def __go_to_table(self):
        self.select_page('TABLE')
        self._reset_board()

    def _reset_board(self):
        self.__phase = STATES[0]
