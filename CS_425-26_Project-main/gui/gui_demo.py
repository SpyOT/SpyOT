from tkinter import Tk
from app import App


class SpyOT(Tk):
    def __init__(self, version=""):
        print("Welcome to SpyOT! The IoT Security System.")
        super().__init__()
        self.title(' '.join(["SpyOT", version]))
        self.app = App(self)


def main():
    root = SpyOT("DEMO")
    root.mainloop()


if __name__ == '__main__':
    main()
