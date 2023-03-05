from tkinter import Tk
from app import App
from systems import Network


class SpyOT(Tk):
    def __init__(self, version="SpyOT"):
        print("Welcome to SpyOT! The IoT Security System.")
        super().__init__()
        self.version = version
        self.title(self.version)
        self.network = Network()
        self.app = App(self)


def main():
    root = SpyOT("DEMO")
    root.mainloop()


if __name__ == '__main__':
    main()
