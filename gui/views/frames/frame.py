from tkinter import ttk


class CustomContainer(ttk.Frame):
    def __init__(self, frame, background, col_config, row_config, **kwargs):
        super().__init__(
            frame,
            **kwargs
        )
        self.style = ttk.Style()
        self.style.configure(
            "MyContainer.TFrame",
            background=background,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.config(style="MyContainer.TFrame")
        self.configure_win(col_config, row_config)
        self.widgets = {}

    def configure_win(self, col_config, row_config):
        # col_config : { col : weight }
        for col in col_config:
            self.columnconfigure(col, weight=col_config[col])
        for row in row_config:
            self.rowconfigure(row, weight=row_config[row])

    def set_widget(self, name, widget_type, **kwargs):
        self.widgets[name] = widget_type(
            frame=self,
            **kwargs
        )
        if 'image' in kwargs:
            self.widgets[name].image = kwargs['image']

    def get_widgets(self):
        return self.widgets

    def get_widget(self, name):
        return self.widgets[name]

    def display_widget(self, name, **kwargs):
        self.widgets[name].grid(
            **kwargs
        )
