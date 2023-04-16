from tkinter import Button


class CustomButton(Button):
    def __init__(self, frame, **kwargs):
        super().__init__(
            frame,
            activebackground=frame.style.lookup('MyFrame.TFrame', 'background'),
            bd=0,
            highlightthickness=0,
            relief="solid",
            **kwargs
        )