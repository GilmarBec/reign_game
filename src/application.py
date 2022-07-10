from tkinter import Tk

from src.page_router import PageRouter
from src.board.page_board import PageBoard
from src.menu.page_menu import PageMenu
from src.table.page_table import PageTable


class Application:
    __window: Tk = Tk()
    __router: PageRouter

    def __init__(self):
        self.__window.title('Jogo do reino')
        # self.window.attributes("-fullscreen", True)
        # self.window.attributes('-topmost', True)
        # self.window.state('zoomed')

        self.__router = PageRouter({
            'BOARD': PageBoard(self.__window),
            'MENU': PageMenu(self.__window),
            'TABLE': PageTable(self.__window),
        })

        self.__window.mainloop()
