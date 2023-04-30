from .custom_widgets import CustomContainer, CustomButton, CustomLabel
from tkinter import ttk, Entry, StringVar, Listbox


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
        self.view = "none"
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
                        listvariable=self.device_list)
        self.get_widget("devices").bind('<<ListboxSelect>>',
                                        self.handle_listbox_select)
        self.set_widget("new_scan", CustomButton,
                        style='ttk.Button.CustomButton.TButton',
                        text='New Scan',
                        command=lambda: controller.handle_btn_press("run_scan"))
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
        self.reset_frame()
        self.set_view(view)
        self.display_frame(column=1, row=0, sticky='n e s w')

    def get_view(self):
        return self.view

    def display_widgets(self, preload=False):
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
            case "output_scan":
                # Update the host name and device list

                self.update_scan_output()
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
            case "none":
                pass
            case _:
                print("Error: Invalid view name")

    def handle_listbox_select(self, _):
        selected_device = self.get_selected_device()
        device_metadata = self.systems.get_device_metadata(selected_device)
        device_index = device_metadata.index.tolist()[0]
        # Get device blacklist status from column 3
        status = device_metadata.at[device_index, 'blacklist']
        if status:
            self.get_widget("add_to_blacklist").configure(state='disabled')
            self.get_widget("add_to_whitelist").configure(state='normal')
        else:
            self.get_widget("add_to_blacklist").configure(state='normal')
            self.get_widget("add_to_whitelist").configure(state='disabled')

    def get_selected_device(self):
        selected_device_index = self.get_widget("devices").curselection()[0]
        selected_device = self.systems.get_devices()[selected_device_index]
        return selected_device

    def update_selected_device(self, **kwargs):
        selected_device_index = self.get_widget("devices").curselection()[0]
        self.get_widget("devices").itemconfigure(
            selected_device_index,
            **kwargs
        )
        self.get_widget("devices").selection_clear(selected_device_index)
        self.get_widget("add_to_blacklist").configure(state='disabled')
        self.get_widget("add_to_whitelist").configure(state='disabled')

    def update_scan_output(self):
        self.host_name.set(self.systems.get_hostname())
        self.device_list.set(self.systems.get_devices())
        listbox_obj = self.get_widget("devices")
        for device_index in range(listbox_obj.size()):
            device_name = listbox_obj.get(device_index)
            device_status = self.systems.get_device_status(device_name)
            if device_status:
                listbox_obj.itemconfigure(device_index,
                                         bg='black',
                                         fg='white')
            else:
                listbox_obj.itemconfigure(device_index,
                                         bg='white',
                                         fg='black')
