from gui import App
from systems import Systems

"""
sources:
https://tkdocs.com/tutorial/index.html
https://tkdocs.com/widgets/
https://www.pythontutorial.net/tkinter/tkinter-grid/
"""


class SpyOT:
    def __init__(self, version="v1", env="dev"):
        print("Welcome to SpyOT! The IoT Security System.")
        self.title = "SpyOT - " + version
        self.env = env
        self.network = Systems()
        self.app = App(self.network, self.title, self.env)

    def mainloop(self):
        self.app.mainloop()


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
