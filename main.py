from gui import App
from systems import Systems
from tkinter import Tk, PhotoImage
from sys import argv
from gui.constants import LOGO_PATH, WIN_BG

"""
sources:
https://tkdocs.com/tutorial/index.html
https://tkdocs.com/widgets/
https://www.pythontutorial.net/tkinter/tkinter-grid/
"""


class SpyOT(Tk):
    """
    MVC Architecture
    Model: Systems
    Views: MainView, OutputView
    Controller: App
    """

    def __init__(self, version):
        super().__init__()
        print("Welcome to SpyOT! The IoT Network Monitoring System.")
        self.version = "SpyOT - " + version
        self.systems = Systems()
        self.app = App(self, self.systems, self.title)
        self.configure_app()

    def configure_app(self):
        self.title(self.version)
        logo = PhotoImage(file=LOGO_PATH)
        self.iconphoto(False, logo)
        self.configure(bg=WIN_BG)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


class TestMain:
    def __init__(self):
        # self.app = SpyOT("UnitTest")
        # Update to match new project directories and class names
        # self.frontend = self.app.frontend
        # self.curr_scene = self.frontend.scene
        # self.app.mainloop()
        pass


def main():
    # Check for version and env args
    # If not passed, use default values of DEMO and dev
    # version passed in format : --version=1.0
    version = "v1"
    for arg in argv:
        if "--version" in arg:
            version = arg.split("=")[1]

    # test = TestMain()
    root = SpyOT(version=version)
    root.mainloop()


if __name__ == '__main__':
    main()
