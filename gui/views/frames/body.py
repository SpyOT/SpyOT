from .frame import CustomContainer


class CustomBody(CustomContainer):
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
        self.actions = {}

    def set_actions(self, action, label_widget, button_widget):
        self.actions[action] = {"label": label_widget, "button": button_widget}

    def get_actions(self):
        return self.actions

    def display_widgets(self):
        for i, action in enumerate(self.actions):
            self.actions[action]["label"].grid(
                column=0, row=i,
                padx=15, pady=15
            )
            self.actions[action]["button"].grid(
                column=1, row=i,
                padx=15, pady=15
            )
