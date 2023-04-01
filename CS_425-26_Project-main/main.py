from tkinter import Tk
import src

"""
sources:
https://tkdocs.com/tutorial/index.html
https://tkdocs.com/widgets/
https://www.pythontutorial.net/tkinter/tkinter-grid/
"""


class SpyOT(Tk):
    def __init__(self, version="v1", env="dev"):
        print("Welcome to SpyOT! The IoT Security System.")
        super().__init__()
        self.version = version
        self.APP_ENV = env
        self.title('-'.join(["SpyOT", self.version]))
        self.network = src.Network()
        self.app = src.App(self)


class TestMain:
    def __init__(self):
        self.app = SpyOT("UnitTest")
        # Update to match new project directories and class names
        # self.frontend = self.app.frontend
        # self.curr_scene = self.frontend.scene
        self.app.mainloop()


def main():
    # test = TestMain()
    root = SpyOT(version="DEMO", env="")
    root.mainloop()


if __name__ == '__main__':
    main()
