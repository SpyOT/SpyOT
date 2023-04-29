from tkinter import Tk, ttk, PhotoImage

from gui import constants as preset
# from .views import MainView
from .views.frames import CustomContainer, CustomHeader

WIN_BG = '#0c131e'
FRAME_BG = '#3b3b3b'


class App(Tk):
    def __init__(self, systems, title, env):
        super().__init__()
        self.version = title
        self.title(title)
        self.APP_ENV = env

        self.configure_app()
        MainView(self, systems)

    def configure_app(self):
        logo = PhotoImage(file=preset.logo_img)
        self.iconphoto(False, logo)
        self.configure(bg=WIN_BG)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


class MainView:
    def __init__(self, base, systems):
        self.base = base
        self.systems = systems
        self.ENV = self.base.APP_ENV
        self.is_prod = self.ENV == 'prod'
        self.FRAME_BG = WIN_BG if self.is_prod else FRAME_BG
        self.WIDGET_BG = self.FRAME_BG
        self.style = ttk.Style()
        self.configure_styles()

        self.main_container = CustomContainer(self.base, style='CustomContainer.TFrame')
        self.main_container.configure_win(col_config={'col 0': 'weight 2',
                                                      'col 1': 'weight 1'},
                                          row_config={'row 0': 'weight 1',
                                                      'row 1': 'weight 5',
                                                      'row 2': 'weight 3'})

        self.header = CustomHeader(self.main_container, style='CustomFrame.TFrame')
        # self.body = CustomBody(self.main_container)
        # self.footer = CustomFooter(self.main_container)
        # self.output = CustomOutput(self.main_container)

        self.display_win()

    def configure_styles(self):
        self.style.configure(
            'CustomContainer.TFrame',
            background=WIN_BG,
            bd=0,
            highlightthickness=0,
            relief='ridge'
        )

        # TFrame style inherits from Container style
        self.style.configure(
            'CustomFrame.TFrame',
            background=self.FRAME_BG
        )

        # TLabel inherits from TFrame style
        self.style.configure(
            'CustomWidget.TLabel',
            background=self.WIDGET_BG,
            relief='solid'
        )

        self.style.configure(
            'CustomWidget.TButton',
            activebackground=self.WIDGET_BG,
            background=self.WIDGET_BG,
            relief='solid',
        )

    def display_win(self):
        self.main_container.grid(column=0, row=0, sticky='n e s w')
        self.header.display_frame(column=0, row=0, sticky='n e s w', padx=5, pady=5)
