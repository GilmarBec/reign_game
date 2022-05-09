from tkinter import Frame


class AbstractWidgets:
    __x: int
    __y: int

    def __init__(self, x: int = 0, y: int = 0):
        self.__x = x
        self.__y = y

    def build_instance(self, frame: Frame, params):
        pass
