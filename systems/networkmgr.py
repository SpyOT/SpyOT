import subprocess
import nmap
import pandas as pd
from os.path import exists, basename
import re

class NetworkMgr(object):
    def __init__(self, ip=''):
        wifi = subprocess.check_output(['netsh', 'WLAN', 'show', 'interfaces'])
        data = wifi.decode('utf-8')
        # print(data)

        self.default_gateway = self.get_default_gateway()
        self.nm = nmap.PortScanner()

        self.current_scan = get_recent_scan()
        self.report_path = None
        self.network_metadata = pd.DataFrame()
        self.load_metadata(self.current_scan)
        self.report_data = {}

        clean_up_local_storage()

    def scan_network(self):
        network_mask = '.'.join(self.default_gateway.split('.')[:-1]) + '.0' + '/24'

        try:
            print("Scanning IPs")
            self.nm.scan(hosts=network_mask, arguments='-sn')
            print("Scanning Complete")

            # Format scan data into a dataframe and set to network metadata attribute
            self.network_metadata = self.format_scan_data()
            # Set current scan to new scan path
            self.set_current_scan_path(new_scan_path())
            # Store metadata in a text file
            self.store_metadata()
            return True

        except Exception as e:
            print("!Error: Unable to scan network")
            print(e)
            return False

    def collect_data(self):
        """
        Collects data from each device on the network
        """
        try:
            # Filter metadata by blacklist status
            filtered_network_data = self.network_metadata[self.network_metadata['blacklist'] == False]
            # Get ips only device data
            filtered_device_ips = filtered_network_data[filtered_network_data['type'] == 'device']['ip'].values
            # Run deep scan on each host to check for open ports
            print("Deep Scanning Devices")
            deep_scan_data = self.deep_scan_devices(filtered_device_ips)
            # Run packet sniffing on each host to check for packet encryption
            print("Sniffing Packets")
            packet_data = {}  # TODO: Packet analysis
            print("Generating Report")
            # Generate Analysis Report
            report = self.generate_report(deep_scan_data,
                                          packet_data)
            # Store report in local storage
            self.store_report(report)
            return True
        except TypeError as e:
            print(f"!{e}: No data to collect")
            return False
        except Exception as e:
            print("!Error:", e)
            return False

    def format_upload_data(self):
        """
        Formats data to be uploaded to firebase
        data = {
        "id": Collection Report Name,
            device_name: {
                "ip": device_ip,
                "mac": device_mac,
                "status": secure
                "ports": {
                            "port23": state,
                            "port80": state,
                            "port2323": state,
                        }
                }, ...
        }
        """
        try:
            report_data = self.get_report_data()
            assert (report_data is not None)
            data = {'id': self.get_report_name()}
            device_port_data = report_data['devices']
            for device_ip in device_port_data:
                device_name = self.get_device_name(device_ip).split('.')[0]
                formatted_ip = re.sub(r'\.', '-', device_ip)
                data[device_name] = {
                    'ip': formatted_ip,
                    'mac': self.get_device_mac(device_ip),
                    'status': report_data['port_analysis']['device_status'][device_ip],
                    'ports': {}
                }
                for port in device_port_data[device_ip]:
                    data[device_name]['ports'][port] = device_port_data[device_ip][port]
            return data
        except AssertionError:
            print("!Error: No collect data to format")
            return None

    def format_scan_data(self):
        """
        Formats scan data into a dataframe
        """
        data = {'ip': [], 'mac': [], 'name': [], 'type': [], 'blacklist': []}
        for i, host_ip in enumerate(self.nm.all_hosts()):
            name_val = self.nm[host_ip]['hostnames'][0]['name']
            is_router = True if host_ip == self.default_gateway else False
            device_type = 'router' if is_router else 'device'
            if not name_val:
                device_name = 'Unnamed Device ' + str(i) if device_type == 'device' else 'Unnamed Router'
            else:
                device_name = name_val
            try:
                mac_addr = self.nm[host_ip]['addresses']['mac']
            except KeyError as _:
                mac_addr = '0:0:0:0:0:0'

            data['ip'].append(host_ip)
            data['mac'].append(mac_addr)
            data['name'].append(device_name)
            data['type'].append(device_type)
            data['blacklist'].append(False)

        # Check if 'router' is in column 'type'
        # Sometimes routers IP is not the same as default gateway
        if 'router' not in data['type']:
            data['ip'].append(self.default_gateway)
            data['mac'].append('N/A')
            data['name'].append('Unnamed Router')
            data['type'].append('router')
            data['blacklist'].append(False)

        return pd.DataFrame(data)

    def generate_report(self, port_data, packet_data):
        # analyze data
        port_analysis = self.analyze_port_data(port_data)
        packet_analysis = self.analyze_packet_capture(packet_data)
        self.report_data = {
            "port_analysis": port_analysis,
            "packet_analysis": packet_analysis,
            "devices": port_data
        }

        # build report
        # format header
        header = '\n'.join([
            "Network Analysis Report",
            '-' * 25,
            "Summary",
            '-' * 25,
            f"Network Name: {self.get_hostname()}",
            f"# of Devices Analyzed: {port_analysis['num_devices']}",
            f"Overall Data Encryption: {packet_analysis['encryption_percentage']}",
            f"Potential Vulnerabilities: {port_analysis['total_open_ports'] + packet_analysis['total_unencrypted_packets']}",
            '-' * 25])
        # format body
        body = f"Devices:\n{'-' * 25}\n"
        # Port Analysis
        devices = []
        for device_ip in port_data:
            name = self.get_device_name(device_ip)
            port_entries = '\n'.join([
                f"\tPort {port} Status:\t\t{port_data[device_ip][port]}" for port in port_data[device_ip]
            ])

            device_status = '\n'.join([
                f"Name: {name}",
                f"IP: {device_ip}",
                f"{port_entries}",
                f"Status: {port_analysis['device_status'][device_ip]}",
                "\n"])
            devices.append(device_status)
        devices = ''.join(devices)

        # Packet Analysis
        packets = ' '.join([
            "Percentage of Encrypted Data:",
            f"{packet_analysis['encryption_percentage']}\n",
            '-' * 25])

        body += devices + packets

        report = '\n'.join([header, body])
        return report

    def store_report(self, report):
        """
        Stores report in a new text file.
        """
        self.report_path = new_report_path()
        with open(self.report_path, 'w') as f:
            f.write(report)
        clean_up_local_storage()

    def store_metadata(self):
        """
        Stores metadata in a text file.
        Format: Dataframe(ips, mac_addr, names, types, blacklist_status)
        """
        with open(self.current_scan, 'w') as f:
            self.network_metadata.to_csv(f, sep=',', index=False, header=False, lineterminator='\n')
        clean_up_local_storage()

    def set_current_scan_path(self, scan_path):
        self.current_scan = scan_path

    def load_metadata(self, scan_path):
        """
        Loads metadata from a text file.
        """
        try:
            # check if scan path exists
            assert (exists(scan_path))
            self.network_metadata = pd.read_csv(scan_path, sep=',', header=None)
            self.network_metadata.columns = ['ip', 'mac', 'name', 'type', 'blacklist']
            self.set_current_scan_path(scan_path)
        except AssertionError:
            print("No scan data found. Please scan network first.")

    def get_device_ips(self):
        """
        Returns a list of device ips
        """
        try:
            return self.network_metadata[self.network_metadata['type'] == 'device']['ip'].tolist()
        except TypeError:
            print("!Error: No network metadata found")
            return []

    def get_report_name(self):
        report_name = basename(self.report_path)
        return report_name.split('.')[0]

    def get_hostname(self):
        return self.network_metadata[self.network_metadata['type'] == 'router']['name'].values[0]

    def get_device_name(self, ip):
        return self.network_metadata[self.network_metadata['ip'] == ip]['name'].tolist()[0]

    def get_filtered_device_ips(self):
        """
        Returns a list of device ips
        """
        try:
            return self.network_metadata[
                (self.network_metadata['type'] == 'device') & (self.network_metadata['blacklist'] == False)][
                'ip'].tolist()
        except TypeError:
            print("!Error: No network metadata found")
            return []

    def set_blacklist_status(self, ip, value):
        """
        Sets blacklist status of device
        """
        # check if ip is in metadata
        if ip not in self.network_metadata['ip'].tolist():
            print("!Error: IP not in metadata")
            return False

        match value:
            case True:
                # check if ip is already blacklisted
                if self.network_metadata.loc[self.network_metadata['ip'] == ip, 'blacklist'].tolist()[0]:
                    print("!Error: IP already blacklisted")
                    return False
                else:
                    self.network_metadata.loc[self.network_metadata['ip'] == ip, 'blacklist'] = value
                    self.store_metadata()
                    return True
            case False:
                # check if ip is already not blacklisted
                if not self.network_metadata.loc[self.network_metadata['ip'] == ip, 'blacklist'].tolist()[0]:
                    print("!Error: IP already not blacklisted")
                    return False
                else:
                    self.network_metadata.loc[self.network_metadata['ip'] == ip, 'blacklist'] = value
                    self.store_metadata()
                    return True

    def get_default_gateway(self):  # Grabs router default gateway
        wifi_data = self.get_wifi_data()
        if 'disconnected' not in ''.join(wifi_data):
            if "Default Gateway" in wifi_data[-1]:
                return wifi_data[-1].split(':')[1].strip()
            return wifi_data[-1]
        else:
            print("!Error: Not connected to an online network")
            return '0.0.0.0'

    def get_metadata(self):
        """
        Returns network metadata as a dataframe
        Format: Dataframe(ips, names, types, blacklist_status)
        :return:
        """
        if self.network_metadata.empty:
            print("!Error: No network metadata found")
            return self.network_metadata
        else:
            return self.network_metadata

    def deep_scan_devices(self, device_ip_list):
        """
        Scans devices for open ports
        deep_scan_data : {
            ip: { port: status }
            }
        """
        deep_scan_data = {}
        PORTS = ['23', '80', '2323']
        port_arg = ','.join(PORTS)
        for ip in device_ip_list:
            result = self.nm.scan(ip, arguments=' '.join(['-p ', port_arg]))  # Scan for open ports
            if result['scan']:
                port_info = result['scan'][ip]['tcp']
                deep_scan_data[ip] = {port: port_info[int(port)]['state'] for port in PORTS}
            else:
                print(f"!Error: Host {ip} is down or not responding")
                deep_scan_data[ip] = {port: 'down' for port in PORTS}
        return deep_scan_data

    def get_device_summary(self):
        """
        Returns a summary of the data on devices generated by collect_data()
        :return: Dictionary of network summary
        device_summary = { 'device_name': 'status' , ...}
        """
        device_status = self.report_data['port_analysis']['device_status']
        device_summary = {
            self.get_device_name(ip): device_status[ip] for ip in device_status
        }
        return device_summary

    def get_device_mac(self, ip):
        """
        Returns mac address of device
        """
        return self.network_metadata[self.network_metadata['ip'] == ip]['mac'].tolist()[0]

    def get_report_data(self):
        return self.report_data

    @staticmethod
    def analyze_port_data(port_data):
        """
        Analyzes port data and returns a report
        TODO: Maybe add more port analysis
            : Add more ports to scan
            : Close ports that are open
        :return: analysis = {
            'device_status': {
                                device0_ip: str,
                                device1_ip: str,
                                ...},
            'total_open_ports': int,
            'num_devices': int
        """
        analysis = {'device_status': {},
                    'total_open_ports': 0,
                    'num_devices': len(port_data),
                    }
        for ip, ports in port_data.items():
            analysis['device_status'][ip] = 'Secure'
            for port, status in ports.items():
                if status == 'open':
                    analysis['total_open_ports'] += 1
                    analysis['device_status'][ip] = 'At Risk'
                elif status == 'down':
                    analysis['device_status'][ip] = 'Unknown'
        return analysis

    @staticmethod
    def analyze_packet_capture(packet_capture):
        """
        Analyzes packet capture and returns a dictionary of results
        TODO: Implement packet capture analysis
            : Encrypt unencrypted packets
        """
        analysis = {'encryption_percentage': 0,
                    'total_encrypted_packets': 0,
                    'total_unencrypted_packets': 0}

        return analysis

    @staticmethod
    def get_wifi_data():
        ipconfig_output = subprocess.check_output(['ipconfig']).decode('utf-8')
        output = [line.strip('\r') for line in ipconfig_output.split('\n') if line.strip('\r')]
        start, end = 0, 0
        for i, line in enumerate(output):
            if start and not line.count('.'):
                end = i
                break
            if 'Wi-Fi' in line:
                start = i
        wifi_data = [line.strip(' ') for line in output[start + 1: end]]
        return wifi_data


if __name__ == "__main__":
    from utils import new_scan_path, get_recent_scan, new_report_path, clean_up_local_storage

    network = NetworkMgr()
    # scan_complete = network.scan_network()
    collect_complete = network.collect_data()
    # scan_complete = network.deep_scan_devices(network.get_device_ips())

else:
    from .utils import new_scan_path, get_recent_scan, new_report_path, clean_up_local_storage
