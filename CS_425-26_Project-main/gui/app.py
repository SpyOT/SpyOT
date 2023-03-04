from tkinter import ttk, Frame, Canvas, Label, Button, PhotoImage
from PIL import ImageTk
import constants as preset


class App:
    def __init__(self, window):
        self.win = window
        self.style = ttk.Style()
        self.style.theme_use('vista')

        self.configure_win()
        self.main_menu = MainMenu(self.win)

    def configure_win(self):
        self.win.resizable(False, False)
        self.win.geometry(preset.default_geometry)
        self.win.configure(bg="#202020")
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

        self.header_widgets = {}
        self.buttons = {
            "scan": None,
            "collect": None,
            "transfer": None,
            "exit": None
        }
        self.set_widgets()

        self.display_win()

    def set_win(self):
        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(0, weight=1)
        self.container.rowconfigure(1, weight=5)

        self.header.columnconfigure(0, weight=1)
        self.header.columnconfigure(1, weight=8)
        self.header.columnconfigure(2, weight=1)
        self.header.rowconfigure(0, weight=1)

    def handle_btn_press(self, option):
        match option:
            case "profile":
                print("clicked on profile")

    def set_widgets(self):
        # Header widgets
        self.header_widgets["canvas"] = Canvas(
            self.header,
            bg="yellow",
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas = self.header_widgets["canvas"]
        profile_icon = ImageTk.PhotoImage(file=preset.profile_path)
        self.header_widgets["profile"] = Button(
            self.header,
            image=profile_icon,
            borderwidth=0,
            highlightthickness=0,
            activebackground="#202020",
            command=lambda: self.handle_btn_press("profile"),
            relief="flat",
        )
        self.header_widgets["profile"].image = profile_icon

        title_icon = PhotoImage(file=preset.title_path)
        self.header_widgets["title"] = Label(
            self.header,
            image=title_icon,
            activebackground="#202020")
        self.header_widgets["title"].image = title_icon

    def display_win(self):
        self.container.grid(column=0, row=0, sticky='nesw')
        self.header.grid(column=0, row=0, sticky='nesw', padx=5, pady=5)
        self.body.grid(column=0, row=1, sticky='nesw', padx=5, pady=5)

        # self.header_widgets["canvas"].place(x=0, y=0)
        # btn = self.header_widgets["profile"]
        # self.header_widgets["canvas"].create_window(0, 0, window=btn)
        self.header_widgets["profile"].grid(column=0, row=0)
        self.header_widgets["title"].grid(column=1, row=0)
