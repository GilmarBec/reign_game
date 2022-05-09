from tkinter import Frame, Tk

from src.decorators.setter_property import setter


class AbstractPage:
    _frame: Frame
    _window: Tk
    _page_router: any = None

    def __init__(self, window: Tk):
        self._window = window

    def build(self, data: any = None):
        raise NotImplementedError(f'Build function not implemented in class "{self.__class__}".')

    def destroy(self):
        if self._frame is None:
            raise SystemError(f"Frame doesn't exists to be destroyed")

        self._frame.destroy()

    def build_frame(self):
        self._frame = Frame(self._window, background='white', pady=10, padx=10)

    @property
    def page_name(self):
        return ''

    @setter
    def page_router(self, page_router: any):
        if self._page_router is not None:
            raise ValueError('Trying to replace page router already set.')

        self._page_router = page_router

    def select_page(self, page: str, data: any = None):
        self._page_router.select(page, data)

    def _go_to_menu(self):
        self._reset_board()
        self.select_page('MENU')

    def _reset_board(self):
        pass
