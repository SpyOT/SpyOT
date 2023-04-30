from tkinter import ttk


class CustomContainer(ttk.Frame):
    def __init__(self, frame, systems, **kwargs):
        super().__init__(
            frame,
            **kwargs
        )
        self.widgets = {}
        self.systems = systems

    def configure_win(self, col_config, row_config):
        """
        :param col_config: { 'col x' : 'weight y' }
        :param row_config: { 'row x' : 'weight y' }
        """
        for col in col_config:
            col_val = int(col.split(' ')[1])
            weight_val = int(col_config[col].split(' ')[1])
            self.columnconfigure(col_val, weight=weight_val)
        for row in row_config:
            row_val = int(row.split(' ')[1])
            weight_val = int(row_config[row].split(' ')[1])
            self.rowconfigure(row_val, weight=weight_val)

    def set_widget(self, name, widget_type, **kwargs):
        self.widgets[name] = widget_type(
            self,
            **kwargs
        )
        if 'image' in kwargs:
            self.widgets[name].image = kwargs['image']

    # Override this method in child classes
    def set_widgets(self, controller):
        pass

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

    def is_hidden(self):
        return self.grid_slaves() == []
