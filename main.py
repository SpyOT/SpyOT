from gui import App
from systems import Systems
from tkinter import Tk, PhotoImage
import gui.constants as preset
from sys import argv

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

    def __init__(self, version, env):
        super().__init__()
        print("Welcome to SpyOT! The IoT Network Monitoring System.")
        self.version = "SpyOT - " + version
        self.env = env
        self.systems = Systems(self.env)
        self.app = App(self, self.systems, self.title, self.env)
        self.configure_app()

    def configure_app(self):
        self.title(self.version)
        logo = PhotoImage(file=preset.logo_img)
        self.iconphoto(False, logo)
        self.configure(bg=App.WIN_BG)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


class TestMain:
    def __init__(self):
        # TODO: Redo this test using new project structure
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
    # env passed in format : --env=dev
    version, env = "DEMO", "dev"
    for arg in argv:
        if "--version" in arg:
            version = arg.split("=")[1]
        elif "--env" in arg:
            env = arg.split("=")[1]

    # test = TestMain()
    root = SpyOT(version=version, env=env)
    root.mainloop()


if __name__ == '__main__':
    main()
