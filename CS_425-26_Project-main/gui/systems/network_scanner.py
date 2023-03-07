import subprocess
import nmap
import sys
import socket
from datetime import datetime


class NetworkScanner(object):
    def __init__(self, ip=''):
        # These two lines grab router ip address
        # hostname = socket.gethostname()
        # test_ip = socket.gethostbyname(hostname)
        wifi = subprocess.check_output(['netsh', 'WLAN', 'show', 'interfaces'])
        data = wifi.decode('utf-8')
        # print(data)
        self.default_gateway = ''
        self.setDefaultGateway()

        self.ip = ip if ip else self.default_gateway
        self.host_list_size = 0
        self.host_list = []
        self.host_ips = []
        self.device_list = {"devices": []}

    def getWiFiData(self):
        ipconfig_output = subprocess.check_output(['ipconfig']).decode('utf-8').split('\n')
        ipconfig_output = [line.strip(' \r') for line in ipconfig_output if line.strip('\r')]
        headers = []
        for line in ipconfig_output:
            line = line.strip('\r\n')
            if '. :' not in line and ':' in line:
                headers.append(line)
        wifi_header_index = [i for i, line in enumerate(headers) if 'Wi-Fi' in line][0]
        wifi_header_start, wifi_header_end = headers[wifi_header_index], headers[wifi_header_index + 1]
        wifi_start_index, wifi_end_index = ipconfig_output.index(wifi_header_start), ipconfig_output.index(
            wifi_header_end)
        wifi_entry = ipconfig_output[wifi_start_index: wifi_end_index]
        default_gateway_entry = [(i, line) for i, line in enumerate(wifi_entry) if "Default Gateway" in line]
        wifi_data = {"connected": False}
        if default_gateway_entry:
            wifi_data["connected"] = True
            gateway_ip_index = default_gateway_entry[0][0]
            wifi_data["default_gateway"] = wifi_entry[gateway_ip_index + 1]
        return wifi_data

    def setDefaultGateway(self):
        wifi_data = self.getWiFiData()
        if wifi_data["connected"]:
            self.default_gateway = wifi_data["default_gateway"]
            return True
        else:
            print("!Error: Not connected to an online network.")
            return False

    def networkCheck(self):
        if (self.host_list_size == 0):
            if (self.ip == '192.168.1.1'):
                self.ip = '192.168.1.0'
                self.networkPatch()

            elif (self.ip == '192.168.1.0'):
                self.ip = '192.168.1.1'
                self.networkPatch()

    def networkPatch(self):
        network = self.ip + '/24'
        nm = nmap.PortScanner()
        nm.scan(hosts=network, arguments='-sn')
        self.host_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]

    def networkCounter(self):
        self.host_list_size = len(self.host_list)  # Counts the amount of connected devices in a network.

    def networkScanner(self):
        network_mask = '.'.join(self.ip.split('.')[:-1]) + '.0' + '/24'

        print("Scanning IPs")  # this takes awhile.
        nm = nmap.PortScanner()  # nm is used to scan the network
        nm.scan(hosts=network_mask, arguments='-sn')

        # Stores a list of every ip address on the network into host_list
        self.host_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]

        #self.networkCounter()

        #self.networkCheck()

        for host, up in self.host_list:
            if (host == self.ip):
                try:
                    self.device_list["host"] = socket.gethostbyaddr(host)
                except:
                    print("Network is missing hostname")
                    self.device_list["host"] = ["Unknown host", [], [self.default_gateway]]
                print("\n List of connected devices:  ")
                print("_______________________________")
            else:
                try:
                    print(socket.gethostbyaddr(host))
                    self.device_list["devices"].append(socket.gethostbyaddr(host))
                except:
                    print("!Error:", host, "is missing hostname")
        # grabs ip addresses from host_list and adds to its list
        for i in self.host_list:
            self.host_ips.append(i[0])

    def portScanner(self):
        try:
            target = self.host_ips.copy()
            # Iterate through each ip address and return open ports
            for x in range(len(target)):
                print("-" * 50)
                print("Scanning Target: " + str(target[x]))
                print("Scanning started at:" + str(datetime.now()))
                for port in range(1, 5):  # Change number of sockets that will be scanned
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    socket.setdefaulttimeout(1)

                    # returns an error indicator
                    result = s.connect_ex((str(target[x]), port))
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
            print("\ Server not responding !!!!")
            sys.exit()

    def pcapScanner(self, file):
        pass


if __name__ == "__main__":
    network = NetworkScanner()
    IP_addresses = network.networkScanner()
    # network.P_Scanner()
