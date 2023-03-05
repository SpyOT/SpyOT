from networkscanner import NetworkScanner
from db_api import MongoAPI


class Network:
    def __init__(self):
        self.db = MongoAPI("user_network")
        self.metadata = None
        self.scanner = NetworkScanner()
        self.isSetup = self.db.is_db_setup()
        self.device_count = 0

    def scan(self):
        print("starting scan")
        self.scanner.networkScanner()
        self.metadata = self.scanner.device_list
        print("scan complete")

    def collect(self):
        pass

    def upload(self):
        print("starting upload")
        try:
            self.db_setup()
        except:
            print("error in upload")
        print("upload complete")

    def db_setup(self):
        self.db.create_collection("user_devices")
        entry = self.create_collection_entry(self.metadata["host"], self.metadata["devices"])
        self.db.insert_into_collection("user_devices", entry)
        self.isSetup = self.db.is_db_setup()

    def create_collection_entry(self, host, device_list):
        host_id = "U1IT" + str(self.device_count)
        self.device_count += 1
        host_name, host_ip = host[0], host[2][0]
        devices = {}
        for i, device in enumerate(device_list):
            device_id = "U1IT" + str(self.device_count)
            self.device_count += 1
            devices[device[0]] = {
                "_id": device_id,
                "ip": device[2][0]
            }
        entry = {
            "_id": host_id,
            "host_name": host_name,
            "host_ip": host_ip,
            "devices": devices
        }
        return entry

    def can_upload(self):
        return self.metadata is not None
