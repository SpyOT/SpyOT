from tkinter import ttk, Frame, Button, Label, PhotoImage, messagebox, Listbox, StringVar
import threading
import SpyOT.gui.constants as preset
from .frames import *
from ..widgets import *


class MainWindow:
    def __init__(self, network, window):
        self.network = network
        self.win = window
        self.is_prod = self.win.APP_ENV == "prod"
        self.win_bg = self.win.configure("bg")[-1]
        self.frame_bg = self.win_bg if self.is_prod else "#3b3b3b"
        self.text_color = "#5EFF5E"

        self.container = CustomContainer(frame=self.win, background=self.win_bg,
                                         col_config={0: 2, 1: 1},
                                         row_config={0: 1, 1: 5, 2: 3})

        self.header = CustomHeader(frame=self.container, background=self.frame_bg,
                                   col_config={0: 1, 1: 8, 2: 1},
                                   row_config={0: 1})

        self.body = CustomBody(frame=self.container, background=self.frame_bg,
                               col_config={0: 1, 1: 1},
                               row_config={0: 1, 1: 1, 2: 1, 3: 1})

        self.output = Frame(
            self.container,
            bg=self.frame_bg,
            bd=0,
            width=150,
            highlightthickness=0,
            relief="ridge",
        )

        self.footer = CustomFooter(frame=self.container, background=self.frame_bg,
                                   col_config={0: 1, 1: 1},
                                   row_config={0: 1})

        self.set_win()

        self.devices = StringVar(value=[self.network.devices[device]["name"] for device in self.network.devices])
        self.host = StringVar(value=self.network.host["name"])
        self.selected_device, self.selected_index = "", 0
        self.info_toggle = 1
        self.output_widgets = {}
        self.alert_widgets = {}
        self.set_widgets()

        self.display_win()

    def set_win(self):
        self.output.columnconfigure(0, weight=1)
        self.output.columnconfigure(1, weight=1)
        self.output.rowconfigure(0, weight=1)
        self.output.rowconfigure(1, weight=2)
        self.output.rowconfigure(2, weight=1)

    def scan_thread(self):
        self.network.scan()
        self.output_widgets["scan_progress"].stop()
        self.body_widgets["scan"]["button"]["state"] = "normal"
        self.footer_widgets["exit"]["state"] = "normal"
        messagebox.showinfo(self.win.version, "Scan Complete")
        self.output_widgets["scan_progress"].grid_forget()
        self.display_summary()

    def display_summary(self):
        self.host.set(self.network.host["name"])
        device_names = [device["name"] for device in self.network.devices]
        self.devices.set(device_names)
        self.output_widgets["host_caption"].grid(
            column=0, row=0,
            padx=5, pady=5,
            sticky='s'
        )
        self.output_widgets["host_name"].grid(
            column=1, row=0,
            padx=5, pady=5,
            sticky='s'
        )
        self.configure_bl_device()
        self.output_widgets["device_list"].grid(
            column=0, columnspan=2,
            row=1, padx=5, pady=5,
            sticky='nesw'
        )
        self.output_widgets["add_device"].grid(
            column=1,
            row=2, padx=5, pady=5,
            sticky='nesw'
        )
        self.output_widgets["remove_device"].grid(
            column=0,
            row=2, padx=5, pady=5,
            sticky='nesw'
        )

    def handle_btn_press(self, option):
        print("clicked on", option, "button")

        has_output = ["scan", "collect", "info", "add_to_bl", "remove_from_bl"]
        if option in has_output:
            match option:
                case "scan":
                    self.output.grid(column=1, row=0, rowspan=3, sticky='nesw', padx=5, pady=5)
                    self.output_widgets["scan_progress"].grid(
                        column=0, columnspan=2,
                        row=0,
                        padx=10, pady=10,
                        sticky="n"
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
                        self.display_summary()
                    else:
                        messagebox.showerror(
                            self.win.version,
                            "Nothing to upload.\nTry scanning network first.")
                        self.output.grid_forget()
                case "info":
                    if self.info_toggle:
                        self.output.grid(column=1, row=0, rowspan=3, sticky='nesw', padx=5, pady=5)
                        self.output_widgets["info"].grid(
                            column=0, columnspan=2,
                            row=0, rowspan=3,
                            sticky='nesw', padx=5, pady=5
                        )
                        self.info_toggle = not self.info_toggle
                    else:
                        self.output_widgets["info"].grid_forget()
                        self.output.grid_forget()
                        self.info_toggle = not self.info_toggle
                    pass
                case "add_to_bl":
                    print(self.selected_device)
                    result = self.network.add_to_blacklist(self.selected_device)
                    device_list = self.output_widgets["device_list"]
                    if result:
                        device_list.selection_clear(0, 'end')
                        device_list.itemconfigure(
                            self.selected_index,
                            bg=self.win_bg,
                            foreground='white')
                        self.disable_device_options()
                case "remove_from_bl":
                    print(self.selected_device)
                    result = self.network.remove_from_blacklist(self.selected_device)
                    device_list = self.output_widgets["device_list"]
                    if result:
                        device_list.selection_clear(0, 'end')
                        device_list.itemconfigure(
                            self.selected_index,
                            bg='white',
                            foreground=self.win_bg)
                        self.disable_device_options()
        else:
            self.output.grid_forget()
            match option:
                case "profile":
                    pass
                case "settings":
                    pass
                case "upload":
                    if self.network.metadata:
                        is_success = self.network.upload()
                        if is_success:
                            messagebox.showinfo(
                                self.win.version,
                                "Upload Complete")
                        else:
                            messagebox.showerror(
                                self.win.version,
                                "Error with Upload")
                    else:
                        messagebox.showerror(
                            self.win.version,
                            "Nothing to upload.\nTry scanning network first.")
                case "exit":
                    print("Goodbye!")
                    self.win.destroy()

    def display_device_options(self, *args):
        device_names = [device["name"] for device in self.network.devices]
        self.output_widgets["add_device"]["bg"] = self.text_color
        self.output_widgets["add_device"]["state"] = 'normal'
        self.output_widgets["remove_device"]["bg"] = self.text_color
        self.output_widgets["remove_device"]["state"] = 'normal'
        device_display = self.output_widgets["device_list"]
        curr_dev = device_display.curselection()[0]
        self.selected_index = curr_dev
        self.selected_device = device_names[curr_dev]

    def disable_device_options(self):
        self.output_widgets["add_device"]["bg"] = self.frame_bg
        self.output_widgets["add_device"]["state"] = 'disabled'
        self.output_widgets["remove_device"]["bg"] = self.frame_bg
        self.output_widgets["remove_device"]["state"] = 'disabled'

    def configure_bl_device(self):
        bl_devices = self.network.get_blacklist()
        bl_devices = [device.strip('\n') for device in bl_devices]
        device_names = [device["name"] for device in self.network.devices]
        bl_indices = [i for i, device in enumerate(device_names) if device in bl_devices]
        device_list = self.output_widgets["device_list"]
        device_list.selection_clear(0, 'end')
        for index in bl_indices:
            device_list.itemconfigure(
                index,
                bg=self.win_bg,
                foreground='white')

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
        self.output_widgets["host_caption"] = Label(
            self.output,
            text="Network Name:",
            foreground=self.text_color,
            bg=widget_bg,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.output_widgets["host_name"] = Label(
            self.output,
            textvariable=self.host,
            foreground=self.text_color,
            bg=widget_bg,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.output_widgets["device_list"] = Listbox(
            self.output,
            listvariable=self.devices,
            foreground=self.win_bg,
            # bg=widget_bg,
            # bd=0,
            # highlightthickness=0,
            # relief="ridge",
            justify="center"
        )
        device_list = self.output_widgets["device_list"]
        device_list.bind('<<ListboxSelect>>', self.display_device_options)

        self.output_widgets["add_device"] = Button(
            self.output,
            text="Blacklist Device",
            bg=self.frame_bg,
            activebackground="white",
            bd=0,
            highlightthickness=0,
            relief="solid",
            state="disabled",
            command=lambda: self.handle_btn_press("add_to_bl")
        )

        self.output_widgets["remove_device"] = Button(
            self.output,
            text="Whitelist Device",
            bg=self.frame_bg,
            activebackground="white",
            bd=0,
            highlightthickness=0,
            relief="solid",
            state="disabled",
            command=lambda: self.handle_btn_press("remove_from_bl")
        )

        about_text = """
        Instructions -
        scan network: Performs a light weight scan on your 
        network with the help of the Nmap library. Once complete,
        a list containing all devices on your network will
        be displayed on this right-hand display.

        collect data: Performs an in-depth scan of your network
        that allows it to collect information on each devices ports
        including: protocol, availability, and service. At this point
        you may also blacklist specific devices by clicking on 
        the devices name, then selecting the 'Add to blacklist' button.
        You may also remove that device from your blacklist by
        selecting the 'Remove from blacklist' button.

        upload data: Connects to our database server and updates
        the collected data to remove devices in the blacklist. Once
        complete, a message will appear stating whether your data
        was successfully uploaded or not.
        """
        self.output_widgets["info"] = Label(
            self.output,
            text=about_text,
            foreground=self.text_color,
            bg=widget_bg,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        # Header widgets
        profile_icon = PhotoImage(file=preset.profile_path)
        self.header.set_widget("profile", CustomButton,
                               image=profile_icon,
                               bg=widget_bg,
                               command=lambda: self.handle_btn_press("profile"))
        title_icon = PhotoImage(file=preset.title_path)
        self.header.set_widget("title", CustomLabel,
                               image=title_icon,
                               bg=widget_bg
                               )
        settings_icon = PhotoImage(file=preset.setting_path)
        self.header.set_widget("settings", CustomButton,
                               image=settings_icon,
                               bg=widget_bg,
                               command=lambda: self.handle_btn_press("settings"))

        # Body widgets
        actions = {"scan": {"label": preset.scan_path, "button": preset.scan_button},
                   "collect": {"label": preset.collect_path, "button": preset.collect_button},
                   "upload": {"label": preset.upload_path, "button": preset.upload_button}}
        for action in actions:
            action_label_icon = PhotoImage(file=actions[action]["label"])
            action_label = action + "_label"
            self.body.set_widget(action_label, CustomLabel,
                                 image=action_label_icon,
                                 bg=widget_bg)
            action_button_icon = PhotoImage(file=actions[action]["button"])
            action_button = action + "_button"

            def callback(curr_action=action):
                self.handle_btn_press(curr_action)

            self.body.set_widget(action_button, CustomButton,
                                 image=action_button_icon,
                                 bg=widget_bg,
                                 command=callback
                                 )
            self.body.set_actions(action,
                                  self.body.get_widget(action_label),
                                  self.body.get_widget(action_button))

        # Footer widgets
        info_icon = PhotoImage(file=preset.info_path)
        self.footer.set_widget("info", CustomButton,
                               image=info_icon,
                               bg=widget_bg,
                               command=lambda: self.handle_btn_press("info"))

        exit_icon = PhotoImage(file=preset.exit_path)
        self.footer.set_widget("exit", CustomButton,
                               image=exit_icon,
                               bg=widget_bg,
                               command=lambda: self.handle_btn_press("exit"))

    def display_win(self):
        self.container.grid(column=0, row=0, sticky='nesw')
        # self.output.grid(column=1, row=0, rowspan=3, sticky='nesw', padx=5, pady=5)
        self.header.grid(column=0, row=0, sticky='nesw', padx=5, pady=5)
        self.body.grid(column=0, row=1, sticky='nesw', padx=5, pady=5)
        self.footer.grid(column=0, row=2, sticky='nesw', padx=5, pady=5)

        self.header.display_widgets()
        self.body.display_widgets()
        self.footer.display_widgets()
