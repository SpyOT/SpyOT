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
