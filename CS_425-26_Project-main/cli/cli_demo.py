import states
from systems.profilemanager import ProfileManager


class SpyOT:
    def __init__(self):
        print("Welcome to SpyOT! The IoT Security System.")
        self.state = states.MainMenu()

    def loop(self):
        self.state.loop()

def main():
    root = SpyOT()
    root.loop()


if __name__ == '__main__':
    main()
