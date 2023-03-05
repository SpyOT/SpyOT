from tkinter import ttk, Frame, Button, Label, PhotoImage, messagebox
from PIL import ImageTk
import constants as preset


class App:
    def __init__(self, window):
        self.win = window
        self.style = ttk.Style()
        self.style.theme_use('vista')

        self.configure_win()
        self.main_menu = MainMenu(window.network, self.win)

    def configure_win(self):
        # self.win.resizable(False, False)
        # self.win.geometry(preset.default_geometry)
        self.win.configure(bg="#202020")
        self.win.columnconfigure(0, weight=1)
        self.win.rowconfigure(0, weight=1)


class MainMenu:
    def __init__(self, network, window):
        self.network = network
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
        self.footer = Frame(
            self.container,
            bg="#3b3b3b",
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.set_win()

        self.header_widgets = {}
        self.body_widgets = {}
        self.footer_widgets = {}
        self.alert_widgets = {}
        self.set_widgets()

        self.display_win()

    def set_win(self):
        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(0, weight=1)
        self.container.rowconfigure(1, weight=5)
        self.container.rowconfigure(2, weight=3)

        self.header.columnconfigure(0, weight=1)
        self.header.columnconfigure(1, weight=8)
        self.header.columnconfigure(2, weight=1)
        self.header.rowconfigure(0, weight=1)

        self.body.columnconfigure(0, weight=1)
        self.body.columnconfigure(1, weight=1)
        self.body.rowconfigure(0, weight=1)
        self.body.rowconfigure(1, weight=1)
        self.body.rowconfigure(2, weight=1)
        self.body.rowconfigure(3, weight=1)

        self.footer.columnconfigure(0, weight=1)
        self.footer.columnconfigure(1, weight=1)
        self.footer.rowconfigure(0, weight=1)

    def handle_btn_press(self, option):
        print("clicked on", option, "button")
        match option:
            case "profile":
                pass
            case "settings":
                pass
            case "scan":
                self.network.scan()
                messagebox.showinfo(self.win.version, "Scan Complete")
            case "collect":
                pass
            case "upload":
                if self.network.can_upload():
                    self.network.upload()
                    messagebox.showinfo(self.win.version, "Upload Complete")
                else:
                    messagebox.showerror(self.win.version, "Nothing to upload.\nTry scanning network first.")
            case "exit":
                print("Goodbye!")
                self.win.quit()
            case "info":
                pass

    def set_widgets(self):
        widget_bg = "#3b3b3b"
        win_bg = "#202020"
        # Header widgets
        profile_icon = PhotoImage(file=preset.profile_path)
        self.header_widgets["profile"] = Button(
            self.header,
            image=profile_icon,
            bg=widget_bg,
            activebackground=win_bg,
            bd=0,
            highlightthickness=0,
            relief="ridge",
            command=lambda: self.handle_btn_press("profile")
        )
        self.header_widgets["profile"].image = profile_icon

        title_icon = PhotoImage(file=preset.title_path)
        self.header_widgets["title"] = Label(
            self.header,
            image=title_icon,
            bg=widget_bg,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.header_widgets["title"].image = title_icon

        settings_icon = PhotoImage(file=preset.setting_path)
        self.header_widgets["settings"] = Button(
            self.header,
            image=settings_icon,
            bg=widget_bg,
            activebackground=win_bg,
            bd=0,
            highlightthickness=0,
            relief="ridge",
            command=lambda: self.handle_btn_press("settings")
        )
        self.header_widgets["settings"].image = settings_icon

        # Body widgets
        action_icons = {"scan": preset.scan_path,
                        "collect": preset.collect_path,
                        "upload": preset.upload_path}
        for action in action_icons:
            self.body_widgets[action] = {}
            curr_line = self.body_widgets[action]
            action_icon = PhotoImage(file=action_icons[action])
            curr_line["label"] = Label(
                self.body,
                image=action_icon,
                bg=widget_bg,
                bd=0,
                highlightthickness=0,
                relief="ridge"
            )
            curr_line["label"].image = action_icon

        self.body_widgets["scan"]["button"] = Button(
            self.body,
            text="Scan Network",
            bg=widget_bg,
            activebackground="white",
            bd=1,
            highlightthickness=0,
            relief="flat",
            foreground="#5EFF5E",
            command=lambda: self.handle_btn_press("scan")
        )
        self.body_widgets["collect"]["button"] = Button(
            self.body,
            text="Collect Data",
            bg=widget_bg,
            activebackground="white",
            bd=1,
            highlightthickness=0,
            relief="flat",
            foreground="#5EFF5E",
            command=lambda: self.handle_btn_press("collect")
        )
        self.body_widgets["upload"]["button"] = Button(
            self.body,
            text="Upload Data",
            bg=widget_bg,
            activebackground="white",
            bd=1,
            highlightthickness=0,
            relief="flat",
            foreground="#5EFF5E",
            command=lambda: self.handle_btn_press("upload")
        )

        # Footer widgets
        info_icon = PhotoImage(file=preset.info_path)
        self.footer_widgets["info"] = Button(
            self.footer,
            image=info_icon,
            bg=widget_bg,
            activebackground=win_bg,
            bd=0,
            highlightthickness=0,
            relief="ridge",
            command=lambda: self.handle_btn_press("info"),
        )
        self.footer_widgets["info"].image = info_icon
        exit_icon = PhotoImage(file=preset.exit_path)
        self.footer_widgets["exit"] = Button(
            self.footer,
            image=exit_icon,
            bg=widget_bg,
            activebackground=win_bg,
            bd=0,
            highlightthickness=0,
            relief="ridge",
            command=lambda: self.handle_btn_press("exit")
        )
        self.footer_widgets["exit"].image = exit_icon

    def display_win(self):
        self.container.grid(column=0, row=0, sticky='nesw')
        self.header.grid(column=0, row=0, sticky='nesw', padx=5, pady=5)
        self.body.grid(column=0, row=1, sticky='nesw', padx=5, pady=5)
        self.footer.grid(column=0, row=2, sticky='nesw', padx=5, pady=5)

        for i, option in enumerate(self.header_widgets):
            self.header_widgets[option].grid(
                column=i,
                row=0,
                padx=15, pady=15)
        # self.header_widgets["profile"].grid(column=0, row=0)
        # self.header_widgets["title"].grid(column=1, row=0)
        # self.header_widgets["settings"].grid(column=2, row=0)

        for i, action in enumerate(self.body_widgets):
            action = self.body_widgets[action]
            action["label"].grid(
                column=0, row=i, padx=15, pady=15
            )
            action["button"].grid(
                column=1, row=i, padx=15, pady=15
            )
        # self.body_widgets["scan"].grid(column=0, row=0, padx=15, pady=15)
        # self.body_widgets["collect"].grid(column=0, row=1)
        # self.body_widgets["upload"].grid(column=0, row=2)
        # self.body_widgets["exit"].grid(column=0, row=3)

        self.footer_widgets["info"].grid(
            column=0,
            row=0,
            padx=15, pady=15,
            sticky='w'
        )
        self.footer_widgets["exit"].grid(
            column=1,
            row=0,
            padx=15, pady=15,
            sticky='e'
        )
