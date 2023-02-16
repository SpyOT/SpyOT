from .networkscanner import NetworkScanner
from .db_api import MongoAPI

class NetworkManager:
    def __init__(self):
        self.title = "Network"
        self.user_choice = None
        self.options = {0:{"isAvailable":True, "output":"Return to Main Menu"},
                        1:{"isAvailable":True, "output":"Run Network Scanner"}}
        self.db = MongoAPI("user_network")
        self.scanner = NetworkScanner()
        self.metadata = None
        self.isSetup = False
        self.setup()

    def setup(self):
        print(self.title)

        print("Options")
        for opt in self.options:
            if self.options[opt]["isAvailable"]:
                print(str(opt) + ":", self.options[opt]["output"])

        self.user_choice = int(input("Input: "))
        print()
        match self.user_choice:
            case 0:
                print("Exiting Setup")
            case 1:
                self.scanner.networkScanner()
                self.metadata = self.scanner.device_list
                self.db_setup()
                self.isSetup = True

    def db_setup(self):
        self.db.create_collection("user_devices")
        self.db.insert_into_collection("user_devices", self.metadata)

    def network_summary(self):
        print()
        print("Detected Network")
        print(self.metadata)
        print("Returning to Main Menu")
        print()

