#Ken Escovilla
#SpyOT network unittest
#03/01/23
#SpyOtUnittest.py

from backendSpyOT import NetworkScanner
import unittest

class test_network_given(unittest.TestCase):
   
    def test_network_counter(self):       
        testNetwork = NetworkScanner()     

        a = 1
        testNetwork.host_list = ["192.168.16.1"]     
        self.assertEqual(a, testNetwork.networkCounter()) 

if __name__ == '__main__':
    unittest.main()
