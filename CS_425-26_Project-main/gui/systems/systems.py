from systems.networkscanner import NetworkScanner
from systems.db_api import MongoAPI
from os import listdir
from os.path import isfile, join


class Network:
    def __init__(self):
        self.db = MongoAPI("user_network")
        self.metadata = None
        self.scanner = NetworkScanner()
        self.isSetup = self.db.is_db_setup()
        self.device_count = 0
        self.devices = []
        self.device_ips = []
        self.host = {"name": "", "ip": ""}

    def add_local_scan(self):
        local_dir = open("systems/local_scans/scan01", "w")
        scan_entry = list()
        scan_entry.append(' '.join(["host", self.host["name"], self.host["ip"] + '\n']))
        for device in self.devices:
            scan_entry.append(' '.join(["devices", device["name"], device["ip"] + '\n']))
        local_dir.writelines(scan_entry)
        local_dir.close()

    def scan(self):
        print("starting scan")
        self.scanner.networkScanner()
        self.metadata = self.scanner.device_list
        self.collect()
        self.add_local_scan()
        print("scan complete")

    def collect(self, blacklist=()):
        print("collecting data")
        # encrypt host IP here
        self.host = {"name": self.metadata["host"][0], "ip": self.metadata["host"][-1][0]}
        for device in self.metadata["devices"]:
            print(device)
            if device[0] not in blacklist and device[-1][0] not in self.device_ips:
                # encrypt device IP here
                self.devices.append({"name": device[0], "ip": device[-1][0]})
                self.device_ips.append(device[-1][0])
        print("collection complete")

    def upload(self):
        print("starting upload")
        try:
            self.db_setup()
            print("upload complete")
            return True
        except:
            print("incomplete upload")
            return False

    def db_setup(self):
        self.db.create_collection("user_devices")
        entry = self.create_collection_entry(self.host, self.devices)
        self.db.insert_into_collection("user_devices", entry)
        self.isSetup = self.db.is_db_setup()

    def create_collection_entry(self, host, device_list):
        host_id = "U1IT" + str(self.device_count)
        self.device_count += 1
        host_name, host_ip = host["name"], host["ip"]
        devices = {}

        for i, device in enumerate(device_list):
            device_id = "U1IT" + str(self.device_count)
            self.device_count += 1
            devices[device_id] = device

        entry = {
            "_id": host_id,
            "host_name": host_name,
            "host_ip": host_ip,
            "devices": devices
        }
        return entry

    def can_upload(self):
        local_scans_path = 'systems/local_scans'
        local_scans = [join(local_scans_path, f) for f in listdir(local_scans_path) if
                       isfile(join(local_scans_path, f))][0]
        if self.metadata:
            return True
        elif local_scans:
            self.metadata = {}
            with open(local_scans) as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip().split()
                    entry_type, entry_name, entry_ip = line
                    if entry_type not in self.metadata:
                        if entry_type == 'host':
                            self.metadata[entry_type] = [entry_name, [entry_ip]]
                        else:
                            self.metadata[entry_type] = [[entry_name, [entry_ip]]]
                    else:
                        self.metadata[entry_type].append([entry_name, [entry_ip]])
            return True
        return False
