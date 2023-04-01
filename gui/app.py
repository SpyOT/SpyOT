from tkinter import Tk, ttk, PhotoImage
from SpyOT.gui import constants as preset
from .views import MainMenu


class App(Tk):
    def __init__(self, network, title, env):
        super().__init__()
        self.version = title
        self.title(title)
        self.APP_ENV = env
        self.style = ttk.Style()
        self.style.theme_use('vista')

        self.configure_win()
        self.main_menu = MainMenu(network, self)

    def configure_win(self):
        logo = PhotoImage(file=preset.logo_img)
        self.iconphoto(False, logo)
        self.configure(bg="#0c131e")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
