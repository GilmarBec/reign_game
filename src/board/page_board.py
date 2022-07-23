from random import randint
from tkinter import Button, Frame, Label, Event
from tkinter.messagebox import showinfo
from .board import Board
from .board_constants import STATES, CARDS
from src.common.pages import AbstractPage
from .board_side_builder import BoardSideBuilder


class PageBoard(AbstractPage):
    __state: int
    __action_frame: Frame
    __board: Board

    @property
    def page_name(self) -> str:
        return 'BOARD'

    def build(self, data: Board or None = None) -> None:
        if data is not None:
            self.__board = data

        self._build_frame()

        side_builder = BoardSideBuilder(parent_frame=self._frame, action_selector=self.__board.current_action_selector)
        side_builder.build(reign=self.__board.attacker, column=0)
        side_builder.build(reign=self.__board.defender, column=2)

        self.__action_frame = Frame(self._frame, pady=10, padx=10)
        self.__action_frame.grid(row=0, column=1, padx=10, rowspan=2)

        self.__update_phase_frame()

        Button(self._frame, text='🔙', command=self._go_to_menu, font=("Arial", 25))\
            .grid(row=0, column=3, padx=10, pady=10, sticky='ne')

        self._frame.pack(padx=50, pady=50)

    def __build_army_faith(self) -> None:
        loose_chance = (self.__board.difficulty * 2) + len(self.__board.attacker.vassals)
        self.__build_dice_test(
            title='Teste de Exército Nativo',
            subtitle=f'Precisa tirar mais que {loose_chance} para Vitória.',
        )

    def __build_army_betrayal(self) -> None:
        self.__build_dice_test(
            title='Teste de Conquista de Exército Inimigo',
            subtitle='Precisa tirar mais que 14 para Vitória.',
        )

    def __build_dice_test(self, title: str, subtitle: str) -> None:
        Label(self.__action_frame, text=title, font=("Arial", 20)).pack()

        dice = Label(self.__action_frame, text='🎲', font=("Arial", 200))
        dice.bind('<Button-1>', self.__roll_dice)
        dice.pack()

        Label(
            self.__action_frame,
            text=subtitle,
            font=("Arial", 20),
        ).pack()

    def __build_revolt_options(self) -> None:
        Label(self.__action_frame, text='Chance de Rebelião', font=("Arial", 20)).pack()

        revolt_chance = self.__board.current_action_selector.revolt_chance

        omit_message = f'⏳ +3 de chance de rebelião'
        if revolt_chance >= 15:
            omit_message = f'⏳ -{revolt_chance - 9} chance de rebelião'

        sword = Label(self.__action_frame, text=f'⚔  {revolt_chance} de sucesso', cursor='hand2', font=("Arial", 30))
        omit = Label(self.__action_frame, text=omit_message, cursor='exchange', font=("Arial", 30))

        sword.bind('<Button-1>', self.__revolt)
        omit.bind('<Button-1>', self.__omit)

        sword.pack()
        omit.pack()

        Label(
            self.__action_frame,
            text=f'Precisa tirar {20-revolt_chance} ou + para Vitória.',
            font=("Arial", 20),
        ).pack()

    def __build_card_game(self) -> None:
        cards = self.__board.cards

        for i in range(len(cards)):
            for j in range(len(cards[i])):
                label = Label(self.__action_frame, text='🂠', font=("Arial", 80))
                label.grid(row=i, column=j)

                label.bind('<Button-1>', (
                    lambda event, row=i, column=j: self.__turn_card(row, column)
                ))

    def __turn_card(self, row, column) -> None:
        old_action_selector_id = self.__board.current_action_selector.id
        is_joker = self.__board.select_card(row, column)

        if is_joker:
            label = Label(self.__action_frame, text='🃏', font=("Arial", 60))
            label.grid(row=row, column=column)
            showinfo('Vitória', 'Ataque bem sucedido!')
            self.__go_to_table()
            return

        card = CARDS[randint(0, len(CARDS) - 1)]

        label = Label(self.__action_frame, text=card, font=("Arial", 80))
        label.grid(row=row, column=column)

        if self.__board.state == STATES.ENDED:
            message = f'Jogador Defensor [{self.__board.defender.symbol}] Venceu!'

            if is_joker:
                message = f'Jogador Atacante [{self.__board.attacker.symbol}] Venceu!'

            showinfo('Fim da Batalha', message)
            self.__update_phase_frame()
            return

        action_selector = self.__board.current_action_selector
        if old_action_selector_id != action_selector.id:
            showinfo('Troca de jogador', f'Jogador que escolhe cartas agora é [{action_selector.symbol}]')

    def __revolt(self, event) -> None:
        [win, revolt_chance] = self.__board.revolt()

        message = 'Você decidiu se rebelar, mas seu suserano era forte de mais.\n' \
                  'Você perdeu essa revolta e seu exército pessoal sofreu baixas.\n'\
                  f'Sua chance de revolta agora é {revolt_chance}.'

        if win:
            message = 'Você decidiu se rebelar, o suserano perdeu o controle sobre você.\n' \
                      'Você agora é um reino livre novamente!'

        showinfo('Decidiu esperar', message)

        self.build()

    # not_revolt
    def __omit(self, event) -> None:
        [win, revolt_chance] = self.__board.not_revolt()

        message = 'Você decidiu esperar e esperou demais!\n' \
                  'Rumores de que você não está apto para ser rei se espalham.\n'

        if win:
            message = 'Você decidiu esperar enquanto ganha a confiança do seu suserano.\n'

        showinfo('Decidiu esperar', message + f'Sua chance de revolta agora é {revolt_chance}.')

        self.build()

    def __roll_dice(self, event: Event) -> None:
        if self.__state == STATES.ARMY_FAITH:
            [win, die_result] = self.__board.army_faith()

            message = 'Seu exército acredita que você não fez a escolha certa ao declarar este ataque!'
            if win:
                message = 'Seu exército estará com você nessa batalha!'

            self._notify_message(f'Resultado 🎲 = {die_result}\n\n{message}')
        elif self.__state == STATES.ARMY_BETRAYAL:
            [win, die_result] = self.__board.army_betrayal()

            message = 'Você não conseguiu convencer o exército neutro a se juntar a você nessa batalha!'
            if win:
                message = 'O exército neutro adentrou a sua causa temporariamente!'

            self._notify_message(f'Resultado 🎲 = {die_result}\n\n{message}')

        self.build()

    def __update_phase_frame(self) -> None:
        self.__state = self.__board.state

        self.__action_frame.destroy()
        self.__action_frame = Frame(self._frame, pady=10, padx=10)
        self.__action_frame.grid(row=0, column=1, padx=10, rowspan=2)

        if self.__state == STATES.ARMY_FAITH:
            self.__build_army_faith()

        elif self.__state == STATES.ARMY_BETRAYAL:
            self.__build_army_betrayal()

        elif self.__state == STATES.REVOLT:
            self.__build_revolt_options()

        elif self.__state == STATES.BATTLE:
            self.__build_card_game()

        elif self.__state == STATES.ENDED:
            self.__go_to_table()

    def __go_to_table(self) -> None:
        self._select_page('TABLE')
        self._reset_board()

    def _reset_board(self) -> None:
        self.__state = STATES.ARMY_FAITH
