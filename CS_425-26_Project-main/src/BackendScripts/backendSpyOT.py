import nmap, socket

class NetworkScanner(object):
    def __init__(self, ip=''):
        #These two lines grab router ip address
        #hostname = socket.gethostname()
        #ip = socket.gethostbyname(hostname)

        #However 192.168.0.1 and 192.168.1.1 are default gateways

        ip = '192.168.1.1' 
        self.ip = ip
        self.host_list_size = 0
        self.host_list = []
        self.host_names = []
        self.host_ips = []

    def networkCheck(self):
        if(self.host_list_size == 0):      #If the gateway didn't bring any ips back
            if (self.ip == '192.168.1.1'):  #Change from 1.1 to 1.0
                self.ip = '192.168.1.0'
                self.networkPatch()
                return True         #Return boolean true for testing

            elif(self.ip == '192.168.1.0'):   #If the given gateway is 1.0
                self.ip = '192.168.1.1'       #Then change it to 1.1
                self.networkPatch()
                return True
        return False        #If for some reason none of the ips worked and we still have zero ips, return false for testing.
    
    def networkPatch(self):
        network = self.ip + '/24'
        nm = nmap.PortScanner() 
        nm.scan(hosts = network, arguments = '-sn')
        self.host_list = [(x, nm[x] ['status'] ['state']) for x in nm.all_hosts()]

    def networkCounter(self):
        self.host_list_size = len(self.host_list) #Counts the amount of connected devices in a network.
        
        return self.host_list_size

    def networkScanner(self):
        if len(self.ip) == 0:
            print("No IP address given")  #If there's no ip given

        else:
            network = self.ip + '/24'
            print("Scanning IPs") #this takes awhile.

            nm = nmap.PortScanner() #nm is used to scan the network
            nm.scan(hosts = network, arguments = '-sn')
            
            #Stores a list of every ip address on the network into host_list
            self.host_list = [(x, nm[x] ['status'] ['state']) for x in nm.all_hosts()]

            self.networkCounter()

            self.networkCheck()

            self.tupleSeparater()

    def tupleSeparater(self):
        for host, b, ip in self.host_list:
            if(host == self.ip):
                print("\n List of connected devices:  ")
                print("_______________________________")
            else:
                    print(host)
                    host, b, ip = socket.gethostbyaddr(host) #The tuple returned puts ip strings in a list
                    for x in range(self.host_list_size - 1): #This for loop takes the string ip out of the list
                        ip = ip[x]
                    self.host_names.append(host)    #Stores the names of the devices
                    self.host_ips.append(ip)        #Stores the ip of the devices
                #Test:
            print("\nDevice names here:\n_______________")
            print(self.host_names)
            print("\nDevice Ip addresses here:\n_____________")
            print(self.host_ips)
        numHostNames = len(self.host_names)

        return numHostNames #For testing purposes this is going to verify that we have names inside the attribute host_name.

if __name__ == "__main__":
    network = NetworkScanner()
    network.networkScanner()