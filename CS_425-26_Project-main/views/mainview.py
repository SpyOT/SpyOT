from tkinter import ttk, PhotoImage, messagebox, Listbox, StringVar, filedialog
import threading
from gui import constants as preset
from .frames import *
from ..widgets import *

is_guest = 0


class MainView:
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

        self.alert_widgets = {}
        self.set_widgets()
        self.thread = None
        self.display_win()

    def set_widgets(self):
        widget_bg = self.frame_bg
        """ Header widgets"""
        profile_icon = PhotoImage(file=preset.profile_path)

        self.header.set_widget("profile", CustomButton,
                               image=profile_icon,
                               bg=widget_bg,
                               command=lambda: self.handle_btn_press("profile"))
        title_icon = PhotoImage(file=preset.title_path)
        self.header.set_widget("title", CustomLabel,
                               image=title_icon,
                               bg=widget_bg,
                               )
        self.header.get_widget("title").bind("<Button-1>", lambda event: self.handle_btn_press('set_admin'))
        self.header.get_widget("title").bind("<Button-3>", lambda event: self.handle_btn_press('set_guest'))
        settings_icon = PhotoImage(file=preset.setting_path)
        self.header.set_widget("settings", CustomButton,  # This is the widget for the gear icon
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

        self.output.set_widget("loading", CustomLabel,
                               text="Loading...",
                               foreground=self.text_color,
                               bg=widget_bg)
        # Header output widgets
        toggle_dark_and_light_mode = PhotoImage(file=preset.dark_mode)
        self.output.set_widget("dark and light mode", CustomButton,
                               image=toggle_dark_and_light_mode,
                               bg=widget_bg,
                               command=lambda: self.handle_btn_press(
                                   "toggle dark and light mode"))  # widget_bg is a default green color we use

        # Scan output widgets
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
                               command=lambda: self.handle_btn_press("new_scan"))

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

        # Collect output widgets
        self.output.set_widget("summary", CustomLabel,
                               text="Summary",
                               foreground=self.text_color,
                               bg=widget_bg)

        self.output.set_widget("device_summary", ttk.Treeview,
                               columns='status')
        self.output.get_widget("device_summary").heading('status', text='Status')

        self.output.set_widget("edit", CustomButton,
                               text="Edit List",
                               bg=self.button_bg,
                               command=lambda: self.handle_btn_press("scan"))

        self.output.set_widget("view", CustomButton,
                               text="View Reports",
                               bg=self.button_bg,
                               command=lambda: self.handle_btn_press("view"))

        self.output.set_widget("save", CustomButton,
                               text="Save Report",
                               bg=self.button_bg,
                               command=lambda: self.handle_btn_press("save"))

        # Upload output widgets
        self.output.set_widget("login", CustomButton,
                               text="Login",
                               bg=self.button_bg,
                               command=lambda: self.handle_btn_press("login"))

        self.output.set_widget("sign_up", CustomLabel,
                               text="Create an account at https://spyot.github.io/SpyOT/",
                               wraplength=200,
                               foreground=self.text_color,
                               bg=widget_bg)

        self.output.set_widget("info", CustomLabel,
                               text=preset.about_text,
                               bg=widget_bg,
                               foreground=self.text_color)

    def display_win(self):
        self.container.grid(column=0, row=0, sticky='n e s w')
        self.header.display_frame(column=0, row=0, sticky='n e s w', padx=5, pady=5)
        self.body.display_frame(column=0, row=1, sticky='n e s w', padx=5, pady=5)
        self.footer.display_frame(column=0, row=2, sticky='n e s w', padx=5, pady=5)

    def handle_btn_press(self, option):  # Grabbing button command
        global is_guest
        if not self.is_prod:
            print("clicked on", option, "button")  # Debugging purposes

        match option:
            # Header Buttons
            case "profile":
                if is_guest:
                    self.output.display_action(
                        'guest',
                        column=1, row=0,
                        rowspan=3, sticky='n e s w',
                        padx=5, pady=5)
            case "set_admin":
                is_guest = 0
            case "set_guest":
                is_guest = 1
            case "settings":  # (Start) Behavior of when you click the gear icon
                self.output.display_action(option,
                                           column=1, row=0,
                                           rowspan=3, sticky='n e s w',
                                           padx=5, pady=5)
                pass
            case "toggle dark and light mode":
                # Handles light/dark mode behavior
                if self.dark_light_mode:
                    self.frame_bg = "#d3d3d3"
                    lm_frame_clr = "#d3d3d3"
                    lm_background_clr = "#a9a9a9"
                    self.container.edit_window_background_color(lm_background_clr)
                    self.header.edit_frame_background_color(lm_frame_clr)
                    self.dark_light_mode = False
                else:
                    self.frame_bg = "#3b3b3b"
                    dm_frame_clr = "#3b3b3b"
                    dm_background_clr = "#0c131e"
                    self.container.edit_window_background_color(dm_background_clr)
                    self.header.edit_frame_background_color(dm_frame_clr)
                    self.dark_light_mode = True

                pass
            # Body Buttons
            case "new_scan":
                self.handle_action('scan')
            case "scan":
                if self.handle_output(option):
                    """ Widgets updated, display widgets"""
                    self.output.display_action(  # Grabs widget output specific to command
                        option,
                        column=1, row=0,
                        rowspan=3, sticky='n e s w',
                        padx=5, pady=5)
                else:
                    """ Running scan on network """
                    self.handle_action(option)
            case "collect":
                if self.handle_output(option):
                    """ Widgets updated, display widgets"""
                    self.output.display_action(
                        option,
                        column=1, row=0,
                        rowspan=3, sticky='n e s w',
                        padx=5, pady=5)
                else:
                    """ Running scan on network """
                    self.handle_action(option)
            case "view":
                local_storage_path = self.systems.get_local_path()
                open_path = filedialog.askopenfilename(
                    initialdir=local_storage_path,
                    defaultextension='.txt', filetypes=[("Text files", "*.txt")])
                self.systems.open_analysis_report(open_path)
            case "save":
                local_storage_path = self.systems.get_local_path()
                save_path = filedialog.asksaveasfilename(
                    initialdir=local_storage_path,
                    defaultextension='.txt', filetypes=[("Text files", "*.txt")])
                self.systems.save_analysis_report(save_path)
            case "upload":
                if is_guest:
                    self.output.display_action(
                        'guest',
                        column=1, row=0,
                        rowspan=3, sticky='n e s w',
                        padx=5, pady=5)
                elif self.systems.upload_success:
                    pass
                else:
                    self.handle_action(option)

            # Footer Buttons
            case "info":
                self.output.set_view(option)
                self.output.toggle_frame(
                    column=1, row=0,
                    rowspan=3,
                    sticky='n e s w',
                    padx=5, pady=5)
            case "toggle_output":
                self.output.toggle_frame(
                    column=1, row=0,
                    rowspan=3,
                    sticky='n e s w',
                    padx=5, pady=5)
            # Output Buttons
            case "blacklist":
                selected_device = self.get_selected_device()
                selected_index = self.output.get_selected_index()
                # result = self.systems.add_to_blacklist(selected_device)
                result = self.systems.update_blacklist('add', selected_device)
                if result:
                    self.output.update_selected_device(selected_index,
                                                       bg=self.win_bg,
                                                       foreground='white')
                self.update_scan_buttons()
            case "whitelist":
                selected_device = self.get_selected_device()
                selected_index = self.output.get_selected_index()
                # result = self.systems.remove_from_blacklist(selected_device)
                result = self.systems.update_blacklist('remove', selected_device)
                if result:
                    self.output.update_selected_device(selected_index,
                                                       bg='white',
                                                       foreground=self.win_bg)
                self.update_scan_buttons()
        self.update_footer_toggle()
        self.update_dark_light_mode_toggle()

    def handle_action(self, action):
        print("!Running {}".format(action))
        self.toggle_buttons()
        self.output.display_action(
            'run_action',
            column=1, row=0,
            rowspan=3, sticky='n e s w',
            padx=5, pady=5)
        self.thread = threading.Thread(target=lambda: self.action_thread(action)).start()

    def handle_output(self, action):  # You don't need a handle output for 'settings'
        """ Get action result and update output widgets """
        print("!Updating {} output widgets".format(action))
        match action:
            case "scan":
                host_name = self.systems.get_hostname()
                device_names = self.systems.get_device_names()
                print(1, host_name, 2, device_names)
                if host_name and device_names:
                    self.output.update_var('host_name', host_name)
                    self.output.update_var('devices', device_names)
                    return True
                else:
                    return False
            case "collect":
                port_output = self.systems.get_port_output()
                if port_output:
                    device_analysis = self.systems.device_analysis(port_output)
                    device_summary = self.systems.device_summary(device_analysis)
                    table = self.output.get_widget("device_summary")
                    rows = table.get_children()
                    if rows:
                        for row in rows:
                            table.delete(row)
                    for i, data in enumerate(device_summary):
                        device = device_summary[data]
                        table.insert('', 'end', text=device['name'], values=(device['status']))
                    table.column('status', width=100)
                    return True
                else:
                    return False
            case "upload":
                pass

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

    # Header utils
    # Profile image
    def update_profile_background(self):
        state = True

        if state:
            profile_icon = PhotoImage(file=preset.profile_path)
        else:
            profile_icon = PhotoImage(file=preset.profile_path)

        self.header.update_widget_value(
            "profile",
            "background", self.frame_bg)

        active_background = ""
        if self.dark_light_mode:
            active_background = "#a9a9a9"
            self.header.update_widget_value(
                "profile",
                "activebackground", active_background)

        self.header.update_widget_value(
            "profile",
            "image", profile_icon)

    # SpyOT title
    def update_title_background(self):
        state = True

        if state:
            title_icon = PhotoImage(file=preset.title_path)
        else:
            title_icon = PhotoImage(file=preset.title_path)

        self.header.update_widget_value(
            "title",
            "background", self.frame_bg)

        active_background = ""
        if self.dark_light_mode:
            active_background = "#a9a9a9"
            self.header.update_widget_value(
                "title",
                "activebackground", active_background)

        self.header.update_widget_value(
            "title",
            "image", title_icon)

    # Settings button
    def update_settings_background(self):
        state = True

        if state:
            settings_icon = PhotoImage(file=preset.setting_path)
        else:
            settings_icon = PhotoImage(file=preset.setting_path)

        self.header.update_widget_value(
            "settings",
            "background", self.frame_bg)

        active_background = ""
        if self.dark_light_mode:
            active_background = "#a9a9a9"
            self.header.update_widget_value(
                "settings",
                "activebackground", active_background)

        self.header.update_widget_value(
            "settings",
            "image", settings_icon)

    # Dark and light mode
    def update_dark_light_mode_toggle(self):
        state = self.dark_light_mode

        if state:  # Dark mode
            toggle_icon = PhotoImage(file=preset.dark_mode)
        else:  # Light mode
            toggle_icon = PhotoImage(file=preset.light_mode)

        self.output.update_widget_value(
            "dark and light mode",
            "background", self.frame_bg)

        self.output.update_widget_value(
            "dark and light mode",
            "image", toggle_icon)

        # All the changed images here:
        self.update_profile_background()
        self.update_title_background()
        self.update_settings_background()
        self.update_scan_label_background()
        self.update_scan_button_background()
        self.update_collect_label_background()
        self.update_collect_button_background()
        self.update_upload_label_background()
        self.update_upload_button_background()
        self.update_info_background()
        self.update_info_text_background()

    # Body utils
    # Side buttons
    def update_scan_label_background(self):
        state = True

        if state:
            scan_icon = PhotoImage(file=preset.scan_path)
        else:
            scan_icon = PhotoImage(file=preset.scan_path)

        self.body.update_widget_value(
            "scan_label",
            "background", self.frame_bg)

        active_background = ""
        if self.dark_light_mode:
            active_background = "#a9a9a9"
            self.body.update_widget_value(
                "scan_label",
                "activebackground", active_background)

        self.body.update_widget_value(
            "scan_label",
            "image", scan_icon)

    def update_scan_button_background(self):
        state = True

        if state:
            scan_icon = PhotoImage(file=preset.scan_button)
        else:
            scan_icon = PhotoImage(file=preset.scan_button)

        self.body.update_widget_value(
            "scan_button",
            "background", self.frame_bg)

        active_background = ""
        if self.dark_light_mode:
            active_background = "#a9a9a9"
            self.body.update_widget_value(
                "scan_button",
                "activebackground", active_background)

        self.body.update_widget_value(
            "scan_button",
            "image", scan_icon)

    def update_collect_label_background(self):
        state = True

        if state:
            collect_icon = PhotoImage(file=preset.collect_path)
        else:
            collect_icon = PhotoImage(file=preset.collect_path)

        self.body.update_widget_value(
            "collect_label",
            "background", self.frame_bg)

        active_background = ""
        if self.dark_light_mode:
            active_background = "#a9a9a9"
            self.body.update_widget_value(
                "collect_label",
                "activebackground", active_background)

        self.body.update_widget_value(
            "collect_label",
            "image", collect_icon)

    def update_collect_button_background(self):
        state = True

        if state:
            collect_icon = PhotoImage(file=preset.collect_button)
        else:
            collect_icon = PhotoImage(file=preset.collect_button)

        self.body.update_widget_value(
            "collect_button",
            "background", self.frame_bg)

        active_background = ""
        if self.dark_light_mode:
            active_background = "#a9a9a9"
            self.body.update_widget_value(
                "collect_button",
                "activebackground", active_background)

        self.body.update_widget_value(
            "collect_button",
            "image", collect_icon)

    def update_upload_label_background(self):
        state = True

        if state:
            upload_icon = PhotoImage(file=preset.upload_path)
        else:
            upload_icon = PhotoImage(file=preset.upload_path)

        self.body.update_widget_value(
            "upload_label",
            "background", self.frame_bg)

        active_background = ""
        if self.dark_light_mode:
            active_background = "#a9a9a9"
            self.body.update_widget_value(
                "upload_label",
                "activebackground", active_background)

        self.body.update_widget_value(
            "upload_label",
            "image", upload_icon)

    def update_upload_button_background(self):
        state = True

        if state:
            upload_icon = PhotoImage(file=preset.upload_button)
        else:
            upload_icon = PhotoImage(file=preset.upload_button)

        self.body.update_widget_value(
            "upload_button",
            "background", self.frame_bg)

        active_background = ""
        if self.dark_light_mode:
            active_background = "#a9a9a9"
            self.body.update_widget_value(
                "upload_button",
                "activebackground", active_background)

        self.body.update_widget_value(
            "upload_button",
            "image", upload_icon)

    def update_info_background(self):
        state = True

        if state:
            info_icon = PhotoImage(file=preset.info_path)
        else:
            info_icon = PhotoImage(file=preset.info_path)

        self.footer.update_widget_value(
            "info",
            "background", self.frame_bg)

        active_background = ""
        if self.dark_light_mode:
            active_background = "#a9a9a9"
            self.footer.update_widget_value(
                "info",
                "activebackground", active_background)

        self.footer.update_widget_value(
            "info",
            "image", info_icon)

    # Footers utils

    # Collapsing arrow
    def update_footer_toggle(self):
        state = self.output.get_state()

        if state:
            toggle_icon = PhotoImage(file=preset.collapse_button)
        else:
            toggle_icon = PhotoImage(file=preset.expand_button)

        self.footer.update_widget_value(
            "toggle_output",
            "background", self.frame_bg)

        active_background = ""
        if self.dark_light_mode:
            active_background = "#a9a9a9"
            self.footer.update_widget_value(
                "toggle_output",
                "activebackground", active_background)

        self.footer.update_widget_value(
            "toggle_output",
            "image", toggle_icon)

    # Output utils
    #  About section

    def update_info_text_background(self):
        black_text = "#000000"
        self.output.update_widget_value(
            "info",
            "background", self.frame_bg)

        self.output.update_widget_value(
            "info",
            "foreground", black_text)

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

    def action_thread(self, action):
        print("!Starting {} thread".format(action))
        result = 0
        match action:
            case "scan":
                result = self.systems.scan()
            case "collect":
                result = self.systems.collect()
            case "upload":
                result = self.systems.upload()
        self.output.display_action(
            'stop_action',
            column=1, row=0,
            rowspan=3, sticky='n e s w',
            padx=5, pady=5)
        self.toggle_buttons()
        if result:
            messagebox.showinfo(self.win.version, "{} Complete".format(action.capitalize()))
            self.handle_btn_press(action)
        else:
            messagebox.showerror(self.win.version, "!Error: {} not successful".format(action.capitalize()))

    def update_scan_buttons(self, *args):
        _ = args
        selected_device_name = self.get_selected_device()
        blacklist = self.systems.get_blacklist()
        if not selected_device_name:
            self.output.disable_button("blacklist", bg=self.frame_bg)
            self.output.disable_button("whitelist", bg=self.frame_bg)
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
