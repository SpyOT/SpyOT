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
        self.ip_port_info = []

        self.device_list = {"devices": []}

        self.nm = nmap.PortScanner()

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
            gateway_ip_entry = wifi_entry[gateway_ip_index]
            if '::' in wifi_entry[gateway_ip_index]:
                gateway_ip_entry = wifi_entry[gateway_ip_index + 1]
            else:
                gateway_ip_entry = wifi_entry[gateway_ip_index].split()[-1]
            wifi_data["default_gateway"] = gateway_ip_entry
        return wifi_data

    def setDefaultGateway(self):    #This is how we grab router IP default gateway
        wifi_data = self.getWiFiData()
        if wifi_data["connected"]:
            self.default_gateway = wifi_data["default_gateway"]
            return True
        else:
            print("!Error: Not connected to an online network.")
            return False

    def networkPatch(self):
        curr_network = self.ip + '/24'
        self.nm.scan(hosts=curr_network, arguments='-sn')
        self.host_list = [(x, self.nm[x]['status']['state']) for x in self.nm.all_hosts()]

    def networkCounter(self):
        self.host_list_size = len(self.host_list)  # Counts the amount of connected devices in a network.

    def networkScanner(self):
        network_mask = '.'.join(self.ip.split('.')[:-1]) + '.0' + '/24'

        print("Scanning IPs")  # this takes awhile.
        nm = self.nm  # nm is used to scan the network
        nm.scan(hosts=network_mask, arguments='-sn')

        # Stores a list of every ip address on the network into host_list
        self.host_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]


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
        return self.host_ips

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
        
    def deepNetworkScanner(self, ips):
        for ip in range(len(ips)):
            self.nm.scan(hosts=ips[ip],arguments='-p 80,23,2323') #Scans given targets (ips) and their ports
            print(f'for ip {ips[ip]}:')
            self.ip_port_info.append([ips[ip], 0, 0, 0])
            try:
                if self.nm[ips[ip]]['tcp'][80]['state'] == 'open':  #Scans if port 80 is open
                    print('Port 80 is OPEN----------')
                    self.ip_port_info[ip][1] = 1
                else:
                    print('Port 80 CLOSED.')
                    self.ip_port_info[ip][1] = 0


                if self.nm[ips[ip]]['tcp'][23]['state'] == 'open':    #Scans if port 23 is open
                    print('Port 23 is OPEN----------')
                    self.ip_port_info[ip][2] = 1
                else:
                    print('Port 23 CLOSED.')
                    self.ip_port_info[ip][2] = 0


                if self.nm[ips[ip]]['tcp'][2323]['state'] == 'open':    #Scans if port 2323 is open
                    print('Port 2323 is OPEN----------')
                    self.ip_port_info[ip][3] = 1
                else:
                    print('Port 2323 CLOSED.')
                    self.ip_port_info[ip][3] = 0


            except:
                print(f'Error on ip: {ips[ip]}, attempting rescan')    #Unknown port scanning error on given target, suggested rescan
                self.portRescan(ips[ip])    #Rescans device with error thrown

        pass

    def portRescan(self, ip):
        self.nm.scan(hosts=ip,arguments='-p 80,23,2323') #Recans the given target that threw an error
        self.ip_port_info.append([ip, 0, 0, 0])
        try:
            if self.nm[ip]['tcp'][80]['state'] == 'open':  #Rescans if port 80 is open
                print('Port 80 is OPEN----------')
                self.ip_port_info[0][1] = 1
            else:
                print('Port 80 CLOSED.')
                self.ip_port_info[0][1] = 0


            if self.nm[ip]['tcp'][23]['state'] == 'open':    #Rescans if port 23 is open
                print('Port 23 is OPEN----------')
                self.ip_port_info[0][2] = 1
            else:
                print('Port 23 CLOSED.')
                self.ip_port_info[0][2] = 0


            if self.nm[ip]['tcp'][2323]['state'] == 'open':    #Rescans if port 2323 is open
                print('Port 2323 is OPEN----------')
                self.ip_port_info[0][3] = 1
            else:
                print('Port 2323 CLOSED.')
                self.ip_port_info[0][3] = 0

        except:
            print('Rescan attempt unsuccessful.')
        
        pass


if __name__ == "__main__":
    network = NetworkScanner()
    IP_addresses = network.networkScanner()
    
    network.deepNetworkScanner(IP_addresses)
    
    print(network.ip_port_info)
    #network.deepNetworkScanner(IP_addresses)
