from networkScanning import NetworkScanner
from dataCapture import PCAPture  


class GenReport():
    def __init__(self):
        network = NetworkScanner()      #Make network object
        pcap = PCAPture()               #Make pcap object

        network.networkScanner()        #Network scan to report on
        self.device_list = network.host_ips     #Stores list of devices

        print(self.device_list)
        network.deepNetworkScanner(self.device_list)    #Network scan ports 80, 23, and 2323 and their status
        #network.ip_port_info = [['1.1', 1, 0, 0], ['1.2', 0, 0, 0], ['1.3', 0, 0, 0]]
        
        self.ip_info = network.ip_port_info     #Store port info
        self.openPorts = self.reviewOpenPorts()

        #pcap.packetCapture()
        pcap.encryptionPercentages = [98, 100, 56]
        self.encryptionData = pcap.encryptionPercentages
        self.overallEncryption = 0
        self.overallEncryption = self.recordOverallEncryption()

        self.report = ""
        
        
    def generateReport(self):
        self.report = f"Network Name: {self.device_list[0]}\n"  #Usually the router is in position 0 of device_list
        
        #Device list and stats
        self.report += f"\tNumber of devices:\n"
        self.report += f"\t\t{len(self.device_list)}\n"
        self.report += "\tOverall Data Encrypted:\n"
        self.report += f"\t\t{self.overallEncryption}\n"
        self.report += "\tPotential Vulnerabilities:\n"
        self.report += f"\t\t{self.openPorts}\n"
        
        #Port Status report
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
        sum = 0
        for row in range(len(self.ip_info)):
            if self.ip_info[row][1] == 1:
                sum += 1
            if self.ip_info[row][2] == 1:
                sum += 1
            if self.ip_info[row][3] == 1:
                sum += 1
        return sum
    
    def recordOverallEncryption(self):
        overallPercent = 0
        numOfPercentages = len(self.encryptionData)
        round = 0

        for percent in range(numOfPercentages):
            overallPercent += self.encryptionData[percent]

        overallPercent = overallPercent/numOfPercentages

        round = overallPercent - int(overallPercent) # Extract decimal part of the number
        if round >= 0.5:
                return int(overallPercent) + 1
        else:
            return int(overallPercent)
    
    def createFile(self):
        with open('NetworkReport.txt', "w") as f:
            f.write(self.report)

    pass

Report = GenReport()
Report.generateReport()
Report.createFile()