from .frame import CustomContainer


class CustomOutput(CustomContainer):
    def __init__(self, frame, background, col_config, row_config, **kwargs):
        super().__init__(
            frame,
            frame.style.lookup("MyContainer.TFrame", "background"),
            col_config,
            row_config,
            **kwargs
        )
        self.style.configure(
            "MyFrame.TFrame",
            background=background,
        )
        self.config(style="MyFrame.TFrame")
        self.widgets = {}
        self.view = ""
        self.state = 0
        self.vars = {}

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def toggle_state(self):
        self.state = not self.state

    def set_view(self, view):
        self.reset_frame()
        self.view = view

    def toggle_frame(self, **kwargs):
        if self.state:
            self.remove_frame()
        else:
            self.display_frame(**kwargs)
        self.toggle_state()

    def display_widgets(self):
        match self.view:
            case "info":
                self.display_widget("info",
                                    column=0, columnspan=2,
                                    row=0, rowspan=3,
                                    sticky='nesw', padx=5, pady=5)
            case "run_action":
                self.display_widget("progress_bar",
                                    column=0, columnspan=2,
                                    row=1,
                                    padx=10, pady=10,
                                    sticky='ew')
                self.display_widget("loading",
                                    column=0, columnspan=2,
                                    row=1,
                                    padx=10, pady=10,
                                    sticky='ews')
                self.get_widget("progress_bar").start(5)
            case "stop_action":
                self.get_widget("progress_bar").stop()
                self.reset_frame()
            case "scan":
                self.display_widget("host_label",
                                    column=0, row=0,
                                    padx=5, pady=5,
                                    sticky='s')
                self.display_widget("host_name",
                                    column=1, row=0,
                                    padx=5, pady=5,
                                    sticky='s')
                self.display_widget("devices",
                                    column=0, columnspan=2,
                                    row=1, padx=5, pady=5,
                                    sticky='nesw')
                self.display_widget("new_scan",
                                    column=0, row=2,
                                    rowspan=2,
                                    padx=5,pady=5,
                                    sticky='ew'
                                    )
                self.display_widget("blacklist",
                                    column=1, row=2,
                                    padx=5, pady=5,
                                    sticky='nesw')
                self.display_widget("whitelist",
                                    column=1, row=3,
                                    padx=5, pady=5,
                                    sticky='nesw')
            case "collect":
                self.display_widget("summary",
                                    column=0, columnspan=2,
                                    row=0, padx=5, pady=5,
                                    sticky='nesw')
                self.display_widget("device_summary",
                                    column=0, columnspan=2,
                                    row=1, padx=5, pady=5,
                                    sticky='ns')
                self.display_widget("edit",
                                    column=0, row=2, rowspan=2,
                                    padx=5, pady=5,
                                    sticky='ew')
                self.display_widget("view",
                                    column=1, row=2,
                                    padx=5, pady=5,
                                    sticky='ew')
                self.display_widget("save",
                                    column=1, row=3,
                                    padx=5, pady=5,
                                    sticky='ew')
            case "upload":
                pass
            case "":
                self.remove_frame()

    def display_action(self, view, **kwargs):
        self.set_view(view)
        self.display_frame(**kwargs)

    def get_selected_index(self):
        return self.get_widget("devices").curselection()[0]

    def update_selected_device(self, index, **kwargs):
        self.get_widget("devices").itemconfigure(
            index,
            **kwargs
        )
        self.get_widget("devices").selection_clear(0, 'end')

    def update_var(self, name, value):
        self.vars[name].set(value)