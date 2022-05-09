from tkinter import Frame
from tkinter.ttk import Combobox

from src.widgets.abstract_widgets import AbstractWidgets


class ComboboxWidget(AbstractWidgets):
    def build_instance(self, frame: Frame, values: [str or int]):
        return Combobox(frame, values=values)
