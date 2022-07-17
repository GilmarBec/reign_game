from tkinter import Frame, Canvas
from tkinter.font import Font
from src.reign import Reign


class BoardSideBuilder:
    __frame: Frame
    __action_selector: Reign
    __canvas: Canvas

    def __init__(self, parent_frame: Frame, action_selector: Reign):
        self.__frame = parent_frame
        self.__action_selector = action_selector

    def build(self, reign, column: int = 0):
        frame = Frame(self.__frame, pady=10, padx=10)
        frame.grid(row=0, column=column, padx=10, rowspan=2)

        self.__canvas = Canvas(frame, height=600, width=250)

        self.__build_side(reign, is_attacker=column == 0)

        self.__canvas.pack()

    def __build_side(self, reign, is_attacker: bool):
        vassals = reign.vassals

        reign_width: int = 200
        reign_height: int = 200
        pad_left = 25
        pad_up = 25

        if not is_attacker:
            pad_up = 600 - 25 - reign_height

        self.__base_build_side(reign, pad_up, pad_left, reign_height, reign_width, 50, 0)

        if is_attacker:
            pad_up += 25 + reign_height
        else:
            pad_up -= 100

        for i in range(len(vassals)):
            line_end = self.__build_vassal(i, vassals[i], pad_up)

            if line_end:
                if is_attacker:
                    pad_up += (25 + reign_height)
                else:
                    pad_up -= (25 + reign_height)

    def __base_build_side(self, reign, pad_up, pad_left, reign_height, reign_width, font_size, border):
        self.__canvas.create_rectangle(
            pad_left, pad_up,
            reign_width + pad_left, reign_height + pad_up,
            fill=reign.color,
            width=border,
        )

        coordinates = (pad_left + reign_width / 2, pad_up + reign_height / 2)
        self.__canvas.create_text(
            coordinates, text=reign.symbol,
            font=Font(family="Arial", size=font_size), fill="light gray"
        )

    def __build_vassal(self, index, vassal, pad_up):
        action_selector = self.__action_selector

        reign_height = 75
        reign_width = 75

        line_end = index % 2 != 0 and index != 0

        pad_left = 25
        if line_end:
            pad_left += (reign_width + 50)

        font_size = 20
        border = 0
        if action_selector is not None and action_selector.id == vassal.id:
            font_size = 35
            border = 5

        self.__base_build_side(
            reign=vassal, pad_up=pad_up, pad_left=pad_left,
            reign_height=reign_height, reign_width=reign_width,
            font_size=font_size, border=border,
        )

        return line_end
