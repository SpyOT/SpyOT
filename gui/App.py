from tkinter import ttk, messagebox, PhotoImage, filedialog
from .OutputView import OutputView
from .MainView import MainView
from threading import Thread, Event
from gui import constants as const


class App:
    def __init__(self, window, systems, title):
        self.window = window
        self.systems = systems
        self.version = title

        self.theme = "LIGHT"
        self.style = ttk.Style()
        self.configure_styles()

        self.window.columnconfigure(0, weight=2)
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

        self.set_win()

        self.stop_thread = Event()
        self.thread = None

    def set_win(self):
        self.main_container.set_widgets(self)
        self.output_container.set_widgets(self)
        self.main_container.display_frame(column=0, row=0, sticky='n e s w')
        self.output_container.display_frame(column=1, row=0, sticky='n e s w')

    def handle_btn_press(self, command):
        match command:
            # MainView commands
            case "profile":
                print("Profile button pressed")
                if self.systems.is_logged_in():
                    print("logged in, show profile screen")
                    self.output_container.update_view("profile")
                else:
                    print("not logged in, show login screen")
                    self.output_container.update_view("login")
            case "settings":
                print("Settings button pressed")
                # set output widgets for settings
                self.output_container.update_view("settings")
            case "about":
                print("Info button pressed")
                # set output widgets for info
                self.output_container.update_view("about")
            # OutputView commands
            case "login":
                print("Login button pressed")
                email, password = self.output_container.get_login_info()
                command_success = self.systems.signin_user(email, password)
                if command_success:
                    messagebox.showinfo("Login Successful", "Welcome back!")
                    self.output_container.update_view("none")
                else:
                    messagebox.showerror("Login Failed", "Invalid email or password")
                    self.output_container.update_view("login")
            case "logout":
                print("Logout button pressed")
                command_success = self.systems.signout_user()
                if command_success:
                    messagebox.showinfo("Logout Successful", "Goodbye!")
                    self.output_container.update_view("login")
                else:
                    messagebox.showerror("Logout Failed", "Something went wrong, closing session.")
                    self.output_container.update_view("login")
            case "run_scan":
                print("New Scan button pressed")
                self.output_container.update_view("loading")
                self.setup_thread("scan")
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
                self.setup_thread("collect")
            case "upload":
                print("Upload button pressed")
                # set output widgets for upload
                if self.systems.is_logged_in():
                    self.output_container.update_view("loading")
                    self.setup_thread("upload")
                else:
                    self.output_container.update_view("login")
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
                save_path = filedialog.asksaveasfilename(
                    title="Save Report",
                    initialdir=self.systems.get_reports_path,
                    filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")),
                    defaultextension="*.txt*")
                self.systems.save_report(save_path)
            case "cancel":
                self.output_container.get_widget("loading_bar").stop()
                self.output_container.update_view("none")
                self.window.destroy()
            case "exit":
                self.window.destroy()
            case _:
                print("Unknown button pressed")

    def configure_styles(self):
        self.style.theme_use('clam')
        # Custom Style names are in the format 'widgetclass.stylename.widgettype'
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
            relief='none',
            font=('Helvetica', 8, 'bold'),
        )

        self.style.configure(
            'ttk.Button.CustomButton.TButton',
            background=const.BUTTON_LIGHT_PRIMARY,
            foreground=const.BUTTON_LIGHT_SECONDARY,
            borderwidth=0,
            disabledforeground=const.BUTTON_LIGHT_PRIMARY,
            font=('Helvetica', 12, 'normal'),
        )
        self.style.map(
            'ttk.Button.CustomButton.TButton',
            background=[('active', const.BUTTON_LIGHT_SECONDARY),
                        ('disabled', const.BUTTON_LIGHT_PRIMARY)],
        )

        self.style.configure(
            'ttk.Button.ImgCustomButton.TButton',
            background=const.IMG_BUTTON_LIGHT_PRIMARY,
            foreground=const.IMG_BUTTON_LIGHT_SECONDARY,
            relief='none',
        )

        self.style.configure(
            'ttk.Button.MainButton.TButton',
            background=const.MAIN_BTTN_LIGHT_PRIMARY,
            relief='none',
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
        main_button_primary = const.MAIN_BTTN_DARK_PRIMARY if is_light else const.MAIN_BTTN_LIGHT_PRIMARY

        title_img_path = const.TITLE_PATH if is_light else const.TITLE_DARK_PATH
        loading_img_path = const.LOADING_ICON_PATH if is_light else const.LOADING_DARK_ICON_PATH
        email_label_path = const.EMAIL_LABEL if is_light else const.EMAIL_DARK_LABEL
        password_label_path = const.PASSWORD_LABEL if is_light else const.PASSWORD_DARK_LABEL
        login_prompt_path = const.LOGIN_PROMPT if is_light else const.LOGIN_DARK_PROMPT
        scan_label_path = const.SCAN_LABEL if is_light else const.SCAN_DARK_LABEL

        title_img = PhotoImage(file=title_img_path)
        loading_img = PhotoImage(file=loading_img_path)
        email_label = PhotoImage(file=email_label_path)
        password_label = PhotoImage(file=password_label_path)
        login_prompt = PhotoImage(file=login_prompt_path)
        scan_label = PhotoImage(file=scan_label_path)
        self.main_container.update_widget_value("title", "image", title_img)
        self.output_container.update_widget_value("loading_label", "image", loading_img)
        self.output_container.update_widget_value("email_label", "image", email_label)
        self.output_container.update_widget_value("password_label", "image", password_label)
        self.output_container.update_widget_value("login_prompt", "image", login_prompt)
        self.output_container.update_widget_value("host_label", "image", scan_label)
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
        self.style.configure(const.MAIN_BUTTON_STYLE,
                             background=main_button_primary)
        self.style.map(
            'ttk.Button.CustomButton.TButton',
            background=[('active', button_secondary),
                        ('disabled', button_primary)],
        )
        self.output_container.toggle_theme(self.theme)

    def setup_thread(self, command):
        self.stop_thread.clear()
        self.thread = Thread(target=lambda: self.run_thread(command))
        self.thread.daemon = True
        self.thread.start()

    def run_thread(self, command):
        """
        Runs a thread for the given command
        Format:
            Conditional for checking if self.systems.command() was successful
            Stopping loading bar animation self.output_container.get_widget("loading_bar").stop()
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
