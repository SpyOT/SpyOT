from tkinter import Tk, ttk, Frame, Button, Label, NORMAL, PhotoImage
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
        # self.win.resizable(False, False)
        # self.win.geometry(preset.default_geometry)
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
        self.body_widgets = {}
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

        self.body.columnconfigure(0, weight=1)
        self.body.rowconfigure(0, weight=1)
        self.body.rowconfigure(1, weight=1)
        self.body.rowconfigure(2, weight=1)
        self.body.rowconfigure(3, weight=1)

    def handle_btn_press(self, option):
        match option:
            case "profile":
                print("clicked on profile")
            case "settings":
                pass
            case "scan":
                pass
            case "collect":
                pass
            case "upload":
                pass
            case "exit":
                pass

    def set_widgets(self):
        # Header widgets
        profile_icon = PhotoImage(file=preset.profile_path)
        self.header_widgets["profile"] = Button(
            self.header,
            image=profile_icon,
            command=lambda: self.handle_btn_press("profile")
        )
        self.header_widgets["profile"].image = profile_icon

        title_icon = PhotoImage(file=preset.title_path)
        self.header_widgets["title"] = Label(
            self.header,
            image=title_icon,
            activebackground="#202020")
        self.header_widgets["title"].image = title_icon

        settings_icon = PhotoImage(file=preset.setting_path)
        self.header_widgets["settings"] = Button(
            self.header,
            image=settings_icon
        )
        self.header_widgets["settings"].image = settings_icon

        # Body widgets
        self.body_widgets["scan"] = Button(
            self.body,
            text="Scan Network",
            command=lambda: self.handle_btn_press("scan")
        )
        self.body_widgets["collect"] = Button(
            self.body,
            text="Collect Data",
            command=lambda: self.handle_btn_press("collect")
        )
        self.body_widgets["upload"] = Button(
            self.body,
            text="Upload Data",
            command=lambda: self.handle_btn_press("upload")
        )
        self.body_widgets["exit"] = Button(
            self.body,
            text="Exit Program",
            command=lambda: self.handle_btn_press("exit")
        )

    def display_win(self):
        self.container.grid(column=0, row=0, sticky='nesw')
        self.header.grid(column=0, row=0, sticky='nesw', padx=5, pady=5)
        self.body.grid(column=0, row=1, sticky='nesw', padx=5, pady=5)

        for i, option in enumerate(self.header_widgets):
            self.header_widgets[option].grid(
                column=i,
                row=0,
                padx=15, pady=15)
        # self.header_widgets["profile"].grid(column=0, row=0)
        # self.header_widgets["title"].grid(column=1, row=0)
        # self.header_widgets["settings"].grid(column=2, row=0)

        for i, option in enumerate(self.body_widgets):
            self.body_widgets[option].grid(
                column=0,
                row=i,
                padx=15, pady=15)
        # self.body_widgets["scan"].grid(column=0, row=0, padx=15, pady=15)
        # self.body_widgets["collect"].grid(column=0, row=1)
        # self.body_widgets["upload"].grid(column=0, row=2)
        # self.body_widgets["exit"].grid(column=0, row=3)
