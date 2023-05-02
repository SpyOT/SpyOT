#Figure out why some TCP Payloads are not showing as encrypted
import pyshark
import os

os.system("tshark -i Wi-Fi -c 2000 -w Eavesdrop_Data.pcap") #Captures data from tshark and stores it.
class PCAP():
	def __init__(self):
		self.pcapfile = "./Eavesdrop_Data.pcap"
		self.capture = pyshark.FileCapture(self.pcapfile)
		self.TCPpayload = None
		self.TCPdata = ""
		self.Encrypted_counter = 0
		self.Non_encrypted_counter = 0
		self.total = 0
	
	def findTCPpayload(self):
		for packet in self.capture:
			if hasattr(packet['TCP'], 'payload'):
				self.TCPpayload = packet['TCP'].payload
				self.TCPdata = packet.tcp.payload.decode('utf-8') 	#Decodes TCP data into a string
				if 'ssl' in self.TCPpayload or 'tls' in self.TCPpayload:
					#TCP payload encrypted.
					return False	#False for unit testing purposes
				else:
					#TCP likely holds unencrypted data.
					return True		#True for unit testing purposes
			else:
				return False	#No TCP payload found in packet
		

	def packetCapture(self):
		
		for packet in self.capture:
			try:
				if 'tls' in packet and 'tcp' in packet or 'quic' in packet:	#In the case that a packet is fully encrypted
					print('Packet is encrypted.')
					self.Encrypted_counter += 1
					self.total += 1

				elif self.TCPpayload in packet is None:	#In the case that no payload was found/given
					print("No payload")
					self.total += 1

				else:
					print("1")
					self.total += 1										#If the above ifs aren't met, we start counting packets.
					self.Non_encrypted_counter += 1
					hex_string = str(self.TCPpayload)
					hex_split = hex_string.split(":")
					hex_as_chars = map(lambda hex: chr(int(hex, 16)), hex_split)
					human_readable = "".join(hex_as_chars)
					#print(human_readable)
					#print (type(payload))
					#print(str(payload))
			except:
				pass
				#break
		self.capture.close()
		self.dataEncryptionPercent()
		pass		#Best to think of a return value so we can test this function
	
	def dataEncryptionPercent(self):
		try:

			print("Total number of packets analyzed:", self.total)
			Percentage_of_encrypted = (self.Encrypted_counter/(self.Non_encrypted_counter + self.Encrypted_counter))*100
			print("Percentage of encrypted data ", Percentage_of_encrypted)
			return Percentage_of_encrypted
		except:
			print("Couldn't find TCP protocol")
			return None

	
if __name__ == '__main__':
    PCAP_instance = PCAP()
    PCAP_instance.packetCapture()