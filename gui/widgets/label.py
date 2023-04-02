from tkinter import Label


class CustomLabel(Label):
    def __init__(self, frame, **kwargs):
        super().__init__(
            frame,
            activebackground="white",
            bd=0,
            highlightthickness=0,
            relief="solid",
            **kwargs
        )
