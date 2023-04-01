from tkinter import Frame


class CustomFrame(Frame):
    def __init__(self, frame, **kwargs):
        super().__init__(
            frame,
            bd=0,
            highlightthickness=0,
            relief="ridge",
            **kwargs
        )
