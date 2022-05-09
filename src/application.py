from tkinter import Tk

from src.page_router import PageRouter
from src.pages.page_board import PageBoard
from src.pages.page_menu import PageMenu
from src.pages.page_table import PageTable


class Application:
    window: Tk = Tk()
    router: PageRouter

    def __init__(self):
        # self.window.attributes("-fullscreen", True)
        self.window.title('Jogo do reino')
        # self.window.attributes('-topmost', True)
        # self.window.state('zoomed')

        self.router = PageRouter({
            'BOARD': PageBoard(self.window),
            'MENU': PageMenu(self.window),
            'TABLE': PageTable(self.window),
        })

        self.window.mainloop()
