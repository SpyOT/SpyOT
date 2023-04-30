from tkinter import ttk, PhotoImage
from .custom_widgets import CustomContainer, CustomButton, CustomLabel
from .OutputView import OutputView
from .MainView import MainView

# Constants
PROFILE_PATH = 'gui/assets/profile_icon.png'
TITLE_PATH = 'gui/assets/title_icon.png'
SETTINGS_PATH = 'gui/assets/settings_icon.png'


class App:
    WIN_BG = '#0c131e'  # Black
    FRAME_BG = '#3b3b3b'  # Dark Grey in prod
    WIDGET_BG = FRAME_BG  # '#3b3b3b' # Dark Grey in prod
    FRAME_MIN_WIDTH = 250
    FRAME_MIN_HEIGHT = 5
    TEXT_COLOR = 'white'

    def __init__(self, window, systems, title, env):
        self.window = window
        self.systems = systems
        self.version = title
        self.APP_ENV = env
        self.is_prod = self.APP_ENV == 'prod'

        self.style = ttk.Style()
        self.configure_styles()

        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)
        self.window.rowconfigure(0, weight=1)

        self.main_container = MainView(self.window,
                                       self.systems,
                                       height=App.FRAME_MIN_HEIGHT,
                                       width=App.FRAME_MIN_WIDTH,
                                       style='ttk.Frame.Home.TFrame')

        self.output_container = OutputView(self.window,
                                           self.systems,
                                           height=App.FRAME_MIN_HEIGHT,
                                           width=App.FRAME_MIN_WIDTH,
                                           style='ttk.Frame.Output.TFrame')

        self.set_widgets()
        self.display_win()

    def display_win(self):
        self.main_container.display_frame(column=0, row=0, sticky='n e s w')
        self.output_container.display_frame(column=1, row=0, sticky='n e s w')

    def set_widgets(self):
        self.main_container.set_widgets(self)
        self.output_container.set_widgets(self)

    def handle_btn_press(self, command):
        match command:
            # MainView commands
            case "profile":
                print("Profile button pressed")
                # set output containers view to profile
                self.output_container.update_view("profile")
            case "settings":
                print("Settings button pressed")
                # set output widgets for settings
                self.output_container.update_view("settings")
            case "info":
                print("Info button pressed")
                # set output widgets for info
                self.output_container.update_view("info")

            # OutputView commands
            case "login":
                print("Login button pressed")
                # call systems model for firebase login
            case "logout":
                print("Logout button pressed")
                # call systems model for firebase logout
            case "new_scan":
                print("New Scan button pressed")
                # set output widgets for new scan
                self.output_container.update_view("new_scan")
            case "scan":
                print("Scan button pressed")
                # set output widgets for scan
                self.output_container.update_view("scan")
            case "collect":
                print("Collect button pressed")
                # set output widgets for collect
                self.output_container.update_view("collect")
            case "upload":
                print("Upload button pressed")
                # set output widgets for upload
                self.output_container.update_view("upload")
            case _:
                print("Unknown button pressed")

    def configure_styles(self):
        self.style.theme_use('vista')
        # Style names are in the format 'widgetclass.stylename.widgettype'
        self.style.configure(
            'TFrame',
            bd=0,
            background=App.WIN_BG,
            highlightthickness=0,
            relief='ridge'
        )

        self.style.configure(
            'ttk.Frame.Home.TFrame',
            background=App.FRAME_BG,
        )

        self.style.configure(
            'ttk.Frame.Output.TFrame',
            background=App.WIN_BG
        )

        self.style.configure(
            'ttk.Label.CustomLabel.TLabel',
            foreground=App.TEXT_COLOR,
            background=App.WIDGET_BG,
            relief='none'
        )

        self.style.configure(
            'ttk.Button.CustomButton.TButton',
            background=App.WIDGET_BG,
            relief='raised',
        )
