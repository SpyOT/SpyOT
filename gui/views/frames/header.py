from .frame import CustomContainer


class CustomHeader(CustomContainer):
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
        for i, name in enumerate(self.widgets):
            self.display_widget(
                name,
                column=i, row=0,
                padx=15, pady=15
            )
    def edit_frame_background_color(self, secondary):
        self.style.configure(
            "MyFrame.TFrame",
            background=secondary)
        pass
