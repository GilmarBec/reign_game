from tkinter import Frame, Tk
from tkinter.messagebox import showinfo
from src.common.decorators import setter
from src.page_router import PageRouter


class AbstractPage:
    _frame: Frame = None
    _window: Tk = None
    _page_router: PageRouter = None

    def __init__(self, window: Tk):
        self._window = window

    @property
    def page_name(self) -> str:
        return ''

    @setter
    def page_router(self, page_router: PageRouter) -> None:
        if self._page_router is not None:
            raise ValueError('Trying to replace page router already set.')

        self._page_router = page_router

    def build(self, data: any = None) -> None:
        raise NotImplementedError(f'Build function not implemented in class "{self.__class__}".')

    def destroy(self) -> None:
        if self._frame is None:
            raise SystemError(f"Frame doesn't exists to be destroyed")

        self._frame.destroy()

    def _build_frame(self) -> None:
        if self._frame is not None:
            self._frame.destroy()

        self._frame = Frame(self._window, background='white', pady=10, padx=10)

    def _select_page(self, page: str, data: any = None) -> None:
        self._page_router.select(page, data)

    def _go_to_menu(self) -> None:
        self._reset_board()
        self._select_page('MENU')

    def _reset_board(self) -> None:
        pass

    def _notify_message(self, message, title: str = 'Mensagem') -> None:
        showinfo(title, message)
