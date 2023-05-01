from tkinter import ttk, messagebox
from .OutputView import OutputView
from .MainView import MainView
from threading import Thread
from gui import constants as const


class App:
    def __init__(self, window, systems, title, env):
        self.window = window
        self.systems = systems
        self.version = title
        self.APP_ENV = env
        self.is_prod = self.APP_ENV == 'prod'

        self.theme = "LIGHT"
        self.style = ttk.Style()
        self.configure_styles()

        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)
        self.window.rowconfigure(0, weight=1)

        self.main_container = MainView(self.window,
                                       self.systems,
                                       height=const.FRAME_MIN_HEIGHT,
                                       width=const.FRAME_MIN_WIDTH,
                                       style='ttk.Frame.Home.TFrame')

        self.output_container = OutputView(self.window,
                                           self.systems,
                                           height=const.FRAME_MIN_HEIGHT,
                                           width=const.FRAME_MIN_WIDTH,
                                           style='ttk.Frame.Output.TFrame')

        self.set_widgets()
        self.main_container.display_frame(column=0, row=0, sticky='n e s w')
        self.output_container.display_frame(column=1, row=0, sticky='n e s w')
        self.thread = None

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
            case "run_scan":
                print("New Scan button pressed")
                self.output_container.update_view("loading")
                self.thread = Thread(target=lambda: self.run_thread("scan")).start()
            case "output_scan":
                print("Scan button pressed")
                # set output widgets for scan
                if self.systems.metadata_available():
                    self.output_container.update_view("output_scan")
                else:
                    self.handle_btn_press("run_scan")
            case "collect":
                print("Collect button pressed")
                # set output widgets for collect
                self.output_container.update_view("loading")
                self.thread = Thread(target=lambda: self.run_thread("collect")).start()
            case "upload":
                print("Upload button pressed")
                # set output widgets for upload
                self.output_container.update_view("upload")
            case "toggle_theme":
                print("Toggle theme button pressed")
                self.toggle_theme()
            case "blacklist":
                print("Blacklist button pressed")
                self.output_container.update_view("blacklist")
            case "whitelist":
                print("Whitelist button pressed")
                self.output_container.update_view("whitelist")
            case "view_report":
                self.systems.view_recent_report()
            case "save_report":
                pass
            case _:
                print("Unknown button pressed")

    def configure_styles(self):
        self.style.theme_use('vista')
        # Style names are in the format 'widgetclass.stylename.widgettype'
        self.style.configure(
            'TFrame',
            bd=0,
            highlightthickness=0,
            relief='ridge'
        )

        self.style.configure(
            'ttk.Frame.Home.TFrame',
            background=const.FRAME_LIGHT_PRIMARY
        )

        self.style.configure(
            'ttk.Frame.Output.TFrame',
            background=const.FRAME_LIGHT_SECONDARY
        )

        self.style.configure(
            'ttk.Label.CustomLabel.TLabel',
            background=const.LABEL_LIGHT_PRIMARY,
            foreground=const.LABEL_LIGHT_SECONDARY,
            relief='none'
        )

        self.style.configure(
            'ttk.Button.CustomButton.TButton',
            background=const.BUTTON_LIGHT_PRIMARY,
            foreground=const.BUTTON_LIGHT_SECONDARY,
            relief='raised',
        )

        self.style.configure(
            'ttk.Button.ImgCustomButton.TButton',
            background=const.IMG_BUTTON_LIGHT_PRIMARY,
            foreground=const.IMG_BUTTON_LIGHT_SECONDARY,
        )

    def toggle_theme(self):
        is_light = self.theme == "LIGHT"
        self.theme = "DARK" if is_light else "LIGHT"

        win_primary = const.FRAME_DARK_PRIMARY if is_light else const.FRAME_LIGHT_PRIMARY
        win_secondary = const.FRAME_DARK_SECONDARY if is_light else const.FRAME_LIGHT_SECONDARY
        label_primary = const.LABEL_DARK_PRIMARY if is_light else const.LABEL_LIGHT_PRIMARY
        label_secondary = const.LABEL_DARK_SECONDARY if is_light else const.LABEL_LIGHT_SECONDARY
        button_primary = const.BUTTON_DARK_PRIMARY if is_light else const.BUTTON_LIGHT_PRIMARY
        button_secondary = const.BUTTON_DARK_SECONDARY if is_light else const.BUTTON_LIGHT_SECONDARY
        img_button_primary = const.IMG_BUTTON_DARK_PRIMARY if is_light else const.IMG_BUTTON_LIGHT_PRIMARY
        img_button_secondary = const.IMG_BUTTON_DARK_SECONDARY if is_light else const.IMG_BUTTON_LIGHT_SECONDARY

        self.style.configure("ttk.Frame.Home.TFrame", background=win_primary)
        self.style.configure("ttk.Frame.Output.TFrame", background=win_secondary)
        self.style.configure("ttk.Label.CustomLabel.TLabel",
                             background=label_primary,
                             foreground=label_secondary)
        self.style.configure(const.BUTTON_STYLE,
                             background=button_primary,
                             foreground=button_secondary)
        self.style.configure(const.IMG_BUTTON_STYLE,
                             background=img_button_primary,
                             foreground=img_button_secondary)
        self.output_container.toggle_theme(self.theme)

    def run_thread(self, command):
        """
        Runs a thread for the given command
        Format:
            Conditional for checking if self.systems.command()
            self.output_container.get_widget("loading_bar").stop()
            If successful, display success message and update output view to command
            If unsuccessful, display error message and update output view to none
        """
        match command:
            case "scan":
                success = self.systems.scan()
                self.output_container.get_widget("loading_bar").stop()
                if success:
                    messagebox.showinfo("Scan Complete", "Scan complete.")
                    self.output_container.update_view("output_scan")
                else:
                    messagebox.showerror("Error", "Scan incomplete. Please try again.")
                    self.output_container.update_view("none")
            case "collect":
                success = self.systems.collect()
                self.output_container.get_widget("loading_bar").stop()
                if success:
                    messagebox.showinfo("Collect Complete", "Collect complete.")
                    self.output_container.update_view("output_collect")
                else:
                    messagebox.showerror("Error", "Collect incomplete. Please try again.")
                    self.output_container.update_view("none")
            case "upload":
                success = self.systems.upload()
                self.output_container.get_widget("loading_bar").stop()
                if success:
                    messagebox.showinfo("Upload Complete", "Upload complete.")
                    self.output_container.update_view("output_upload")
                else:
                    messagebox.showerror("Error", "Upload incomplete. Please try again.")
                    self.output_container.update_view("none")
            case _:
                print("Unknown thread command")
                self.output_container.update_view("none")
