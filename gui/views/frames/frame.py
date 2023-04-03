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
            self,
            **kwargs
        )
        if 'image' in kwargs:
            self.widgets[name].image = kwargs['image']

    def update_widget_value(self, name, val, new_val):
        self.widgets[name][val] = new_val
        if val == 'image':
            self.widgets[name].image = new_val

    def get_widgets(self):
        return self.widgets

    def get_widget(self, name):
        return self.widgets[name]

    def display_widget(self, name, **kwargs):
        self.widgets[name].grid(
            **kwargs
        )

    def display_widgets(self):
        pass

    def display_frame(self, **kwargs):
        self.grid(**kwargs)
        self.display_widgets()

    def remove_frame(self):
        self.grid_forget()

    def reset_frame(self):
        for widget in self.widgets:
            self.widgets[widget].grid_forget()

    def disable_button(self, name, **kwargs):
        self.get_widget(name)["state"] = "disabled"
        self.get_widget(name).configure(**kwargs)

    def enable_button(self, name, **kwargs):
        self.get_widget(name)["state"] = "normal"
        self.get_widget(name).configure(**kwargs)