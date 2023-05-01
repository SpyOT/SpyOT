import subprocess
import nmap
import sys
import socket
from datetime import datetime


class NetworkScanner(object):
    def __init__(self, ip=''):
        wifi = subprocess.check_output(['netsh', 'WLAN', 'show', 'interfaces'])
        data = wifi.decode('utf-8')
        # print(data)
        self.default_gateway = self.getDefaultGateway().split()[-1]
        self.ip = ip if ip else self.default_gateway
        self.nm = nmap.PortScanner()
        self.network_metadata = {}
        self.network_deepscan = {}
        self.filtered_network_data = {}
        self.host_ips = []
        self.ip_port_info = []

    def getWiFiData(self):
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

    def getDefaultGateway(self):  # Grabs router default gateway
        wifi_data = self.getWiFiData()
        if 'disconnected' not in ''.join(wifi_data):
            return wifi_data[-1]
        else:
            print("!Error: Not connected to an online network")
            return '0.0.0.0'

    def getDeviceCount(self):
        # Counts the amount of connected devices in a network.
        return sum([1 for data in self.network_metadata if self.network_metadata[data]['type'] == 'device'])

    def networkScanner(self):
        network_mask = '.'.join(self.ip.split('.')[:-1]) + '.0' + '/24'
        nm = self.nm
        try:
            print("Scanning IPs")
            nm.scan(hosts=network_mask, arguments='-sn')
            print("Scanning Complete")
            scanned_ips = nm.all_hosts()
            print('bro')
            for i, host_ip in enumerate(scanned_ips):
                hostname = nm[host_ip]['hostnames'][0]['name']
                hostname = hostname if hostname else 'device{}'.format(i)
                host_type = 'device' if host_ip != self.default_gateway else 'router'
                print(self.default_gateway, host_ip)
                if hostname:
                    self.network_metadata[host_ip] = {
                        'type': host_type,
                        'hostname': hostname
                    }
            return True
        except:
            return False

    def getMetadata(self):
        return self.network_metadata

    def displayMetadata(self, data):
        for ip in data:
            if data[ip]['type'] == 'router':
                print("Host:", ip, data[ip]['hostname'])
                print("List of connected devices:")
                print("--------------------------")
            else:
                print(ip, data[ip]['hostname'], sep='\t')
        print("--------------------------")
        print("Number of devices in network:", self.getDeviceCount())

    def deepPortScanner(self, ip_list=[]):
        ips = ip_list if ip_list else self.getMetadata()
        try:
            targets = [ip for ip in ips]
            # Iterate through each ip address and return open ports

            for ip in targets:
                print("-" * 50)
                print("Scanning Target: " + ip)
                print("Scanning started at:" + str(datetime.now()))
                for port in range(1, 1023):  # Change number of sockets that will be scanned
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    socket.setdefaulttimeout(1)

                    # returns an error indicator
                    result = s.connect_ex((ip, port))
                    if result == 0:
                        print("Port {} is open".format(port))  # print port number that is open
                    s.close()  # close port once done and iterate through to next ip address
                print("-" * 50)
        except KeyboardInterrupt:
            print("\n Exiting Program !!!!")
            sys.exit()
        except socket.gaierror:
            print("\n Hostname Could Not Be Resolved !!!!")
            sys.exit()
        except socket.error:
            print("\n Server not responding !!!!")
            sys.exit()

    def portScanner(self, ip_list=[]):
        ips = ip_list if ip_list else self.getMetadata()
        ips = [ip for ip in ips]
        deep_scan_result = {}
        for ip in ips:
            try:
                deep_scan_result[ip] = {}
                self.nm.scan(hosts=ip, arguments='-p 80,23,2323')  # Scans given targets (ips) and their ports
                print('for ip {}:'.format(ip))
                for value in self.nm[ip]['tcp']:
                    deep_scan_result[ip][value] = self.nm[ip]['tcp'][value]['state']
                    print('\t', value, self.nm[ip]['tcp'][value]['state'])
            except KeyError as _:
                print("!Error: Scanning ports for ip {}".format(ip))
        return deep_scan_result

    def analyzePorts(self):
        deep_scan = self.network_deepscan
        analysis = deep_scan.copy()
        for ip in deep_scan:
            try:
                if not deep_scan[ip]['ports']:
                    analysis[ip] = {'ports':deep_scan[ip], 'status': 'Unknown'}
                else:
                    open_ports = sum([1 if deep_scan[ip][port] == 'open' else 0 for port in deep_scan[ip]])
                    if open_ports:
                        analysis[ip] = {'ports': deep_scan[ip], 'status': 'At Risk'}
                    else:
                        analysis[ip] = {'ports': deep_scan[ip], 'status': 'Secure'}
            except KeyError as _:
                pass
        self.network_deepscan = analysis
        return analysis

    def generateSummary(self):
        networkscan = self.network_metadata
        portscan = self.network_deepscan
        summary = {}
        for ip in networkscan:
            if networkscan[ip]['type'] == 'device':
                name = networkscan[ip]['hostname']
                status = portscan[ip]['status']
                summary[ip] = {'name': name, 'status':status}
        return summary

    def filter_blacklist_ips(self, blacklist):
        self.filtered_network_data = self.network_metadata.copy()
        for ip in self.network_metadata:
            if self.network_metadata[ip]['hostname'] in blacklist:
                del self.filtered_network_data[ip]

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
    network = NetworkScanner()
    scan_complete = network.networkScanner()
    if scan_complete:
        network.displayMetadata(network.getMetadata())
    else:
        print("!Error: Scan was not successful")

    scan_result = network.portScanner()
    # network.deepNetworkScanner()
