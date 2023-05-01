from .frame import CustomContainer


class CustomFooter(CustomContainer):
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

    def display_widgets(self):
        self.display_widget("info",
                            column=0, row=0,
                            padx=15, pady=15,
                            sticky='w')
        self.display_widget("toggle_output",
                            column=1, row=0,
                            padx=15, pady=15,
                            sticky='e')