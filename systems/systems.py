from .network_scanner import NetworkScanner
from .db_api import MongoAPI
from os import listdir, mkdir, remove, system
from os.path import isfile, join, exists
from cryptography.fernet import Fernet
from SpyOT.systems import constants as preset

key = Fernet.generate_key()
fernet = Fernet(key)


class Systems:
    def __init__(self, env):
        self.env = env
        self.is_prod = self.env == 'prod'
        self.log = not self.is_prod
        self.db = MongoAPI('user_network')
        self.metadata = None
        self.scanner = NetworkScanner()
        self.device_count = 0
        self.devices = []
        self.device_ips = []
        self.host = {'name': '', 'ip': ''}
        self.upload_devices = []
        self.scans = []
        self.create_local_storage()
        self.port_output = {}
        self.upload_success = False

    def create_local_storage(self):
        """ Create a local directory to store scans and blacklist"""
        try:
            mkdir(preset.local_storage_path)
            if not self.is_prod:
                print('Created local storage')
        except FileExistsError as _:
            if not self.is_prod:
                print('!Error: Local dir already exists')

        """ Create a directory for storing scanned metadata locally"""
        try:
            mkdir(preset.scans_path)
        except FileExistsError as _:
            if not self.is_prod:
                print('!Error: Local dir already exists')
            # If directory for storing previous scans exists,
            # find and save all previous scan file names
            self.get_local_scan_files()

        """ Create a blacklist text file in the local directory """
        if not exists(preset.blacklist_path):
            temp = open(preset.blacklist_path, 'w')
            temp.close()

    def scan_exists(self):
        return bool(self.scans)

    def get_local_scan_files(self):
        """ Create list of the file names for all locally saved scan data """
        self.scans = listdir(preset.scans_path)

    def get_hostname(self):
        hostname = ''
        try:
            recent_scan_path = preset.scans_path + self.scans[-1]
            with open(recent_scan_path, 'r') as f:
                for line in f:
                    line = line.split()
                    if 'router' == line[0]:
                        hostname = line[1]
        except FileNotFoundError as _:
            if not self.is_prod:
                print('!Error:', self.scans[-1], 'cannot be found')
        except IndexError as _:
            if not self.is_prod:
                print('!Error: No scans saved in local storage')
        return hostname

    def get_port_output(self):
        return self.port_output

    def get_devices(self):
        devices = []
        try:
            recent_scan_path = preset.scans_path + self.scans[-1]
            with open(recent_scan_path, 'r') as f:
                for line in f:
                    line = line.split()
                    if line and 'device' == line[0]:
                        devices.append(line[1:])
            return devices
        except FileNotFoundError as _:
            if not self.is_prod:
                print('!Error:', self.scans[-1], 'cannot be found')
        except IndexError as _:
            if not self.is_prod:
                print('!Error: No scans saved in local storage')
        return devices

    def get_device_name(self, ip):
        devices = self.get_devices()
        for device in devices:
            name, device_ip = device[0], device[1]
            if ip == device_ip:
                return name

    def get_device_names(self):
        devices = self.get_devices()
        return [device[0] for device in devices]

    def store_metadata(self, metadata):
        curr_scan_num = len(self.scans)
        curr_scan_filename = 'scan' + '_' + str(curr_scan_num)
        curr_scan_path = preset.scans_path + curr_scan_filename
        with open(curr_scan_path, 'w') as file:
            for ip in metadata:
                entry = ' '.join([metadata[ip][value] for value in metadata[ip]] + [ip, '\n'])
                file.write(entry)
        self.get_local_scan_files()

    def get_local_path(self):
        return preset.local_storage_path

    def generate_analysis_report(self, device_analysis):
        # TODO: Implement Kens Report Generator Here
        pass

    def save_analysis_report(self, filepath):
        if filepath:
            pass

    def open_analysis_report(self, filepath):
        if filepath:
            system("notepad.exe " + filepath)

    def scan(self):
        if self.log:
            print('starting scan')
        if self.scanner.networkScanner():
            metadata = self.scanner.getMetadata()
            self.store_metadata(metadata)
            if self.log:
                print('scan complete')
            return True
        else:
            if self.log:
                print("!Error: Scan not successful")
            return False

    def collect(self):
        print('collecting data')
        valid_devices = self.get_whitelist()
        self.port_output = self.scanner.portScanner(valid_devices)
        return self.port_output

    def upload(self):
        print('starting upload')
        self.update_devices()
        try:
            result = self.db_setup()
            print('upload complete')
            self.upload_success = True
            return result
        except:
            print('incomplete upload')
            self.upload_success = False
            return False

    def db_setup(self):
        if self.db.test_connection():
            self.db.create_collection('user_devices')
            entry = self.create_collection_entry(self.host, self.upload_devices)
            if not entry:
                return False
            self.db.insert_into_collection('user_devices', entry)
            self.isSetup = self.db.is_db_setup()
            return True
        else:
            print('!Error: Database is not responding')
            return False

    def create_collection_entry(self, host, device_list):
        host_id = 'U1IT' + str(self.device_count)
        self.device_count += 1
        enc_host_ip = fernet.encrypt(host['ip'].encode())
        host_name, host_ip = host['name'], enc_host_ip
        devices = {}
        if not device_list:
            return False

        for i, device in enumerate(device_list):
            device_id = 'U1IT' + str(self.device_count)
            self.device_count += 1
            devices[device_id] = device

        entry = {
            '_id': host_id,
            'host_name': host_name,
            'host_ip': host_ip,
            'devices': devices
        }
        return entry

    def can_upload(self):
        local_scans_path = preset.local_storage_path + '/local_scans'
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

    def update_blacklist(self, action, device_name):
        match action:
            case "add":
                with open(preset.blacklist_path, 'r+') as file:
                    for line in file:
                        if device_name in line:
                            print("!Error: Device already blacklisted")
                            return False
                    file.write(device_name + '\n')
            case "remove":
                devices = []
                with open(preset.blacklist_path, 'r') as file:
                    flag = 0
                    for line in file:
                        if device_name in line:
                            flag = 1
                        else:
                            devices.append(line)
                    if not flag:
                        return False
                f = open(preset.blacklist_path, 'r+')
                f.truncate(0)
                f.seek(0)
                f.writelines(devices)
        self.port_output = {}
        return True

    # def add_to_blacklist(self, device):
    #     blacklist = open(preset.blacklist_path, 'r')
    #     lines = blacklist.readlines()
    #     curr_list = []
    #     for line in lines:
    #         if device in line:
    #             print('!Error: Device already blacklisted')
    #             return False
    #         curr_list.append(line)
    #     print('Adding', device, 'to blacklist')
    #     curr_list.append(device + '\n')
    #     blacklist.close()
    #     blacklist = open(preset.blacklist_path, 'w')
    #     blacklist.writelines(curr_list)
    #     blacklist.close()
    #     self.port_output = {}
    #     return True
    #
    # def remove_from_blacklist(self, device):
    #     blacklist = open(preset.blacklist_path, 'r+')
    #     curr_devices = blacklist.readlines()
    #     if device + '\n' not in curr_devices:
    #         print('Error: Device is not blacklisted')
    #         return False
    #     new_devices = [line for line in curr_devices if device not in line]
    #     blacklist.truncate(0)
    #     blacklist.seek(0)
    #     blacklist.writelines(new_devices)
    #     self.port_output = {}
    #     return True

    def get_blacklist(self):
        device_list = []
        with open(preset.blacklist_path) as f:
            for line in f:
                device_list.append(line.strip('\n'))
        return device_list

    def get_whitelist(self):
        blacklist = self.get_blacklist()
        devices = self.get_devices()
        whitelist = []
        for device in devices:
            try:
                name = device[0]
                ip = device[1]
                if name not in blacklist:
                    whitelist.append(ip)
            except IndexError as _:
                continue
        return whitelist

    def device_analysis(self, devices):
        analysis = devices.copy()
        for device_ip in devices:
            ports = devices[device_ip]
            analysis[device_ip] = {'ports': analysis[device_ip]}
            if ports:
                risk = 0
                for port in ports:
                    if ports[port] == 'open':
                        risk += 1
                analysis[device_ip]['status'] = 'At Risk' if risk else 'Secure'
            else:
                analysis[device_ip]['status'] = 'Unknown'
        return analysis

    def device_summary(self, analyzed_devices):
        summary = {}
        for device_ip in analyzed_devices:
            name = self.get_device_name(device_ip)
            status = analyzed_devices[device_ip]['status']
            summary[device_ip] = {'name': name, 'status': status}
        return summary

    def update_devices(self):
        blacklist = self.get_blacklist()
        blacklist = [x.strip('\n') for x in blacklist]
        self.upload_devices = []
        for i, device in enumerate(self.devices):
            if device['name'] not in blacklist:
                self.upload_devices.append(device)
                enc_IP = fernet.encrypt(device['ip'].encode())
                self.upload_devices[-1]['ip'] = enc_IP

    def remove_scans(self):
        try:
            print(self.scans)
            for scan_filename in self.scans:
                scan_path = preset.scans_path + scan_filename
                remove(scan_path)
                self.scans.remove(scan_filename)
        except:
            print('error')
