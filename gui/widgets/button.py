from tkinter import Button


class CustomButton(Button):
    def __init__(self, frame=None, text="temp", **kwargs):
        super().__init__(
            frame,
            text=text,
            activebackground="white",
            bd=0,
            highlightthickness=0,
            relief="solid",
            **kwargs
        )
        pass
