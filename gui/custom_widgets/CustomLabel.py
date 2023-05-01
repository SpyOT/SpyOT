from tkinter import ttk, Label


class CustomLabel(ttk.Label):
    def __init__(self, frame, **kwargs):
        super().__init__(
            frame,
            anchor='center',
            **kwargs
        )
