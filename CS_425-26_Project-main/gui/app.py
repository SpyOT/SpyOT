from tkinter import ttk, Frame, Label, Text, Button
import constants as preset


class App:
    def __init__(self, window):
        self.win = window
        self.style = ttk.Style()
        self.style.theme_use('vista')

        self.configure_win()
        self.set_main_menu = MainMenu(self.win)

    def configure_win(self):
        self.win.resizable(False, False)
        self.win.geometry(preset.default_geometry)
        self.win.columnconfigure(0, weight=1)
        self.win.rowconfigure(0, weight=1)

class MainMenu:
    def __init__(self, window):
        self.win = window
        self.container = Frame(
            self.win,
            bg="#202020",
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.header = Frame(
            self.container,
            bg="#3b3b3b",
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.body = Frame(
            self.container,
            bg="#3b3b3b",
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.set_win()

        self.labels = {}
        self.buttons = {
            "scan": None,
            "collect": None,
            "transfer": None,
            "exit": None
        }
        self.set_widgets()

    def set_win(self):
        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(0, weight=1)
        self.container.rowconfigure(1, weight=5)

        self.container.grid(column=0, row=0, sticky='nesw')
        self.header.grid(column=0, row=0, sticky='nesw', padx=5, pady=5)
        self.body.grid(column=0, row=1, sticky='nesw', padx=5, pady=5)

    def set_widgets(self):
        pass

    def set_buttons(self):
        pass