from .frame import CustomContainer
from gui import widgets
from tkinter import PhotoImage
from os import getcwd
from os.path import join

# Constants
CWD = getcwd()
ASSETS_PATH = join(CWD, 'gui', 'assets')
PROFILE_PATH = join(ASSETS_PATH, 'profile_icon.png')
TITLE_PATH = join(ASSETS_PATH, 'title_icon.png')
SETTINGS_PATH = join(ASSETS_PATH, 'settings_icon.png')


class CustomHeader(CustomContainer):
    def __init__(self, frame, **kwargs):
        super().__init__(
            frame,
            **kwargs
        )
        self.configure_win()
        self.widgets = {}
        self.set_widgets()

    def configure_win(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=8)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)

    def set_widgets(self):
        """ Header widgets"""
        profile_icon = PhotoImage(file=PROFILE_PATH)
        self.set_widget("profile", widgets.CustomButton,
                        image=profile_icon,
                        style='CustomWidget.TButton',
                        command=lambda: self.handle_btn_press("profile"))
        title_icon = PhotoImage(file=TITLE_PATH)
        self.set_widget("title", widgets.CustomLabel,
                        image=title_icon,
                        style='CustomWidget.TLabel'
                        )

    #     self.get_widget("title").bind("<Button-1>", lambda event: self.handle_btn_press('set_admin'))
    #     self.get_widget("title").bind("<Button-3>", lambda event: self.handle_btn_press('set_guest'))
    #     settings_icon = PhotoImage(file=SETTINGS_PATH)
    #     self.set_widget("settings", widgets.CustomButton,
    #                            image=settings_icon,
    #                            bg=widget_bg,
    #                            command=lambda: self.handle_btn_press("settings"))

    def display_widgets(self):
        for i, name in enumerate(self.widgets):
            self.display_widget(
                name,
                column=i, row=0,
                padx=15, pady=15
            )

    def handle_btn_press(self, command):
        pass