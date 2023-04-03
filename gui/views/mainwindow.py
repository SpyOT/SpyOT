from tkinter import ttk, Frame, Button, Label, PhotoImage, messagebox, Listbox, StringVar
import threading
import SpyOT.gui.constants as preset
from .frames import *
from ..widgets import *


class MainWindow:
    def __init__(self, systems, window):
        self.systems = systems
        self.win = window
        self.is_prod = self.win.APP_ENV == "prod"
        self.win_bg = self.win.configure("bg")[-1]
        self.frame_bg = self.win_bg if self.is_prod else "#3b3b3b"
        self.button_bg = "#1DD75B"
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

        self.output = CustomOutput(frame=self.container, background=self.frame_bg,
                                   col_config={0: 1, 1: 1},
                                   row_config={0: 1, 1: 2, 2: 1, 3: 1})

        self.footer = CustomFooter(frame=self.container, background=self.frame_bg,
                                   col_config={0: 1, 1: 1},
                                   row_config={0: 1})

        self.devices = StringVar(value=[self.systems.devices[device]["name"] for device in self.systems.devices])
        self.host = StringVar(value=self.systems.host["name"])
        self.selected_device, self.selected_index = "", 0
        self.info_toggle = 1
        self.alert_widgets = {}
        self.set_widgets()
        self.thread = None
        self.display_win()

    def set_widgets(self):
        widget_bg = self.frame_bg
        button_bg = "#1DD75B"
        """ Header widgets"""
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

        """ Body widgets"""
        actions = {"scan": {"label": preset.scan_path, "button": preset.scan_button},
                   "collect": {"label": preset.collect_path, "button": preset.collect_button},
                   "upload": {"label": preset.upload_path, "button": preset.upload_button}}
        for action in actions:
            action_label_icon = PhotoImage(file=actions[action]["label"])
            action_button_icon = PhotoImage(file=actions[action]["button"])
            action_label, action_button = action + "_label", action + "_button"
            self.body.set_widget(action_label, CustomLabel,
                                 image=action_label_icon,
                                 bg=widget_bg)

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

        """ Footer widgets"""
        info_icon = PhotoImage(file=preset.info_path)
        self.footer.set_widget("info", CustomButton,
                               image=info_icon,
                               bg=widget_bg,
                               command=lambda: self.handle_btn_press("info"))

        toggle_output_icon = PhotoImage(file=preset.expand_button)
        self.footer.set_widget("toggle_output", CustomButton,
                               image=toggle_output_icon,
                               bg=widget_bg,
                               command=lambda: self.handle_btn_press("toggle_output"))

        """ Output widgets"""
        self.output.set_widget("progress_bar", ttk.Progressbar,
                               orient="horizontal",
                               mode="indeterminate",
                               length=140)

        self.output.set_widget("host_label", CustomLabel,
                               text="Detected Network:",
                               foreground=self.text_color,
                               bg=widget_bg)

        self.output.vars["host_name"] = StringVar(value=self.systems.get_hostname())
        self.output.set_widget("host_name", CustomLabel,
                               textvariable=self.output.vars["host_name"],
                               foreground=self.text_color,
                               bg=widget_bg)

        self.output.vars["devices"] = StringVar(value=self.systems.get_devices())
        self.output.set_widget("devices", Listbox,
                               listvariable=self.output.vars["devices"],
                               foreground=self.win_bg,
                               justify='center')
        self.output.get_widget("devices").bind('<<ListboxSelect>>',
                                               self.update_scan_buttons)

        self.output.set_widget("new_scan", CustomButton,
                               text="New Scan",
                               bg=self.button_bg,
                               command=lambda: self.handle_btn_press("run_scan"))

        self.output.set_widget("blacklist", CustomButton,
                               text="Blacklist",
                               bg=self.frame_bg,
                               state="disabled",
                               command=lambda: self.handle_btn_press("blacklist"))

        self.output.set_widget("whitelist", CustomButton,
                               text="Whitelist",
                               bg=self.frame_bg,
                               state="disabled",
                               command=lambda: self.handle_btn_press("whitelist"), )

        self.output.set_widget("info", CustomLabel,
                               text=preset.about_text,
                               bg=widget_bg,
                               foreground=self.text_color)

    def display_win(self):
        self.container.grid(column=0, row=0, sticky='nesw')
        self.header.display_frame(column=0, row=0, sticky='nesw', padx=5, pady=5)
        self.body.display_frame(column=0, row=1, sticky='nesw', padx=5, pady=5)
        self.footer.display_frame(column=0, row=2, sticky='nesw', padx=5, pady=5)

    def handle_btn_press(self, option):
        if not self.is_prod:
            print("clicked on", option, "button")

        match option:
            # Header Buttons
            case "profile":
                pass
            case "settings":
                pass
            # Body Buttons
            case "run_scan":
                self.toggle_buttons()
                self.output.set_view('scan_run')
                self.output.display_frame(
                    column=1, row=0,
                    rowspan=3,
                    sticky='nesw',
                    padx=5, pady=5)
                self.thread = threading.Thread(target=self.scan_thread).start()
            case "scan":
                if self.systems.scan_exists():
                    self.update_devices()
                    self.output.set_view('scan_output')
                    self.output.display_frame(
                        column=1, row=0,
                        rowspan=3,
                        sticky='nesw',
                        padx=5, pady=5)
                else:
                    self.handle_btn_press("run_scan")
            case "collect":
                self.systems.remove_scans()
            case "upload":
                pass
            # Footer Buttons
            case "info":
                self.output.set_view(option)
                self.output.toggle_frame(
                    column=1, row=0,
                    rowspan=3,
                    sticky='nesw',
                    padx=5, pady=5)
            case "toggle_output":
                self.output.toggle_frame(
                    column=1, row=0,
                    rowspan=3,
                    sticky='nesw',
                    padx=5, pady=5)
            # Output Buttons
            case "blacklist":
                selected_device = self.get_selected_device()
                selected_index = self.output.get_selected_index()
                result = self.systems.add_to_blacklist(selected_device)
                if result:
                    self.output.update_selected_device(selected_index,
                                                       bg=self.win_bg,
                                                       foreground='white')
                self.update_scan_buttons()
            case "whitelist":
                selected_device = self.get_selected_device()
                selected_index = self.output.get_selected_index()
                result = self.systems.remove_from_blacklist(selected_device)
                if result:
                    self.output.update_selected_device(selected_index,
                                                       bg='white',
                                                       foreground=self.frame_bg)
                self.update_scan_buttons()
        self.update_footer_toggle()

        # Output Buttons
        # TBD
        # match option:
        #     case "collect":
        #         if self.systems.can_upload():
        #             self.output.grid(column=1, row=0, rowspan=3, sticky='nesw', padx=5, pady=5)
        #             self.systems.collect()
        #             messagebox.showinfo(
        #                 self.win.version,
        #                 "Collection Complete"
        #             )
        #             self.display_summary()
        #         else:
        #             messagebox.showerror(
        #                 self.win.version,
        #                 "Nothing to upload.\nTry scanning systems first.")
        #             self.output.grid_forget()
        #     case "upload":
        #         if self.systems.metadata:
        #             is_success = self.systems.upload()
        #             if is_success:
        #                 messagebox.showinfo(
        #                     self.win.version,
        #                     "Upload Complete")
        #             else:
        #                 messagebox.showerror(
        #                     self.win.version,
        #                     "Error with Upload")
        #         else:
        #             messagebox.showerror(
        #                 self.win.version,
        #                 "Nothing to upload.\nTry scanning systems first.")

    # Output utils
    def update_footer_toggle(self):
        state = self.output.get_state()
        if state:
            toggle_icon = PhotoImage(file=preset.collapse_button)
        else:
            toggle_icon = PhotoImage(file=preset.expand_button)
        self.footer.update_widget_value(
            "toggle_output",
            "image", toggle_icon)

    def update_devices(self):
        self.output.vars['devices'].set(self.systems.get_device_names())

    def toggle_buttons(self):
        header_widgets = [self.header.get_widget(widget) for widget in self.header.get_widgets()]
        body_widgets = [self.body.get_widget(widget) for widget in self.body.get_widgets()]
        footer_widgets = [self.footer.get_widget(widget) for widget in self.footer.get_widgets()]
        widgets = header_widgets + body_widgets + footer_widgets
        for widget in widgets:
            if widget.winfo_class() == "Button":
                if widget["state"] == "disabled":
                    widget["state"] = "normal"
                else:
                    widget["state"] = "disabled"

    def scan_thread(self):
        result = self.systems.scan()
        self.output.set_view('scan_stop')
        self.output.display_frame(
            column=1, row=0,
            rowspan=3,
            sticky='nesw',
            padx=5, pady=5)
        self.toggle_buttons()
        if result:
            messagebox.showinfo(self.win.version, "Scan Complete")
            self.handle_btn_press("scan")
        else:
            messagebox.showerror(self.win.version, "!Error: Scan not successful")

    def update_scan_buttons(self, *args):
        selected_device_name = self.get_selected_device()
        blacklist = self.systems.get_blacklist()
        if not selected_device_name:
            self.output.disable_button("blacklist", bg=self.frame_bg)
            self.output.disable_button("whitelist")
        elif selected_device_name in blacklist:
            self.output.disable_button("blacklist", bg=self.frame_bg)
            self.output.enable_button("whitelist", bg=self.button_bg)
        else:
            self.output.enable_button("blacklist", bg=self.button_bg)
            self.output.disable_button("whitelist", bg=self.frame_bg)

    def get_selected_device(self):
        try:
            selected_index = self.output.get_widget("devices").curselection()[0]
            devices = self.systems.get_device_names()
            return devices[selected_index]
        except IndexError as _:
            return None

    def configure_bl_device(self):
        bl_devices = self.systems.get_blacklist()
        bl_devices = [device.strip('\n') for device in bl_devices]
        device_names = [device["name"] for device in self.systems.devices]
        bl_indices = [i for i, device in enumerate(device_names) if device in bl_devices]
        device_list = self.output_widgets["device_list"]
        device_list.selection_clear(0, 'end')
        for index in bl_indices:
            device_list.itemconfigure(
                index,
                bg=self.win_bg,
                foreground='white')
