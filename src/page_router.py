from src.pages.abstract_page import AbstractPage


class PageRouter:
    pages: dict
    current_page: AbstractPage

    def __init__(self, pages: dict):
        self.pages = pages

        for page in pages.values():
            page.page_router = self

        self.initial_page()

    def initial_page(self):
        self.current_page = self.pages['MENU']
        self.current_page.build()

    def select(self, key: str, data):
        if self.current_page is None:
            raise SystemError(f'Current page not defined', {
                'key': key,
            })

        if self.current_page.page_name == key:
            raise SystemError(f'Already in page "{key}"', {
                'current_page': self.current_page,
                'key': key,
            })

        self.current_page.destroy()

        print(f'Going to Page {key}')

        self.current_page = self.pages[key]
        self.current_page.build(data)
