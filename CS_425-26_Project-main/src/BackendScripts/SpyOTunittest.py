#Kenneth Peterson
#SpyOT unittesting
#02/22/23
#SpyOtUnittest.py

from backendSpyOT import NetworkScanner
import unittest

class testSpyOT(unittest.TestCase):
    #Naming convention is important, make sure it starts with "test_"
    def test_network_counter(self):        #In this test I'll be checking if network counter returns a number of ips in the host list.
        testNetwork = NetworkScanner()     #For unittests we need to make objects for testing,

        hasNothing = testNetwork.networkCounter()   #Should have nothing in it, testNetwork has no network IPs
        testNetwork.host_list = ["192.168.28.1"]     #Just give it whatever ip so the "hasSomething" variable gets incremented (By one in this case)
        hasSomething = testNetwork.networkCounter()
        self.assertNotEqual(hasSomething, hasNothing)   #This is how unittesting is done, there's a bunch of methods for asserting true or false, equal or not equal, it all comes down to return statements.

    def test_no_gateway_given(self):
        testNetwork = NetworkScanner()

        testNetwork.ip = "Neither default gateway 1.1 or 0.0"
        self.assertFalse(testNetwork.networkCheck())
        
    
    

if __name__ == '__main__':
    unittest.main()