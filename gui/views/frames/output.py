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

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def toggle_state(self):
        self.state = not self.state

    def set_view(self, view):
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
                self.display_widget(self.view,
                                    column=0, columnspan=2,
                                    row=0, rowspan=3,
                                    sticky='nesw', padx=5, pady=5)
