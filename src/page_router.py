from src.common.pages import AbstractPage


class PageRouter:
    __pages: dict
    __current_page: AbstractPage

    def __init__(self, pages: dict):
        self.__pages = pages

        for page in pages.values():
            page.page_router = self

        self.__initial_page()

    def select(self, key: str, data):
        if self.__current_page is None:
            raise SystemError(f'Current page not defined', {
                'key': key,
            })

        if self.__current_page.page_name == key:
            raise SystemError(f'Already in page "{key}"', {
                'current_page': self.__current_page,
                'key': key,
            })

        self.__current_page.destroy()

        print(f'Going to Page {key}')

        self.__current_page = self.__pages[key]
        self.__current_page.build(data)

    def __initial_page(self):
        self.__current_page = self.__pages['MENU']
        self.__current_page.build()
