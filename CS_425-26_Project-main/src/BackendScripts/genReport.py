class GenReport():
    def __init__(self):
        self.network = NetworkMgr()  # Make network object
        self.pcap = PCAPture()  # Make pcap object

        self.router_name = ""
        self.device_list = []
        self.ip_info = []
        self.totalOverallOpenPorts = 0

        # pcap.packetCapture()
        self.encryptionPercentages = [98, 100, 56]
        # self.encryptionData = self.pcap.encryptionPercentages
        self.encryptionData = []
        self.overallEncryption = 0
        # self.overallEncryption = self.recordOverallEncryption()

        self.report = ""

    def generateData(self):
        self.network.scan_network()  # Network scan to report on
        self.device_list = self.network.get_device_ips()  # Stores list of devices
        print('device list', self.device_list, '\n')

        # Network scan ports 80, 23, and 2323 and their status
        # Return Format : { IP : { Port # : Status } }
        deep_scan_data = self.network.deep_scan_devices(self.device_list)
        print('deep scan data', deep_scan_data, '\n')

        # Store port info
        # network.ip_port_info = [['1.1', 1, 0, 0], ['1.2', 0, 0, 0], ['1.3', 0, 0, 0]]
        for device_ip in deep_scan_data:
            port_status = [1 if deep_scan_data[device_ip][port] == 'open' else 0 for port in deep_scan_data[device_ip]]
            self.ip_info.append([device_ip] + port_status)
        print('ip info', self.ip_info, '\n')
        self.reviewOpenPorts()
        print('total open ports', self.totalOverallOpenPorts, '\n')

        self.encryptionData = [0] * len(self.device_list)

    def generateReport(self):
        self.report = f"Network Name: {self.device_list[0]}\n"  # Usually the router is in position 0 of device_list

        # Device list and stats
        self.report += f"\tNumber of devices:\n"
        self.report += f"\t\t{len(self.device_list)}\n"
        self.report += "\tOverall Data Encrypted:\n"
        self.report += f"\t\t{self.overallEncryption}\n"
        self.report += "\tPotential Vulnerabilities:\n"
        self.report += f"\t\t{self.totalOverallOpenPorts}\n"

        # Port Status report
        self.report += "\n\tDevice Status:\n"

        for row in range(len(self.ip_info)):
            self.report += "\t\tIP:"
            self.report += f"  {self.ip_info[row][0]}\n"

            self.report += "\t\t\tPort 80 Status:\t"
            if self.ip_info[row][1] == 1:
                self.report += "\topen\n"
            else:
                self.report += "\tclosed\n"

            self.report += "\t\t\tPort 23 Status:\t"
            if self.ip_info[row][2] == 1:
                self.report += "\topen\n"
            else:
                self.report += "\tclosed\n"

            self.report += "\t\t\tPort 2323 Status:\t"
            if self.ip_info[row][3] == 1:
                self.report += "\topen\n"
            else:
                self.report += "closed\n"

            self.report += "\t\tPercentage Of Encrypted Data:"
            self.report += f"\t{self.encryptionData[row]}"
            self.report += "\n________________________________\n\n"
        pass

    def reviewOpenPorts(self):
        for row in range(len(self.ip_info)):
            if self.ip_info[row][1] == 1:
                self.totalOverallOpenPorts += 1
            if self.ip_info[row][2] == 1:
                self.totalOverallOpenPorts += 1
            if self.ip_info[row][3] == 1:
                self.totalOverallOpenPorts += 1

    def recordOverallEncryption(self):
        overallPercent = 0
        numOfPercentages = len(self.encryptionData)
        round = 0

        for percent in range(numOfPercentages):
            overallPercent += self.encryptionData[percent]

        overallPercent = overallPercent / numOfPercentages

        round = overallPercent - int(overallPercent)  # Extract decimal part of the number
        if round >= 0.5:
            return int(overallPercent) + 1
        else:
            return int(overallPercent)

    def createFile(self):
        with open('NetworkReport.txt', "w") as f:
            f.write(self.report)


def main():
    Report = GenReport()
    Report.generateData()
    Report.generateReport()
    Report.createFile()


if __name__ == '__main__':
    from networkmgr import NetworkMgr
    from dataCapture import PCAPture

    main()
else:
    from systems.networkmgr import NetworkMgr
    from .dataCapture import PCAPture

    main()
