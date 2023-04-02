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
                                   row_config={0: 1, 1: 2, 2: 1})

        self.footer = CustomFooter(frame=self.container, background=self.frame_bg,
                                   col_config={0: 1, 1: 1},
                                   row_config={0: 1})

        self.devices = StringVar(value=[self.systems.devices[device]["name"] for device in self.systems.devices])
        self.host = StringVar(value=self.systems.host["name"])
        self.selected_device, self.selected_index = "", 0
        self.info_toggle = 1
        self.alert_widgets = {}
        self.set_widgets()

        self.display_win()

    def set_widgets(self):
        widget_bg = self.frame_bg
        win_bg = self.win_bg
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
        # self.output_widgets["scan_progress"] = ttk.Progressbar(
        #     self.output,
        #     orient='horizontal',
        #     mode='indeterminate',
        #     length=140
        # )
        # self.output_widgets["host_caption"] = Label(
        #     self.output,
        #     text="Network Name:",
        #     foreground=self.text_color,
        #     bg=widget_bg,
        #     bd=0,
        #     highlightthickness=0,
        #     relief="ridge"
        # )
        # self.output_widgets["host_name"] = Label(
        #     self.output,
        #     textvariable=self.host,
        #     foreground=self.text_color,
        #     bg=widget_bg,
        #     bd=0,
        #     highlightthickness=0,
        #     relief="ridge"
        # )
        # self.output_widgets["device_list"] = Listbox(
        #     self.output,
        #     listvariable=self.devices,
        #     foreground=self.win_bg,
        #     # bg=widget_bg,
        #     # bd=0,
        #     # highlightthickness=0,
        #     # relief="ridge",
        #     justify="center"
        # )
        # device_list = self.output_widgets["device_list"]
        # device_list.bind('<<ListboxSelect>>', self.display_device_options)
        #
        # self.output_widgets["add_device"] = Button(
        #     self.output,
        #     text="Blacklist Device",
        #     bg=self.frame_bg,
        #     activebackground="white",
        #     bd=0,
        #     highlightthickness=0,
        #     relief="solid",
        #     state="disabled",
        #     command=lambda: self.handle_btn_press("add_to_bl")
        # )
        #
        # self.output_widgets["remove_device"] = Button(
        #     self.output,
        #     text="Whitelist Device",
        #     bg=self.frame_bg,
        #     activebackground="white",
        #     bd=0,
        #     highlightthickness=0,
        #     relief="solid",
        #     state="disabled",
        #     command=lambda: self.handle_btn_press("remove_from_bl")
        # )
        #
        # self.output_widgets["info"] = Label(
        #     self.output,
        #     text=preset.about_text,
        #     foreground=self.text_color,
        #     bg=widget_bg,
        #     bd=0,
        #     highlightthickness=0,
        #     relief="ridge"
        # )
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
            case "scan":
                pass
            case "collect":
                pass
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
        self.update_footer_toggle()

        # Output Buttons
        # TBD
        # match option:
        #     case "scan":
        #         self.output.grid(column=1, row=0, rowspan=3, sticky='nesw', padx=5, pady=5)
        #         self.output_widgets["scan_progress"].grid(
        #             column=0, columnspan=2,
        #             row=0,
        #             padx=10, pady=10,
        #             sticky="n"
        #         )
        #         self.output_widgets["scan_progress"].start(5)
        #         self.body.actions["scan"]["button"]["state"] = "disabled"
        #         self.footer.widgets["toggle_output"]["state"] = "disabled"
        #         threading.Thread(target=self.scan_thread).start()
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
        #     case "info":
        #         if self.info_toggle:
        #             self.output.grid(column=1, row=0, rowspan=3, sticky='nesw', padx=5, pady=5)
        #             self.output_widgets["info"].grid(
        #                 column=0, columnspan=2,
        #                 row=0, rowspan=3,
        #                 sticky='nesw', padx=5, pady=5
        #             )
        #             self.info_toggle = not self.info_toggle
        #         else:
        #             self.output_widgets["info"].grid_forget()
        #             self.output.grid_forget()
        #             self.info_toggle = not self.info_toggle
        #         pass
        #     case "add_to_bl":
        #         print(self.selected_device)
        #         result = self.systems.add_to_blacklist(self.selected_device)
        #         device_list = self.output_widgets["device_list"]
        #         if result:
        #             device_list.selection_clear(0, 'end')
        #             device_list.itemconfigure(
        #                 self.selected_index,
        #                 bg=self.win_bg,
        #                 foreground='white')
        #             self.disable_device_options()
        #     case "remove_from_bl":
        #         print(self.selected_device)
        #         result = self.systems.remove_from_blacklist(self.selected_device)
        #         device_list = self.output_widgets["device_list"]
        #         if result:
        #             device_list.selection_clear(0, 'end')
        #             device_list.itemconfigure(
        #                 self.selected_index,
        #                 bg='white',
        #                 foreground=self.win_bg)
        #             self.disable_device_options()
        #     case "profile":
        #         pass
        #     case "settings":
        #         pass
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
        #     case "toggle_output":
        #         print("Toggling Output")
        #         if self.footer.get_widget("toggle_output").cget("text") == "open":
        #             self.output.grid_forget()
        #             self.footer.get_widget("toggle_output")["text"] = "closed"
        #             toggle_output_icon = PhotoImage(file=preset.expand_button)
        #             self.footer.get_widget("toggle_output")["image"] = toggle_output_icon
        #             self.footer.get_widget("toggle_output").image = toggle_output_icon
        #         else:
        #             self.output.grid(column=1, row=0, rowspan=3, sticky='nesw', padx=5, pady=5)
        #             toggle_output_icon = PhotoImage(file=preset.collapse_button)
        #             self.footer.get_widget("toggle_output")["image"] = toggle_output_icon
        #             self.footer.get_widget("toggle_output").image = toggle_output_icon
        #             self.footer.get_widget("toggle_output")["text"] = "open"

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

    def scan_thread(self):
        self.systems.scan()
        self.output_widgets["scan_progress"].stop()
        self.body_widgets["scan"]["button"]["state"] = "normal"
        self.footer_widgets["exit"]["state"] = "normal"
        messagebox.showinfo(self.win.version, "Scan Complete")
        self.output_widgets["scan_progress"].grid_forget()
        self.display_summary()

    def display_summary(self):
        self.host.set(self.systems.host["name"])
        device_names = [device["name"] for device in self.systems.devices]
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

    def display_device_options(self, *args):
        device_names = [device["name"] for device in self.systems.devices]
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
