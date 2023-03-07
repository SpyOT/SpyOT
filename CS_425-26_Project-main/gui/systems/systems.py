from systems.network_scanner import NetworkScanner
from systems.db_api import MongoAPI
from os import listdir, mkdir
from os.path import isfile, join


class Network:
    def __init__(self):
        self.db = MongoAPI("user_network")
        self.metadata = None
        self.scanner = NetworkScanner()
        self.device_count = 0
        self.devices = []
        self.device_ips = []
        self.host = {"name": "", "ip": ""}
        self.blacklist_path = 'systems/local/blacklist.text'
        self.upload_devices = []
        self.create_local_storage()

    def create_local_storage(self):
        local_dir = 'systems/local'
        try:
            mkdir(local_dir)
            print("Created local storage")
        except FileExistsError as err:
            print("!Error: Local dir already exists")

        f = open(self.blacklist_path, 'a')
        f.close()
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

    def collect(self):
        print("collecting data")
        # encrypt host IP here
        self.host = {"name": self.metadata["host"][0], "ip": self.metadata["host"][-1][0]}
        for device in self.metadata["devices"]:
            if device[-1][0] not in self.device_ips:
                # encrypt device IP here
                self.devices.append({"name": device[0], "ip": device[-1][0]})
                self.device_ips.append(device[-1][0])
        print("collection complete")

    def upload(self):
        print("starting upload")
        self.update_devices()
        try:
            result = self.db_setup()
            print("upload complete")
            return result
        except:
            print("incomplete upload")
            return False

    def db_setup(self):
        if self.db.test_connection():
            self.db.create_collection("user_devices")
            entry = self.create_collection_entry(self.host, self.upload_devices)
            if not entry:
                return False
            self.db.insert_into_collection("user_devices", entry)
            self.isSetup = self.db.is_db_setup()
            return True
        else:
            print("!Error: Database is not responding")
            return False

    def create_collection_entry(self, host, device_list):
        host_id = "U1IT" + str(self.device_count)
        self.device_count += 1
        host_name, host_ip = host["name"], host["ip"]
        devices = {}
        if not device_list:
            return False

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
        local_scans = []
        if listdir(local_scans_path):
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

    def add_to_blacklist(self, device):
        blacklist = open(self.blacklist_path, 'r')
        lines = blacklist.readlines()
        curr_list = []
        for line in lines:
            if device in line:
                print("!Error: Device already blacklisted")
                return False
            curr_list.append(line)
        print("Adding", device, "to blacklist")
        curr_list.append(device+'\n')
        blacklist.close()
        blacklist = open(self.blacklist_path, 'w')
        blacklist.writelines(curr_list)
        blacklist.close()
        return True

    def remove_from_blacklist(self, device):
        blacklist = open(self.blacklist_path, 'r+')
        curr_devices = blacklist.readlines()
        if device + '\n' not in curr_devices:
            print("Error: Device is not blacklisted")
            return False
        new_devices = [line for line in curr_devices if device not in line]
        blacklist.truncate(0)
        blacklist.seek(0)
        blacklist.writelines(new_devices)
        return True

    def get_blacklist(self):
        device_list = []
        with open(self.blacklist_path) as f:
            lines = f.readlines()
            for line in lines:
                device_list.append(line)
        return device_list

    def update_devices(self):
        blacklist = self.get_blacklist()
        blacklist = [x.strip('\n') for x in blacklist]
        self.upload_devices = []
        for device in self.devices:
            if device["name"] not in blacklist:
                self.upload_devices.append(device)
