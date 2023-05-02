from .custom_widgets import CustomContainer, CustomButton, CustomLabel
from tkinter import ttk, Entry, StringVar, Listbox, PhotoImage
from gui import constants as const


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
        self.email_entry = ""
        self.password_entry = ""
        self.host_name = None
        self.device_list = None
        self.thread = None

        self.light_mode_icon = PhotoImage(file=const.LIGHT_MODE_ICON)
        self.dark_mode_icon = PhotoImage(file=const.DARK_MODE_ICON)

    # override this method from CustomContainer
    def set_widgets(self, controller):
        """ Login Widgets """
        self.set_widget("login_prompt", CustomLabel,
                        style='ttk.Label.CustomLabel.TLabel',
                        text="""Please enter a valid email and password to login
                        or create a new account."""
                        )
        self.set_widget("email_label", CustomLabel,
                        style='ttk.Label.CustomLabel.TLabel',
                        text='Email:')
        self.set_widget("email_entry", Entry,
                        textvariable=self.email_entry, )
        self.set_widget("password_label", CustomLabel,
                        style='ttk.Label.CustomLabel.TLabel',
                        text='Password:')
        self.set_widget("password_entry", Entry,
                        textvariable=self.password_entry,
                        show='*')
        self.set_widget("login_btn", CustomButton,
                        style=const.BUTTON_STYLE,
                        text='Login',
                        command=lambda: controller.handle_btn_press("login"))
        self.set_widget("register_btn", CustomButton,
                        style=const.BUTTON_STYLE,
                        text='Create Account',
                        command=lambda: controller.handle_btn_press("register"))
        """ Profile Widgets """
        self.set_widget("logout_btn", CustomButton,
                        style=const.BUTTON_STYLE,
                        text='Logout',
                        command=lambda: controller.handle_btn_press("logout"))
        """ Settings Widgets """
        self.set_widget("toggle_theme", CustomButton,
                        style=const.BUTTON_STYLE,
                        image=self.dark_mode_icon,
                        command=lambda: controller.handle_btn_press("toggle_theme"))

        """ Loading Widgets """
        self.set_widget("loading_bar", ttk.Progressbar,
                        orient='horizontal',
                        mode='indeterminate',
                        length=200)
        self.set_widget("loading_label", CustomLabel,
                        style='ttk.Label.CustomLabel.TLabel',
                        font='default 12 bold',
                        text='Loading...')
        self.set_widget("cancel", CustomButton,
                        style=const.BUTTON_STYLE,
                        text='Cancel',
                        command=lambda: controller.handle_btn_press("cancel"))

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
                        style=const.BUTTON_STYLE,
                        text='New Scan',
                        command=lambda: controller.handle_btn_press("run_scan"))
        self.set_widget("add_to_blacklist", CustomButton,
                        style=const.BUTTON_STYLE,
                        text="Blacklist",
                        state='disabled',
                        command=lambda: controller.handle_btn_press("blacklist"))
        self.set_widget("add_to_whitelist", CustomButton,
                        style=const.BUTTON_STYLE,
                        text="Whitelist",
                        state='disabled',
                        command=lambda: controller.handle_btn_press("whitelist"))

        """ Collect Widgets """
        self.set_widget("summary_label", CustomLabel,
                        style='ttk.Label.CustomLabel.TLabel',
                        text='Summary:')
        self.set_widget("device_summary", ttk.Treeview,
                        columns='Status')
        self.get_widget("device_summary").column('#0', stretch='no')
        self.get_widget("device_summary").heading('#0', text='Device')
        self.get_widget("device_summary").column('Status', anchor='center')
        self.get_widget("device_summary").heading('Status', text='Status')
        self.set_widget("edit_list", CustomButton,
                        style=const.BUTTON_STYLE,
                        text='Edit List',
                        command=lambda: controller.handle_btn_press("output_scan"))
        self.set_widget("view_report", CustomButton,
                        style=const.BUTTON_STYLE,
                        text='View Report',
                        command=lambda: controller.handle_btn_press("view_report"))
        self.set_widget("save_report", CustomButton,
                        style=const.BUTTON_STYLE,
                        text='Save Report',
                        command=lambda: controller.handle_btn_press("save_report"))

        """ Upload Widgets """

        """ About Widgets """

    def set_view(self, view):
        self.view = view

    def update_view(self, view):
        self.reset_frame()
        self.set_view(view)
        self.configure(width=const.FRAME_MIN_WIDTH, height=const.FRAME_MIN_HEIGHT)
        self.display_frame(column=1, row=0, sticky='n e s w')

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
                self.display_widget("cancel", #sticky='',
                                    column=0, row=3, columnspan=2,
                                    padx=15, pady=15)
                self.get_widget("loading_bar").start(5)
            case "login":
                self.get_widget("email_entry").delete(0, "end")
                self.get_widget("password_entry").delete(0, "end")
                self.display_widget("login_prompt", sticky='ns',
                                    column=0, columnspan=2, row=0,
                                    padx=15, pady=15)
                self.display_widget("email_label", sticky='w',
                                    column=0, row=1,
                                    padx=15, pady=15)
                self.display_widget("email_entry", sticky='ew',
                                    column=0, columnspan=2, row=1, rowspan=2,
                                    padx=15, pady=15)
                self.display_widget("password_label", sticky='w',
                                    column=0, row=2,
                                    padx=15, pady=15)
                self.display_widget("password_entry", sticky='ew',
                                    column=0, columnspan=2, row=2, rowspan=2,
                                    padx=15, pady=15)
                self.display_widget("login_btn",  sticky='s',
                                    column=0, columnspan=2, row=3,
                                    padx=15, pady=15,
                                    ipadx=15)
                self.display_widget("register_btn",  sticky='n',
                                    column=0, columnspan=2, row=4,
                                    padx=15, pady=15,
                                    ipadx=15)
            case "profile":
                self.display_widget("logout_btn", sticky='n',
                                    column=0, row=4, columnspan=2,
                                    padx=15, pady=15)

            case "settings":
                self.display_widget("toggle_theme", sticky='nsew',
                                    column=0, row=0, columnspan=2, rowspan=2,
                                    padx=15, pady=15)
            case "blacklist":
                self.set_selected_device_status(True)
                self.update_view("output_scan")
            case "whitelist":
                self.set_selected_device_status(False)
                self.update_view("output_scan")
            case "output_scan":
                self.update_scan_output()  # Update host_name, device_list, and
                # device list bindings

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
            case "output_collect":
                self.update_collect_output()
                self.display_widget("summary_label", sticky='nsew',
                                    column=0, row=0, columnspan=2,
                                    padx=15, pady=15)
                self.display_widget("device_summary", sticky='nsew',
                                    column=0, row=1, columnspan=2, rowspan=2,
                                    padx=15, pady=15)
                self.display_widget("view_report", sticky='nsew',
                                    column=0, row=3,
                                    padx=15, pady=15)
                self.display_widget("save_report", sticky='nsew',
                                    column=1, row=3,
                                    padx=15, pady=15)
                self.display_widget("edit_list", sticky='nsew',
                                    column=0, row=4, columnspan=2,
                                    padx=15, pady=15)
            case "output_upload":
                pass
            case "about":
                pass
            case "none":
                pass
            case _:
                print("Error: Invalid view name")

    """ Utils """

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

    def update_collect_output(self):
        device_summary_tree = self.get_widget("device_summary")
        if device_summary_tree.get_children():
            device_summary_tree.delete(*device_summary_tree.get_children())
        # Get device summary metadata from systems
        device_summary_values = self.systems.get_device_summary()
        # Insert device summary into treeview
        for _, device_metadata in device_summary_values.items():
            device_summary_tree.insert('', 'end', text=device_metadata['hostname'],
                                       values=(device_metadata['status']))

    def set_selected_device_status(self, status):
        selected_device_name = self.get_selected_device()
        selected_device_ip = self.systems.get_device_ip(selected_device_name)
        self.systems.update_device_blacklist_status(selected_device_ip, status)
        if status:
            self.update_selected_device(bg=const.BLACKLIST_PRIMARY, fg=const.BLACKLIST_SECONDARY)
        else:
            self.update_selected_device(bg=const.WHITELIST_PRIMARY, fg=const.WHITELIST_SECONDARY)

    def toggle_theme(self, value):
        if value == "DARK":
            self.update_widget_value("toggle_theme", "image", self.light_mode_icon)
        else:
            self.update_widget_value("toggle_theme", "image", self.dark_mode_icon)
        self.set_view("settings")

    def get_login_info(self):
        email = self.get_widget("email_entry").get()
        password = self.get_widget("password_entry").get()
        return email, password
