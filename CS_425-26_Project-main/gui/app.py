from tkinter import ttk, Frame, Button, Label, PhotoImage, messagebox, Listbox, StringVar
import constants as preset
import threading


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
        self.win.configure(bg="#0c131e")
        self.win.columnconfigure(0, weight=1)
        self.win.rowconfigure(0, weight=1)


class MainMenu:
    def __init__(self, network, window):
        self.network = network
        self.win = window
        self.win_bg = self.win.configure("bg")[-1]
        self.frame_bg = "#3b3b3b" if not self.win.is_prod else self.win_bg
        self.container = Frame(
            self.win,
            bg=self.win_bg,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.output = Frame(
            self.container,
            bg=self.frame_bg,
            bd=0,
            width=150,
            highlightthickness=0,
            relief="ridge",
        )
        self.header = Frame(
            self.container,
            bg=self.frame_bg,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.body = Frame(
            self.container,
            bg=self.frame_bg,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.footer = Frame(
            self.container,
            bg=self.frame_bg,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.set_win()

        self.devices = StringVar(value=self.network.devices)
        self.output_widgets = {}
        self.header_widgets = {}
        self.body_widgets = {}
        self.footer_widgets = {}
        self.alert_widgets = {}
        self.set_widgets()

        self.display_win()

    def set_win(self):
        self.container.columnconfigure(0, weight=2)
        self.container.columnconfigure(1, weight=1)
        self.container.rowconfigure(0, weight=1)
        self.container.rowconfigure(1, weight=5)
        self.container.rowconfigure(2, weight=3)

        self.output.columnconfigure(0, weight=1)
        self.output.rowconfigure(0, weight=1)

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

    def scan_thread(self):
        self.network.scan()
        self.output_widgets["scan_progress"].stop()
        self.body_widgets["scan"]["button"]["state"] = "normal"
        self.footer_widgets["exit"]["state"] = "normal"
        messagebox.showinfo(self.win.version, "Scan Complete")
        self.output_widgets["scan_progress"].grid_forget()

    def handle_btn_press(self, option):
        print("clicked on", option, "button")

        has_output = ["scan", "collect", "info"]
        if option in has_output:
            match option:
                case "scan":
                    self.output.grid(column=1, row=0, rowspan=3, sticky='nesw', padx=5, pady=5)
                    self.output_widgets["scan_progress"].grid(
                        column=0,
                        row=0,
                        padx=10, pady=10
                    )
                    self.output_widgets["scan_progress"].start(5)
                    self.body_widgets["scan"]["button"]["state"] = "disabled"
                    self.footer_widgets["exit"]["state"] = "disabled"
                    threading.Thread(target=self.scan_thread).start()
                case "collect":
                    if self.network.can_upload():
                        self.output.grid(column=1, row=0, rowspan=3, sticky='nesw', padx=5, pady=5)
                        self.network.collect()
                        messagebox.showinfo(
                            self.win.version,
                            "Collection Complete"
                        )
                    else:
                        messagebox.showerror(
                            self.win.version,
                            "Nothing to upload.\nTry scanning network first.")
                        self.output.grid_forget()
                case "info":
                    self.output.grid(column=1, row=0, rowspan=3, sticky='nesw', padx=5, pady=5)
                    pass
        else:
            self.output.grid_forget()
            match option:
                case "profile":
                    pass
                case "settings":
                    pass
                case "upload":
                    if self.network.can_upload():
                        self.network.upload()
                        messagebox.showinfo(
                            self.win.version,
                            "Upload Complete")
                    else:
                        messagebox.showerror(
                            self.win.version,
                            "Nothing to upload.\nTry scanning network first.")
                case "exit":
                    print("Goodbye!")
                    self.win.destroy()

    def set_widgets(self):
        widget_bg = self.frame_bg
        win_bg = self.win_bg
        # Output widgets
        self.output_widgets["scan_progress"] = ttk.Progressbar(
            self.output,
            orient='horizontal',
            mode='indeterminate',
            length=140
        )
        self.output_widgets["list_title"] = Label(
            self.header,
            text=self.network,
            bg=widget_bg,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.output_widgets["device_list"] = Listbox(
            self.output,
            listvariable=self.devices,
            justify="center"
        )

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

        # self.body_widgets["scan"]["button"] = Button(
        #     self.body,
        #     text="Scan Network",
        #     bg=widget_bg,
        #     activebackground="white",
        #     bd=1,
        #     highlightthickness=0,
        #     relief="solid",
        #     foreground="#5EFF5E",
        #     command=lambda: self.handle_btn_press("scan")
        # )
        scan_button = PhotoImage(file=preset.scan_button)
        self.body_widgets["scan"]["button"] = Button(
            self.body,
            image=scan_button,
            bg=widget_bg,
            activebackground="white",
            bd=0,
            highlightthickness=0,
            # relief="solid",
            # foreground="#5EFF5E",
            command=lambda: self.handle_btn_press("scan")
        )
        self.body_widgets["scan"]["button"].image = scan_button

        # self.body_widgets["collect"]["button"] = Button(
        #     self.body,
        #     text="Collect Data",
        #     bg=widget_bg,
        #     activebackground="white",
        #     bd=0,
        #     highlightthickness=0,
        #     relief="flat",
        #     foreground="#5EFF5E",
        #     command=lambda: self.handle_btn_press("collect")
        # )
        collect_button = PhotoImage(file=preset.collect_button)
        self.body_widgets["collect"]["button"] = Button(
            self.body,
            image=collect_button,
            bg=widget_bg,
            activebackground="white",
            bd=0,
            highlightthickness=0,
            # relief="solid",
            # foreground="#5EFF5E",
            command=lambda: self.handle_btn_press("collect")
        )
        self.body_widgets["collect"]["button"].image = collect_button

        # self.body_widgets["upload"]["button"] = Button(
        #     self.body,
        #     text="Upload Data",
        #     bg="#5EFF5E",
        #     activebackground="white",
        #     bd=1,
        #     highlightthickness=0,
        #     relief="flat",
        #     foreground=widget_bg,
        #     command=lambda: self.handle_btn_press("upload")
        # )
        upload_button = PhotoImage(file=preset.upload_button)
        self.body_widgets["upload"]["button"] = Button(
            self.body,
            image=upload_button,
            bg=widget_bg,
            activebackground="white",
            bd=0,
            highlightthickness=0,
            # relief="solid",
            # foreground="#5EFF5E",
            command=lambda: self.handle_btn_press("upload")
        )
        self.body_widgets["upload"]["button"].image = upload_button

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
        # self.output.grid(column=1, row=0, rowspan=3, sticky='nesw', padx=5, pady=5)
        self.header.grid(column=0, row=0, sticky='nesw', padx=5, pady=5)
        self.body.grid(column=0, row=1, sticky='nesw', padx=5, pady=5)
        self.footer.grid(column=0, row=2, sticky='nesw', padx=5, pady=5)

        # self.output_widgets["scan_progress"].grid(
        #     column=0,
        #     row=0,
        #     padx=10, pady=10
        # )

        for i, option in enumerate(self.header_widgets):
            self.header_widgets[option].grid(
                column=i,
                row=0,
                padx=15, pady=15)

        for i, action in enumerate(self.body_widgets):
            action = self.body_widgets[action]
            action["label"].grid(
                column=0, row=i, padx=15, pady=15
            )
            action["button"].grid(
                column=1, row=i, padx=15, pady=15
            )

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
