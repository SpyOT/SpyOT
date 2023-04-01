from tkinter import Tk
import os
import sys
import src
from dotenv import load_dotenv

"""
sources:
https://tkdocs.com/tutorial/index.html
https://tkdocs.com/widgets/
https://www.pythontutorial.net/tkinter/tkinter-grid/
"""

load_dotenv()


class SpyOT(Tk):
    def __init__(self, version="SpyOT"):
        print("Welcome to SpyOT! The IoT Security System.")
        super().__init__()
        self.version = version
        self.env = os.getenv('APP_ENV')
        self.is_prod = self.env == "prod"
        self.title(self.version)
        self.network = src.Network()
        self.app = src.App(self)


class TestMain:
    def __init__(self):
        self.app = SpyOT("UnitTest")
        self.frontend = self.app.frontend
        self.curr_scene = self.frontend.scene
        self.app.mainloop()


def main():
    # test = TestMain()
    root = SpyOT()
    root.mainloop()


if __name__ == '__main__':
    main()
