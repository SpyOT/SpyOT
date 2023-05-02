import subprocess
import nmap
import pandas as pd
from os.path import exists


# import sys
# import socket
# from datetime import datetime

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
        self.device_summary = {}

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

    def get_upload_data(self):
        summary = self.get_device_summary()
        data = {
            self.get_device_name(ip): summary[ip] for ip in summary
        }
        return data

    def format_scan_data(self):
        """
        Formats scan data into a dataframe
        """
        data = {'ip': [], 'name': [], 'type': [], 'blacklist': []}
        for ip in self.nm.all_hosts():
            print(ip, self.nm[ip].hostname(), self.nm[ip].state())
        for i, host_ip in enumerate(self.nm.all_hosts()):
            name_val = self.nm[host_ip]['hostnames'][0]['name']
            device_name = name_val if name_val else 'Unnamed Device ' + str(i)
            is_router = True if host_ip == self.default_gateway else False
            device_type = 'router' if is_router else 'device'

            data['ip'].append(host_ip)
            data['name'].append(device_name)
            data['type'].append(device_type)
            data['blacklist'].append(False)

        # Check if 'router' is in column 'type'
        # Sometimes routers IP is not the same as default gateway
        if 'router' not in data['type']:
            data['ip'].append(self.default_gateway)
            data['name'].append('Unnamed Router')
            data['type'].append('router')
            data['blacklist'].append(False)

        return pd.DataFrame(data)

    def generate_report(self, port_data, packet_data):
        # analyze data
        port_analysis = self.analyze_port_data(port_data)
        packet_analysis = self.analyze_packet_capture(packet_data)
        self.device_summary = port_analysis['device_status']

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
        Format: Dataframe(ips, names, types, blacklist_status)
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
            self.network_metadata.columns = ['ip', 'name', 'type', 'blacklist']
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
        return self.device_summary

    @staticmethod
    def analyze_port_data(port_data):
        """
        Analyzes port data and returns a report
        TODO: Maybe add more port analysis
            : Add more ports to scan
            : Close ports that are open
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

    # def getMetadata(self):
    #     return self.network_metadata
    #
    # def deepPortScanner(self, ip_list=list):
    #     ips = ip_list if ip_list else self.getMetadata()
    #     try:
    #         targets = [ip for ip in ips]
    #         # Iterate through each ip address and return open ports
    #
    #         for ip in targets:
    #             print("-" * 50)
    #             print("Scanning Target: " + ip)
    #             print("Scanning started at:" + str(datetime.now()))
    #             for port in range(1, 1023):  # Change number of sockets that will be scanned
    #                 s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #                 socket.setdefaulttimeout(1)
    #
    #                 # returns an error indicator
    #                 result = s.connect_ex((ip, port))
    #                 if result == 0:
    #                     print("Port {} is open".format(port))  # print port number that is open
    #                 s.close()  # close port once done and iterate through to next ip address
    #             print("-" * 50)
    #     except KeyboardInterrupt:
    #         print("\n Exiting Program !!!!")
    #         sys.exit()
    #     except socket.gaierror:
    #         print("\n Hostname Could Not Be Resolved !!!!")
    #         sys.exit()
    #     except socket.error:
    #         print("\n Server not responding !!!!")
    #         sys.exit()
    #
    # def portScanner(self, ip_list=list):
    #     ips = ip_list if ip_list else self.getMetadata()
    #     ips = [ip for ip in ips]
    #     deep_scan_result = {}
    #     for ip in ips:
    #         try:
    #             deep_scan_result[ip] = {}
    #             self.nm.scan(hosts=ip, arguments='-p 80,23,2323')  # Scans given targets (ips) and their ports
    #             print('for ip {}:'.format(ip))
    #             for value in self.nm[ip]['tcp']:
    #                 deep_scan_result[ip][value] = self.nm[ip]['tcp'][value]['state']
    #                 print('\t', value, self.nm[ip]['tcp'][value]['state'])
    #         except KeyError as _:
    #             print("!Error: Scanning ports for ip {}".format(ip))
    #     return deep_scan_result
    #
    # def analyzePorts(self):
    #     deep_scan = self.network_deepscan
    #     analysis = deep_scan.copy()
    #     for ip in deep_scan:
    #         try:
    #             if not deep_scan[ip]['ports']:
    #                 analysis[ip] = {'ports': deep_scan[ip], 'status': 'Unknown'}
    #             else:
    #                 open_ports = sum([1 if deep_scan[ip][port] == 'open' else 0 for port in deep_scan[ip]])
    #                 if open_ports:
    #                     analysis[ip] = {'ports': deep_scan[ip], 'status': 'At Risk'}
    #                 else:
    #                     analysis[ip] = {'ports': deep_scan[ip], 'status': 'Secure'}
    #         except KeyError as _:
    #             pass
    #     self.network_deepscan = analysis
    #     return analysis


#    def portRescan(self, ip):
#        self.nm.scan(hosts=ip, arguments='-p 80,23,2323')  # Recans the given target that threw an error
#        self.ip_port_info.append([ip, 0, 0, 0])
#        try:
#            if self.nm[ip]['tcp'][80]['state'] == 'open':  # Rescans if port 80 is open
#                print('Port 80 is OPEN----------')
#                self.ip_port_info[0][1] = 1
#            else:
#                print('Port 80 CLOSED.')
#                self.ip_port_info[0][1] = 0
#
#            if self.nm[ip]['tcp'][23]['state'] == 'open':  # Rescans if port 23 is open
#                print('Port 23 is OPEN----------')
#                self.ip_port_info[0][2] = 1
#            else:
#                print('Port 23 CLOSED.')
#                self.ip_port_info[0][2] = 0
#
#            if self.nm[ip]['tcp'][2323]['state'] == 'open':  # Rescans if port 2323 is open
#                print('Port 2323 is OPEN----------')
#                self.ip_port_info[0][3] = 1
#            else:
#                print('Port 2323 CLOSED.')
#                self.ip_port_info[0][3] = 0
#
#        except:
#            print('Rescan attempt unsuccessful.')


if __name__ == "__main__":
    from utils import new_scan_path, get_recent_scan, new_report_path, clean_up_local_storage

    network = NetworkMgr()
    # scan_complete = network.scan_network()
    collect_complete = network.collect_data()
    # scan_complete = network.deep_scan_devices(network.get_device_ips())

else:
    from .utils import new_scan_path, get_recent_scan, new_report_path, clean_up_local_storage
