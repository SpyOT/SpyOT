from .custom_widgets import CustomContainer, CustomButton, CustomLabel
from tkinter import ttk, Entry, StringVar, Listbox, messagebox
from threading import Thread


class OutputView(CustomContainer):
    def __init__(self, frame, systems, **kwargs):
        super().__init__(
            frame,
            systems,
            **kwargs)
        self.configure_win(col_config={'col 0': 'weight 1',
                                       'col 1': 'weight 1'},
                           row_config={'row 0': 'weight 1',
                                       'row 1': 'weight 1',
                                       'row 2': 'weight 1',
                                       'row 3': 'weight 1',
                                       'row 4': 'weight 1', })
        self.view = None
        self.username_entry = ""
        self.password_entry = ""
        self.host_name = None
        self.device_list = None
        self.thread = None

    # override this method from CustomContainer
    def set_widgets(self, controller):
        """ Profile Widgets """
        self.set_widget("login_prompt", CustomLabel,
                        style='ttk.Label.CustomLabel.TLabel',
                        text='Please enter your username and password',
                        )
        self.set_widget("username_entry", Entry,
                        textvariable=self.username_entry, )
        self.set_widget("password_entry", Entry,
                        textvariable=self.password_entry,
                        show='*')
        self.set_widget("login_btn", CustomButton,
                        style='ttk.Button.CustomButton.TButton',
                        text='Login',
                        command=lambda: controller.handle_btn_press("login"))

        """ Settings Widgets """

        """ Loading Widgets """
        self.set_widget("loading_bar", ttk.Progressbar,
                        orient='horizontal',
                        mode='indeterminate',
                        length=200)
        self.set_widget("loading_label", CustomLabel,
                        style='ttk.Label.CustomLabel.TLabel',
                        font='default 12 bold',
                        text='Loading...')

        """ Scan Widgets """
        self.set_widget("host_label", CustomLabel,
                        style='ttk.Label.CustomLabel.TLabel',
                        text='Detected Network:')
        self.host_name = StringVar(value=self.systems.get_hostname())
        self.set_widget("host_name", CustomLabel,
                        style='ttk.Label.CustomLabel.TLabel',
                        textvariable=self.host_name)
        self.device_list = StringVar(value=self.systems.get_devices())
        self.set_widget("devices", Listbox,
                        justify='center',
                        listvariable=self.device_list, )
        self.set_widget("new_scan", CustomButton,
                        style='ttk.Button.CustomButton.TButton',
                        text='New Scan',
                        command=lambda: controller.handle_btn_press("new_scan"))
        self.set_widget("add_to_blacklist", CustomButton,
                        style='ttk.Button.CustomButton.TButton',
                        text="Blacklist",
                        state='disabled',
                        command=lambda: controller.handle_btn_press("blacklist"))
        self.set_widget("add_to_whitelist", CustomButton,
                        style='ttk.Button.CustomButton.TButton',
                        text="Whitelist",
                        state='disabled',
                        command=lambda: controller.handle_btn_press("whitelist"))

        """ Collect Widgets """

        """ Upload Widgets """

        """ About Widgets """

    def set_view(self, view):
        self.view = view

    def update_view(self, view):
        self.set_view(view)
        self.reset_frame()
        self.display_widgets()

    def get_view(self):
        return self.view

    def display_widgets(self):
        match self.view:
            case "loading":
                self.display_widget("loading_label", sticky='new',
                                    column=0, row=2, columnspan=2,
                                    padx=15, pady=15)
                self.display_widget("loading_bar", sticky='sew',
                                    column=0, row=2, columnspan=2,
                                    padx=15, pady=15)
                self.get_widget("loading_bar").start(5)

            case "profile":
                self.display_widget("login_prompt", sticky='ns',
                                    column=0, columnspan=2, row=0,
                                    padx=15, pady=15)
                self.display_widget("username_entry", sticky='ew',
                                    column=0, columnspan=2, row=1,
                                    padx=15, pady=15)
                self.display_widget("password_entry", sticky='ew',
                                    column=0, columnspan=2, row=2,
                                    padx=15, pady=15)
                self.display_widget("login_btn", sticky='nsew',
                                    column=0, columnspan=2, row=3,
                                    padx=15, pady=15)
            case "settings":
                pass
            case "new_scan":
                # Scan start
                print("New Scan View")
                self.update_view("loading")
                self.thread = Thread(target=lambda: self.run_thread("scan")).start()
            case "scan":
                # Scan start
                print("Scan View")
                if self.systems.get_metadata().empty:
                    print("No previous data, new scan starting")
                    self.update_view("new_scan")

                # Scan Complete
                self.display_widget("host_label", sticky='nsew',
                                    column=0, row=0,
                                    padx=15, pady=15)
                self.display_widget("host_name", sticky='nsew',
                                    column=1, row=0,
                                    padx=15, pady=15)
                self.display_widget("devices", sticky='nsew',
                                    column=0, columnspan=2, row=1, rowspan=2,
                                    padx=15, pady=15)
                self.display_widget("add_to_blacklist", sticky='nsew',
                                    column=0, row=3,
                                    padx=15, pady=15)
                self.display_widget("add_to_whitelist", sticky='nsew',
                                    column=1, row=3,
                                    padx=15, pady=15)
                self.display_widget("new_scan", sticky='ew',
                                    column=0, row=4, columnspan=2,
                                    padx=15, pady=15)

            case "collect":
                pass
            case "upload":
                pass
            case "about":
                pass
            case _:
                pass

    def run_thread(self, command):
        match command:
            case "scan":
                self.systems.scan()
                if not self.systems.get_metadata().empty:
                    self.get_widget("loading_bar").stop()
                    messagebox.showinfo("Scan Complete", "Scan Complete")
                    self.update_view("scan")
                else:
                    messagebox.showerror("Scan Error", "Scan Error")
            case _:
                pass
        return
