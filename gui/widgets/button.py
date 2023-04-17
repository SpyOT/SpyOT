from tkinter import ttk, Button


class CustomButton(ttk.Button):
    def __init__(self, frame, **kwargs):
        super().__init__(
            frame,
            **kwargs
        )